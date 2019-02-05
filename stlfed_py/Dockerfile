FROM python:3.7-stretch

COPY . /root
WORKDIR /root

# Dummy README to .dockerignore real one on changes
RUN touch README.md \
    && pip3 install .

CMD ["fcast-listen"]
