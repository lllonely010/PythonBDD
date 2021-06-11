from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from appium import webdriver as appiumwebdriver
from appium.webdriver.common.mobileby import MobileBy
import logging
import os
import json
import requests
import time
from PIL import Image, ImageDraw, ImageChops
from appium.webdriver.common.touch_action import TouchAction

class Ui(object):

    def __init__(self, session, config_string):
        connection_json = json.loads(config_string)
        self.connection_json = connection_json
        self.isclosed=True
        self.session = session
        self.driver = None
        self.object_data = {self.session: {}}
        self.start_driver()

    def click(self, selector):
        e = self.find_element(selector)
        if e:
            e.click()

    def scroll_to_element(self, selector_start, selector_end):
        element_to_tap = self.find_element(selector_start).location['y']
        element_to_drag_to = self.find_element(selector_end).location['y']
        TouchAction(self.driver).press(x=0, y=element_to_tap).move_to(x=0, y=element_to_drag_to).release().perform()
    
    def sroll_to_top(self):
        x1 = self.driver.get_window_size()["width"]
        y1 = self.driver.get_window_size()["height"]
        TouchAction(self.driver).press(x = int(x1*0.5), y= int(y1*0.8)).move_to(x = int(x1*0.5), y= int(y1*0.2)).release().perform()

    def start_driver(self):
        pass

    def wait_for_element(self, element):
        e = self.find_element(element, retries=10)
        assert e, f"element {element} not found"
        return e

    def wait_for_elements(self, element):
        e = self.find_elements(element, retries=10)
        assert len(e) > 0, f"element {element} not found"

    def wait_for_element_and_click_it(self, element):
        e = self.wait_for_element(element)
        e.click()

    def wait_for_random_elementAndClick(self, selector):
        try:
            if self.wait_for_enabled_element(selector):
                self.click(selector)
        except:
            logging.debug(f"Random element {selector} is not displayed")

    def wait_for_enabled_element(self, selector):
        if "css:" == selector[0:4]:
            element_to_be_located = selector.lstrip("css:")
            selector_type = By.CSS_SELECTOR
        elif "id:" == selector[0:3]:
            element_to_be_located = selector.lstrip("id:")
            selector_type = By.ID
        elif "xpath:" == selector[0:6]:
            element_to_be_located = selector.lstrip("xpath:")
            selector_type = By.XPATH
        elif "name:" == selector[0:5]:
            element_to_be_located = selector.lstrip("name:")
            selector_type = By.NAME
        elif "accessibility:" == selector[0:14]:
            element_to_be_located = selector[14:]
            selector_type = MobileBy.ACCESSIBILITY_ID
        elif "uiautomator:" == selector[0:12]:
            element_to_be_located = selector[12:]
            selector_type = MobileBy.ANDROID_UIAUTOMATOR
        else:
            assert False, f"find element supports css, id, name and xpath.  {selector} doesn't state any one of those."
        wait = WebDriverWait(self.driver, 30)
        enabled = wait.until(ExpectedConditions.element_to_be_clickable((selector_type, element_to_be_located)))
        return enabled

    def is_element_enabled(self, selector):
        element = self.find_element(selector)
        if element and element.is_enabled():
            return element
        else:
            return False

    def check_data_attr_value(self, selector, data_attr_value):
        element = self.find_element(selector)
        if element:
            if element.get_attribute("data-attr-value") == data_attr_value:
                return True
            else:
                assert False, f"Couldn't find data-attr-value {data_attr_value} in {selector}."
        else:
            assert False, f"No element."

    def find_element(self, selector, retries=2):
        element = None
        if "css:" == selector[0:4]:
            element = self.find_element_via_css(selector.lstrip("css:"))
        elif "id:" == selector[0:3]:
            element = self.find_element_via_id(selector.lstrip("id:"))
        elif "xpath:" == selector[0:6]:
            element = self.find_element_via_xpath(selector.lstrip("xpath:"))
        elif "dataqa:" == selector[0:7]:
            element = self.find_element(f'xpath://*[@data-qa="{selector.replace("dataqa:", "")}"]')
        elif "name:" == selector[0:5]:
            element = self.find_element_via_name(selector.lstrip("name:"))
        elif "accessibility:" == selector[0:14]:
            element = self.find_element_via_accessibility(selector[14:])
        elif "tagname:" == selector[0:8]:
            element = self.find_element_via_tag_name(selector.lstrip("tagname:"))
        else:
            assert False, f"find element supports css, id, name and xpath.  {selector} doesn't state any one of those."
        if not element:
            if retries > 0:
                time.sleep(5)
                element = self.find_element(selector, retries-1)
            else:
                assert False, f"find element failed on {selector} unable to find element."
        return element

    def find_elements(self, selector, retries=2):
        if "css:" == selector[0:4]:
            elements = self.find_elements_via_css(selector.lstrip("css:"))
        elif "id:" == selector[0:3]:
            elements = self.find_elements_via_id(selector.lstrip("id:"))
        elif "xpath:" == selector[0:6]:
            elements = self.find_elements_via_xpath(selector.lstrip("xpath:"))
        elif "name:" == selector[0:5]:
            elements = self.find_elements_via_name(selector.lstrip("name:"))
        elif "accessibility:" == selector[0:14]:
            elements = self.find_elements_via_accessibility(selector[14:])
        else:
            assert False, f"find element supports css, id, name and xpath.  {selector} doesn't state any one of those."
        if not len(elements):
            if retries > 0:
                time.sleep(5)
                elements = self.find_elements(selector, retries-1)
            else:
                assert False, f"find elements failed on {selector} unable to find elements."
        return elements

    def find_element_via_name(self, selector, tries=10):
        logging.debug(f"trying to locate name '{selector}' selector")
        e = None
        try:
            e = self.driver.find_element_by_name(selector)
        except:
            self.dump_source()
        return e

    def find_element_via_accessibility(self, selector, tries=10):
        logging.debug(f"trying to locate name '{selector}' selector")
        e = None
        try:
            e = self.driver.find_element_by_accessibility_id(selector)
        except:
            self.dump_source()
        return e

    def find_element_via_css(self, selector):
        e = None
        try:
            e = self.driver.find_element_by_css_selector(selector)
            logging.debug(f"succeeded to locate css '{selector}' selector")
        except:
            self.dump_source()
            logging.debug(f"failed to locate css '{selector}' selector")
        return e

    def find_element_via_tag_name(self,selector):
        e= None
        try:
            e=self.driver.find_element_by_tag_name(selector)
            logging.debug(f"succeeded  to locate tagname '{selector}' selector")
        except:
            self.dump_source()
            logging.debug(f"failed to locate tagname '{selector}' selector")
        return e

    def find_element_via_id(self, selector):
        logging.debug(f"trying to locate id '{selector}' selector")
        e = None
        try:
            e = self.driver.find_element_by_id(selector)
        except:
            self.dump_source()
        return e

    def find_element_via_xpath(self, selector):
        logging.debug(f"trying to locate xpath '{selector}' selector")
        e = None
        try:
            e = self.driver.find_element_by_xpath(selector)
        except:
            self.dump_source()
        return e

    def find_elements_via_name(self, selector, tries=10):
        logging.debug(f"trying to locate name '{selector}' selector")
        e = []
        try:
            e = self.driver.find_elements_by_name(selector)
        except:
            self.dump_source()
        return e

    def find_elements_via_accessibility(self, selector, tries=10):
        logging.debug(f"trying to locate name '{selector}' selector")
        e = []
        try:
            e = self.driver.find_elements_by_accessibility_id(selector)
        except:
            self.dump_source()
        return e

    def find_elements_via_css(self, selector):
        e = []
        try:
            e = self.driver.find_elements_by_css_selector(selector)
            logging.debug(f"succeeded to locate css '{selector}' selector")
        except:
            self.dump_source()
            logging.debug(f"failed to locate css '{selector}' selector")
        return e

    def find_elements_via_id(self, selector):
        logging.debug(f"trying to locate id '{selector}' selector")
        e = []
        try:
            e = self.driver.find_elements_by_id(selector)
        except:
            self.dump_source()
        return e

    def find_elements_via_xpath(self, selector):
        logging.debug(f"trying to locate xpath '{selector}' selector")
        e = []
        try:
            e = self.driver.find_elements_by_xpath(selector)
        except:
            self.dump_source()
        return e

    def find_no_element(self, selector, retries=2):
        element = None
        if "css:" == selector[0:4]:
            element = self.find_element_via_css(selector.lstrip("css:"))
        elif "id:" == selector[0:3]:
            element = self.find_element_via_id(selector.lstrip("id:"))
        elif "xpath:" == selector[0:6]:
            element = self.find_element_via_xpath(selector.lstrip("xpath:"))
        elif "dataqa:" == selector[0:7]:
            element = self.find_element_via_xpath(f'xpath://*[@data-qa="{selector.replace("dataqa:", "")}"]')
        elif "name:" == selector[0:5]:
            element = self.find_element_via_name(selector.lstrip("name:"))
        elif "accessibility:" == selector[0:14]:
            element = self.find_element_via_accessibility(selector[14:])
        else:
            return False
        if not element:
            if retries > 0:
                time.sleep(5)
                element = self.find_no_element(selector, retries-1)
            else:
                return False
        return element

    def close(self):
        pass

    def capture_screenshot_to_file(self, filename):
        directories = '/'

        # If filename has / get a string with the path to the directory
        # e.g. b2b/registration/myfile -> /b2b/registration/
        if (filename.count('/') > 0):
            directories = filename.split('/')
            directories = directories[:-1]
            directories = '/' + '/'.join(directories) + '/'

        if not os.path.isdir(os.getcwd() + "/results/screenshots" + directories):
            os.makedirs(os.getcwd() + "/results/screenshots" + directories)
        save_path = os.getcwd() + "/results/screenshots/" + filename + ".png"
        logging.debug(save_path)

        self.driver.save_screenshot(save_path)

    def upload_screenshot(self, filename):
        saved_path = os.getcwd() + "/results/screenshots/" + filename + ".png"
        files = {"file": open(saved_path, "rb")}
        url = "https://ta-screenshots.parknowtech.net/api/upload/key"
        rq = requests.request(
            "POST", url,
            files=files
        )
        if rq.status_code < 400:
            logging.debug(f"upload of {saved_path} successful")
            return_uuid = json.loads(rq.content)["id"]
        else:
            logging.debug(f"upload of {saved_path} failed")
            return_uuid = "00000000-0000-0000-00000000000000000"

        return return_uuid

    def populate_element_object(self, element_name, selector):
        try:
            e = self.find_element(selector)
        except:
            e = None

        if e:
            self.object_data[self.session][element_name] = {
                "exists": True,
                "id": e.id,
                "text": e.text,
                "is_displayed": e.is_displayed(),
                "is_enabled": e.is_enabled(),
                "is_selected": e.is_selected()
            }
            try:
                self.object_data[self.session][element_name]['value'] = e.get_property('value')
                self.object_data[self.session][element_name]['type'] = e.get_property('type')
                self.object_data[self.session][element_name]['title'] = e.get_property('title')
                self.object_data[self.session][element_name]['class'] = e.get_property('class')
                self.object_data[self.session][element_name]['checked'] = e.get_property('checked')
            except:
                pass
        else:
            self.object_data[self.session][element_name] = {
                "exists": False
            }

        logging.debug(self.object_data[self.session][element_name])

    def select_value(self, value, selector):
        select = Select(self.find_element(selector))
        select.select_by_visible_text(value)

    def type_into(self, selector, text):
        element = self.find_element(selector)
        element.clear()
        logging.debug(f"entering string '{text}'")
        element.send_keys(text)
    
    def clear_text(self, selector):
        element = self.find_element(selector)
        element.clear()
        logging.debug(f"text is cleared/erased'")

    def set_value_into(self, selector, text):
        element = self.find_element(selector)
        element.click()
        element.clear()
        logging.debug(f"entering string '{text}'")
        element.set_value(text)

    def log_source(self):
        logging.debug(self.driver.page_source)

    def dump_source(self):
        f = open("./pagesource.xml", "w")
        f.write(self.driver.page_source)
        f.close
        return

    def capture_wireframe_to_file(self, filename):
        elements = self.driver.find_elements_by_xpath("//body//*")
        draw_elements = []
        max_width = 0
        max_height = 0
        for element in elements:
            if sum((element.size['height'], element.size['width'])) > 0:
                draw_elements.append((
                    (
                        element.location['x'],
                        element.location['y']
                    ),
                    (
                        element.location['x'] + element.size['width'],
                        element.location['y'] + element.size['height']
                    )
                ))
                if element.location['x'] + element.size['width'] > max_width:
                    max_width = element.location['x'] + element.size['width']
                if element.location['y'] + element.size['height'] > max_height:
                    max_height = element.location['y'] + element.size['height']

        wireframe = Image.new('RGBA', (max_width, max_height), (255,255,255,0))

        draw = ImageDraw.Draw(wireframe)
        for wire in draw_elements:
            draw.rectangle(wire, fill=None, outline=(255,0,0,255), width=2)

        wireframe.save(os.getcwd() + "/results/screenshots/" + filename + ".png", "PNG")

