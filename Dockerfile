ARG BUILD_FROM
FROM $BUILD_FROM

# copy project files and run.sh file
COPY . /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]