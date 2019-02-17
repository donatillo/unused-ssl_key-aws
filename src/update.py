import boto3
import logging
import os
import sys

# setup logs
logging.basicConfig(
    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

# globals
ssm = boto3.client('ssm')

# create parameter
ssm.put_parameter(
        Name='hello2',
        Description='Description',
        Value='world3',
        Type='SecureString',
        KeyId='alias/ssm_store',
        Overwrite=True
)
logging.info('Parameter created.')

# read parameter
parameter = ssm.get_parameter(Name='hello2', WithDecryption=True)
print(parameter['Parameter']['Value'])
