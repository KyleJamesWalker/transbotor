FROM python:3.5.1-alpine

# Install Dependencies
RUN apk add --update \
        cyrus-sasl-dev \
        g++ \
        gcc \
        git \
        libgcc \
        musl-dev \
    && \
    apk upgrade && \
    rm -rf /var/cache/apk/*

WORKDIR /home

COPY requirements.txt /home/
RUN pip install -r requirements.txt

COPY . /home

ENTRYPOINT ["python3", "-m", "transbotor"]