class AppiumObject(Ui):

    def __init__(self, session, config_string, driver_provider):
        self.driver_provider = driver_provider
        self.platform_name = None
        super().__init__(session, config_string)

    def start_driver(self):
        logging.debug(os.getcwd())
        self.desired_caps = self.connection_json
        self.platform_name = self.desired_caps['platformName']
        if self.driver_provider == "local":
            self.driver = appiumwebdriver.Remote(
                command_executor="http://host.docker.internal:4723/wd/hub",
                desired_capabilities=self.desired_caps
            )
        elif self.driver_provider == "testobject":
            self.desired_caps['testobject_api_key'] = os.environ["SAUCE_KEY"]
            self.desired_caps['testobject_app_id'] = os.environ["SAUCE_APP_VERSION_KEY_ANDROID"]
            self.start_sauce_driver()
        self.driver.implicitly_wait(5)

        super().start_driver()
        self.get_driver()
        session_id = self.driver.session_id
        logging.debug(f'Appium session id is {session_id}')

        if self.driver_provider != "local":
            testobject_test_live_view_url = self.driver.desired_capabilities[
                'testobject_test_live_view_url']
            testobject_test_report_url = self.driver.desired_capabilities[
                'testobject_test_report_url']
            logging.debug(f'Live web url is {testobject_test_live_view_url}')
            logging.debug(f'Test report link is {testobject_test_report_url}')

    def get_driver(self):
        return self.driver

    def compare_text_of_element(self, selector, attribute, element_text):
        text_from_locator = self.find_element(selector).get_attribute(""+attribute)
        logging.debug(f"Text from locator {text_from_locator.lstrip()}")
        logging.debug(f"Element text is {element_text.lstrip()}")
        return text_from_locator.replace(" ", "") == element_text.replace(" ", "")

    def start_sauce_driver(self):
        EU_endpoint = 'http://eu1.appium.testobject.com/wd/hub'
        self.driver = appiumwebdriver.Remote(EU_endpoint, self.desired_caps)

    # Some additional implementation might be needed to make it work on Saucelabs
    def hide_keyboard(self, retries=5):
        if self.platform_name == 'iOS':
            number_of_elements = len(self.driver.find_elements_by_xpath(
                "//XCUIElementTypeButton[@name='Done']"))
            if number_of_elements == 1:
                self.driver.find_element_by_xpath(
                    "//XCUIElementTypeButton[@name='Done']").click()
        elif self.driver.is_keyboard_shown():
            if retries > 0:
                self.driver.hide_keyboard()
                time.sleep(2)
                self.hide_keyboard(retries-1)
            else:
                assert False, f"find keyboard fails"

    def close(self):
        self.driver.close_app()
        self.driver.quit()

    def set_geo_location(self, long, lat):
        self.driver.set_location(float(long), float(lat), 10)


