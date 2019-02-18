import OpenSSL
import boto3
import logging
import os
import ssl, socket
import subprocess
import sys
from datetime import datetime

#
# globals
#
ssm = boto3.client('ssm')

#
# setup logs
#
logging.basicConfig(
    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

#
# get domain
#
try:
    domain   = os.environ['DOMAIN']
    mail     = os.environ['MAIL']
    basename = os.environ['BASENAME']
except KeyError:
    logging.error('Environment variable DOMAIN or MAIL not found.')
    sys.exit(1)

#
# procedure to create new certificate
#
def create_new_certificate():
    subprocess.run([
        'certbot', 'certonly',
        #'--dry-run',
        '-d', domain, '-d', '*.' + domain,
        '--dns-route53',
        '-m', mail,
        '--agree-tos',
        '--non-interactive',
        '--server', 'https://acme-v02.api.letsencrypt.org/directory'
    ])
    logging.info('SSL credential generated. Now reading from files...')
    with open('/etc/letsencrypt/live/' + domain + '/privkey.pem', 'r') as f:
        ssl_privkey = f.read().strip()
    with open('/etc/letsencrypt/live/' + domain + '/fullchain.pem', 'r') as f:
        ssl_fullchain = f.read().strip()
    with open('/etc/letsencrypt/live/' + domain + '/cert.pem', 'r') as f:
        ssl_cert = f.read().strip()
    with open('/etc/letsencrypt/live/' + domain + '/chain.pem', 'r') as f:
        ssl_chain = f.read().strip()
    logging.info('Files read, now storing in SSM...')
    ssm.put_parameter(
        Name='ssl_privkey',
        Description='Description',
        Value=ssl_privkey,
        Type='SecureString',
        KeyId='alias/ssm_store',
        Overwrite=True
    )
    ssm.put_parameter(
        Name='ssl_fullchain',
        Description='Description',
        Value=ssl_fullchain,
        Type='SecureString',
        KeyId='alias/ssm_store',
        Overwrite=True
    )
    ssm.put_parameter(
        Name='ssl_cert',
        Description='Description',
        Value=ssl_cert,
        Type='SecureString',
        KeyId='alias/ssm_store',
        Overwrite=True
    )
    ssm.put_parameter(
        Name='ssl_chain',
        Description='Description',
        Value=ssl_chain,
        Type='SecureString',
        KeyId='alias/ssm_store',
        Overwrite=True
    )
    logging.info('Done.')

# restart service
for env in ("devl", "master"):
    subprocess.run([
        "aws", "ecs", "update-service", "--force-new-deployment",
        "--cluster", os.environ['BASENAME'] + "-" + env,
        "--service", "backend-service"
    ])
    logging.info('Service backend-service at cluster ' + os.environ['BASENAME'] + "-" + env + ' restarted.')

#
# load parameter values
#
try:
    ssm.get_parameter(Name='ssl_fullchain', WithDecryption=True)['Parameter']['Value']
    ssm.get_parameter(Name='ssl_privkey', WithDecryption=True)['Parameter']['Value']
    ssm.get_parameter(Name='ssl_cert', WithDecryption=True)['Parameter']['Value']
    ssm.get_parameter(Name='ssl_chain', WithDecryption=True)['Parameter']['Value']
    logging.info('SSL credential parameters found.')
except ssm.exceptions.ParameterNotFound:
    logging.info('SSL credential parameters not found. Requesting certificate from Let\'s Encrypt...')
    create_new_certificate()

#
# calculate expiration date
#
try:
    expiration_date = ssm.get_parameter(Name='ssl_expiration_date', WithDecryption=True)['Parameter']['Value']
except ssm.exceptions.ParameterNotFound:
    ssl_fullchain = ssm.get_parameter(Name='ssl_fullchain', WithDecryption=True)['Parameter']['Value']
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, ssl_fullchain)
    expiration_date = datetime.strptime(x509.get_notAfter().decode('latin1'),'%Y%m%d%H%M%SZ')
logging.info('Expiration date is ' + str(expiration_date) + '.')

if (expiration_date - datetime.now()).days <= 5:
    logging.info('Less than 5 days to expire certificate. Renewing it...')
    create_new_certificate()
