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
db = boto3.resource('dynamodb')
db_client = boto3.client('dynamodb')
logging.info('Boto3 initialized.')

# load variables
try:
    access = os.environ['AWS_ACCESS_KEY_ID']
    secret = os.environ['AWS_SECRET_ACCESS_KEY']
    logging.info('Credentials loaded.')
except KeyError:
    logging.error("Access/secret variables not set.", file=sys.stderr)
    exit(1)

# if table does not exist, create it
try:
    certificates = db.Table('certificates')
    certificates.item_count
    logging.info('Credentials table loaded.')
except db.meta.client.exceptions.ResourceNotFoundException:
    logging.info('Credentials table does not exist, creating it.')
    certificates = db.create_table(
            TableName='certificates',
            KeySchema=[ { 'AttributeName': 'type', 'KeyType': 'HASH' } ], 
            AttributeDefinitions=[ { 'AttributeName': 'type', 'AttributeType': 'S' } ],
            ProvisionedThroughput={ 'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1 }
    )
    certificates.meta.client.get_waiter('table_exists').wait(TableName='certificates')
    logging.info('Credentials table created.')

print(certificates.item_count)