class SeleniumObject(Ui):

    def __init__(self, session, config_string):
        connection_json = json.loads(config_string)
        self.browser_type = connection_json['browser']
        super().__init__(session, config_string)

    def start_driver(self):
        logging.debug(os.getcwd())
        if self.browser_type == "chrome-headless":
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.add_argument("--remote-debugging-address=0.0.0.0")

            prefs = {'download.default_directory': "/home/mydemo/framework/temp/",
                     'download.prompt_for_download': False,
                     'download.directory_upgrade': True,
                     'safebrowsing.enabled': False,
                     'safebrowsing.disable_download_protection': True}
            chrome_options.add_experimental_option('prefs', prefs)
            # self.driver = webdriver.Chrome(os.getcwd() + "/tools/chromedriver", chrome_options=chrome_options)
            self.driver = webdriver.Chrome(
                "/usr/local/bin/chromedriver", chrome_options=chrome_options)
            self.driver.set_window_size(1680, 1773)
            self.enable_download_in_headless_chrome(
                self.driver, "/home/mydemo/framework/temp/")
            self.driver.implicitly_wait(15)
        if self.browser_type == "firefox-headless":
            firefox_options = FirefoxOptions()
            firefox_options.headless = True
            self.driver = webdriver.Firefox(
                options=firefox_options, executable_path='/usr/bin/firefox')
            self.driver.set_window_size(1680, 1773)
            self.driver.implicitly_wait(15)
        if self.browser_type == "standalone-chrome":
            if "DOCKER" in os.environ:
                hostname = "host.docker.internal"
            else:
                hostname = "localhost"
            hub_url = f'http://{hostname}:4444/wd/hub'

            rq = requests.get(url=hub_url, timeout=2)
            assert rq.status_code==200, "Selenium not available"

            chrome_options = ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.add_argument("--remote-debugging-address=0.0.0.0")

            self.driver = webdriver.Remote(hub_url, desired_capabilities=webdriver.DesiredCapabilities.CHROME, options=chrome_options)
            self.driver.set_window_size(1680, 1773)
            self.driver.implicitly_wait(15)
        self.isclosed=False
        super().start_driver()

    def get(self, url):
        logging.debug(f"navigate to: {url}")
        self.driver.get(url)

    def set_name(self, element_name, name_attribute):
        logging.debug(
            f"setting name {name_attribute} for iframe with selector: {element_name}")
        element = self.find_element(element_name)
        self.driver.execute_script(
            "arguments[0].setAttribute(arguments[1], arguments[2]);",
            element,
            "name",
            name_attribute
        )

    def switch_to_window(self, window_index):
        logging.debug(f"switching to window index: {window_index}")

        self.driver.switch_to.window(self.driver.window_handles[int(window_index)])

    def switch_to_frame(self, frame_name):
        logging.debug(f"switching to: {frame_name}")
        if frame_name == "default":
            self.driver.switch_to_default_content()
        elif "index:" in frame_name:
            frame_index = int(frame_name.lstrip("index:"))
            self.driver.switch_to.frame(frame_index)
        else:
            self.driver.switch_to_frame(frame_name)
            # logging.debug(self.driver.page_source)

    def wait_url_change(self, duration, url):
        duration = int(duration)

        if duration > 0:
            if url in self.driver.current_url:
                return
            else:
                # If the URL we are waiting for does not partialy match the current page url
                # wait 1 second then recurse
                logging.debug(
                    f"waiting for url to change for {duration} more seconds")

                time.sleep(1)

                self.wait_url_change(duration - 1, url)
        else:
            # If the current page url has not changed in the given duration
            # we fail the test so its obvious the page was never updated
            # and we waiting forever if a URL has gone down etc
            self.dump_source()
            assert False, f"url did not change to {url}."
            return

    def hover_over(self, selector):
        actions = ActionChains(self.driver)
        actions.move_to_element(self.find_element(selector))
        actions.perform()

    def compare_text(self, element_text, selector, element_attribute):
        e = self.find_element(selector)
        if element_attribute == "text":
            text_from_locator = e.text
        elif element_attribute == "value":
            text_from_locator = e.get_attribute("value")
        elif element_attribute == "innerHTML":
            text_from_locator = e.get_attribute("innerHTML")
        logging.debug(f"Text from locator {text_from_locator.lstrip()}")
        logging.debug(f"Element text is {element_text.lstrip()}")
        return text_from_locator.replace(" ", "").lower() == element_text.replace(" ", "").lower()
    
    def is_disabled(self, selector):
        e = self.find_element(selector)

        text_from_locator = e.get_property("disabled")

        return text_from_locator

    def enable_download_in_headless_chrome(self, driver, download_dir):
        """
        there is currently a "feature" in chrome where
        headless does not allow file download: https://bugs.chromium.org/p/chromium/issues/detail?id=696481
        This method is a hacky work-around until the official chromedriver support for this.
        Requires chrome version 62.0.3196.0 or above.
        """

        # add missing support for chrome "send_command"  to selenium webdriver
        driver.command_executor._commands["send_command"] = (
            "POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {
            'behavior': 'allow', 'downloadPath': download_dir}}
        command_result = driver.execute("send_command", params)
        print("response from browser:")
        for key in command_result:
            print("result:" + key + ":" + str(command_result[key]))

    def dismiss_native_popup(self, acceptordecline):
        alert = self.driver.switch_to_alert()
        if acceptordecline == "accept":
            alert.accept()
        else:
            alert.dismiss()    
    
    def scroll_to_selected_element(self, selector):
        element_to_scroll_to = self.find_element(selector)
        actions = ActionChains(self.driver)
        actions.move_to_element(element_to_scroll_to).perform()

    def close(self):
        if not self.isclosed:
            self.driver.close()
            self.isclosed=True
