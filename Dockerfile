FROM alpine

RUN apk --no-cache add python3 certbot \
    && apk add aws-cli --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ --allow-untrusted \
    && pip3 install --upgrade pip \
    && pip3 install boto3 certbot-dns-route53 pyopenssl

WORKDIR /usr/src/app

COPY src .

CMD python3 update.py
