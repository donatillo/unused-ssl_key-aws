import boto3
import logging
import os
import subprocess
import sys

# setup logs
logging.basicConfig(
    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

# get domain
try:
    domain = os.environ['DOMAIN']
    mail   = os.environ['MAIL']
except KeyError:
    logging.error('Environment variable DOMAIN or MAIL not found.')
    os.exit(1)

# globals
ssm = boto3.client('ssm')

# load parameter values
try:
    ssl_fullchain  = ssm.get_parameter(Name='ssl_fullchain', WithDecryption=True)['Parameter']['Value']
    ssl_privkey    = ssm.get_parameter(Name='ssl_privkey', WithDecryption=True)['Parameter']['Value']
    ssl_cert       = ssm.get_parameter(Name='ssl_cert', WithDecryption=True)['Parameter']['Value']
    ssl_chain      = ssm.get_parameter(Name='ssl_chain', WithDecryption=True)['Parameter']['Value']
    ssl_expiration = ssm.get_parameter(Name='ssl_expiration', WithDecryption=True)['Parameter']['Value']
    #logging.info('SSL credential parameters found and loaded. Certificate expiration date: ' + ssl_expiration)
except ssm.exceptions.ParameterNotFound:
    logging.info('SSL credential parameters not found. Requesting certificate from Let\'s Encrypt...')
    subprocess.run([
        'certbot', 'certonly',
        '--dry-run',
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
