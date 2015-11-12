import boto3
import os
import sys
import uuid
import gzip
import json

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = '/tmp/{}'.format(uuid.uuid4())

        print bucket
        print key
        print download_path
        s3 = boto3.resource('s3')
        s3.meta.client.download_file(Bucket=bucket, Key=key, Filename=download_path)
        with gzip.open(download_path, 'rb') as filestream:
            for line in filestream:
                records = json.loads(line)
                print records
                for record in records['Records']:
                    print record
                    if record['eventSource'] == 'ec2.amazonaws.com':
                        print "*** Matching Record ***"
                        print record