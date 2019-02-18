FROM alpine

RUN apk --no-cache add python3 certbot \
    && pip3 install --upgrade pip \
    && pip3 install boto3 certbot-dns-route53 pyopenssl

#    && apk --no-cache add --virtual deps gcc musl-dev linux-headers python3-dev \
#    && apk del deps

WORKDIR /usr/src/app

COPY src .

CMD python3 update.py
