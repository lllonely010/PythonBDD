import requests
from requests.adapters import HTTPAdapter
import json
import logging
import subprocess
from dotted.collection import DottedDict
from urllib3.util.retry import Retry


class RequestObject:

    def __init__(self, session):
        """A request object, made for calling APIs

        Parameters:
            session (str): The name of this object
        """
        self.session = session
        self.request = requests.Session()
        self.timeout = 20
        self.parameters = {}
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
            # "Accept-Language": "en-US,en;q=0.9"
        }
        self.object_data = {self.session: {}}
        self.auth = None
        self.allow_redirects = True
        self.proxies = {
            # "http": "http://192.168.201.24:8866/",
            # "https": "https://192.168.201.24:8866/"
        }

    def adjust_http_proxy(self, hostname, port):
        self.proxies["http"] = "http://" + hostname + ":" + port + "/"

    def perform_request(self, method, url, filename=None, data=None, params=None, filepath=None):
        """Performs a request to a provided url

        Parameters:
            method (str): The chosen method (POST, PUT, GET, etc)
            url (str): The full url that's to be called including schema (http://www.google.com/)
            data (str): Json in string from, to be sent as the payload, or None if not required
        """
        try:
            params = json.loads(self.parameters)
        except:
            params = self.parameters
        if data:
            if data[0] == "$":
                data = json.loads(data[1:])

        if filepath:
            files = {'file': open(filepath, 'rb')}

        logging.info(f"request: {method} {url} headers: {self.headers} Params: {params} Payload: {data}")
        if filepath:
            content_type=""
            if filepath[filepath.rfind("."):]==".csv" :
                content_type="type=text/csv"
            elif filepath[filepath.rfind("."):]==".xlsx":
                content_type="type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            curl_str = f'curl -X POST "{url}" '
            for h in self.headers:
                curl_str += f'-H "{h}: {self.headers[h]}" '
            curl_str += f'-F "{filename}=@{filepath};{content_type}"'
            logging.debug(curl_str)
            output = subprocess.check_output(curl_str, shell=True)
            logging.debug(output)
            # self.request = requests.request(
            #     method, url,
            #     params=params, 
            #     headers=self.headers,
            #     auth=self.auth,
            #     files=files,
            #     proxies=self.proxies,
            #     timeout=self.timeout
            #     )
                
            self.object_data[self.session] = {
                "data": json.loads(output.decode("utf-8")),
                "statuscode": None
            }
        else:
            self.response = self.request.request(
                method, url,
                data=data,
                params=params, 
                headers=self.headers,
                auth=self.auth,
                proxies=self.proxies,
                timeout=self.timeout,
                allow_redirects=self.allow_redirects
                )
        
            self.object_data[self.session] = {
                "data": self.content(),
                "statuscode": self.response.status_code,
                "resp_headers": self.response.headers
            }
            if type(self.object_data[self.session]["resp_headers"]) is requests.structures.CaseInsensitiveDict:
                self.object_data[self.session]["resp_headers"] = DottedDict(self.object_data[self.session]["resp_headers"])

        logging.info(f"Response: {self.object_data}")

    def close(self):
        """Closes the request
        """
        if self.request:
            self.request.close()

    def set_retry_on(self):
        retry_strategy = Retry(
            total=5,
            backoff_factor=2,
            method_whitelist=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST", "PATCH"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.request.mount("https://", adapter)
        self.request.mount("http://", adapter)


    def set_allow_redirects(self, enabled):
        self.allow_redirects = enabled

    def add_basic_auth(self, username, password):
        """Adds basic auth to the request

        Parameters:
            username (str): The desired username
            password (str): The desired password
        """
        self.auth = (username, password)

    def add_headers(self, headers):
        """Adds a set of headers to the request

        Parameters:
            headers (dict): The dictionary of headers to add
        """
        for k in headers:
            self.headers[k] = headers[k]

    def add_parameters(self, parameters):
        """Adds a set of headers to the request

        Parameters:
            parameters (dict): The dictionary of parameters to add
        """
        logging.debug(f"adding params {parameters}")
        for k in parameters:
            self.parameters[k] = parameters[k]

    def status_code(self):
        """Returns the status code of the response

        Returns:
            String: The status code returned from the last response
        """
        return str(self.object_data[self.session]['statuscode'])

    def content(self):
        """Returns the body of the response

        Returns:
            String: The status code returned from the last request
        """
        try:
            return_value = json.loads(self.response.content.decode("utf-8"))
        except:
            return_value = self.response.content.decode("utf-8")
        if not return_value:
            return_value = "None"
        return return_value
