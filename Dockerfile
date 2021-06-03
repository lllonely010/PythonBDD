FROM ubuntu:20.04

ARG USERNAME=mydemo
ARG UID=1000
ARG GID=$UID
ENV HOME /home/$USERNAME

RUN addgroup \
  --gid=$GID \
  $USERNAME

RUN adduser \
  --disabled-password \
  --gecos "" \
  --ingroup "$USERNAME" \
  --uid "$UID" \
  "$USERNAME"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
  apt-get install -y\
  gnupg \
  apt-transport-https \
  debconf-utils \
  curl \
  wget \
  net-tools \
  python-dev \
  libxml2-dev \
  libxslt1-dev \
  antiword \
  unrtf \
  poppler-utils \
  pstotext \
  tesseract-ocr \
  flac \
  ffmpeg \
  lame \
  libmad0 \
  libsox-fmt-mp3 \
  sox \
  libjpeg-dev \
  swig \
  libpulse-dev && \
  rm -rf /var/lib/apt/lists/*

# adding custom MS repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# apt-get and system utilities
RUN apt-get update && \
  ACCEPT_EULA=Y apt-get install -y \
  curl \
  wget \
  python3 \
  python3-pip \
  git \
  zip \
  wget \
  uuid-runtime \
  build-essential \
  zlib1g-dev \
  libffi-dev \
  libreadline-gplv2-dev \
  libncursesw5-dev \
  libssl-dev \
  libsqlite3-dev \
  tk-dev \
  libgdbm-dev \
  libc6-dev \
  libbz2-dev \
  unixodbc-dev \
  msodbcsql17 \
  mssql-tools \
  unixodbc \
  locales \
  && rm -rf /var/lib/apt/lists/*

RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"

# Install locale
RUN locale-gen en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8

RUN pip3 --no-cache-dir install flask==1.1.2 \
  && pip3 --no-cache-dir install certifi==2020.12.5 \
  && pip3 --no-cache-dir install chardet==4.0.0 \
  && pip3 --no-cache-dir install dotted==0.1.8 \
  && pip3 --no-cache-dir install Faker==6.6.3 \
  && pip3 --no-cache-dir install idna==3.1 \
  && pip3 --no-cache-dir install parse==1.19.0 \
  && pip3 --no-cache-dir install git+https://github.com/behave/behave@gherkin_v6 \
  && pip3 --no-cache-dir install parse-type==0.5.2 \
  && pip3 --no-cache-dir install python-dateutil==2.8.1 \
  && pip3 --no-cache-dir install regex==2021.3.17 \
  && pip3 --no-cache-dir install requests==2.25.1 \
  && pip3 --no-cache-dir install six==1.15.0 \
  && pip3 --no-cache-dir install text-unidecode==1.3 \
  && pip3 --no-cache-dir install urllib3==1.26.4 \
  && pip3 --no-cache-dir install pylint==2.7.2 \
  && pip3 --no-cache-dir install selenium==3.141.0 \
  && pip3 --no-cache-dir install pyodbc==4.0.30 \
  && pip3 --no-cache-dir install elasticsearch==7.12.0 \
  && pip3 --no-cache-dir install Pillow==8.1.2 \
  && pip3 --no-cache-dir install CMRESHandler==1.0.0 \
  && pip3 --no-cache-dir install mysql-connector-python==8.0.23 \
  && pip3 --no-cache-dir install pdfminer.six==20201018 \
  && pip3 --no-cache-dir install python-owasp-zap-v2.4 \
  && pip3 --no-cache-dir install Appium-Python-Client==1.1.0 \
  && pip3 --no-cache-dir install textract==1.6.3 \
  && pip3 --no-cache-dir install python-dateutil==2.8.1 \
  && pip3 --no-cache-dir install boto3==1.17.38 \
  && pip3 --no-cache-dir install awscli==1.19.38 \
  && pip3 --no-cache-dir install maya==0.6.1 \
  && pip3 --no-cache-dir install lxml==4.6.3 \
  && pip3 --no-cache-dir install boto3==1.17.38


COPY . /opt/mydemo
RUN chown -R $USERNAME:$USERNAME /opt/mydemo

USER $USERNAME
