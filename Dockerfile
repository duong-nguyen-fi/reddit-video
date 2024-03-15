FROM python:3.10.9-slim

ARG UNAME=andy
ARG UID=1003
ARG GID=1004
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME


RUN apt update
RUN apt-get install -y ffmpeg
RUN apt install python3-pip -y


ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m playwright install
RUN python -m playwright install-deps

RUN mkdir /app
ADD . /app
WORKDIR /app
RUN chmod 755 /app
RUN chown andy:andy /app
#RUN rm config.toml && cp config_default.toml config.toml
# tricks for pytube : https://github.com/elebumm/RedditVideoMakerBot/issues/142 
# (NOTE : This is no longer useful since pytube was removed from the dependencies)
# RUN sed -i 's/re.compile(r"^\\w+\\W")/re.compile(r"^\\$*\\w+\\W")/' /usr/local/lib/python3.8/dist-packages/pytube/cipher.py
USER $UNAME
CMD ["python3", "main.py"]
