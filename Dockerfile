ARG BUILD_FROM
FROM $BUILD_FROM

# install python
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# copy project files and run.sh file
COPY . /
COPY run.sh /

RUN pip install -r requirements.txt

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]