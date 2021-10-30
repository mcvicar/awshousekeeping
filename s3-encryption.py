#!/usr/bin/python

import boto3
from botocore.exceptions import ClientError
import argparse
from pprint import pprint
from datetime import datetime

class bcolors:
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'

arguments = argparse.ArgumentParser()
arguments.add_argument(
  'profile',
  help="BOTO Profile")

arguments.add_argument(
  '--region',
  default=False,
  help="AWS Region")

args = arguments.parse_args()

if args.region:
  session = boto3.Session(profile_name=args.profile,region_name=args.region)
else:
  session = boto3.Session(profile_name=args.profile)

print ("S3 Buckets at %s" % datetime.now())
s3 = session.client('s3');

def getAllBuckets():
  try:
    response = s3.list_buckets()
    for bucket in response['Buckets']:
      bucket_name = bucket['Name']
      print (bucket_name)
      getBucketEncryption(bucket_name)
  except ClientError as e:
    print(bcolors.FAIL + "No buckets exist? " + e + bcolors.ENDC)
  return

def getBucketEncryption(bucket_name):
    try:
        enc = s3.get_bucket_encryption(Bucket=bucket_name)
        rules = enc['ServerSideEncryptionConfiguration']['Rules']
        formatEncryptionRule(rules)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
            print(bcolors.FAIL +'No server-side encryption' + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "unexpected error: %s" % (e)  + bcolors.ENDC)

def formatEncryptionRule(rules):
    for rule in rules:
        print(bcolors.OKGREEN + " * " + rule["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"] + bcolors.ENDC)
        if rule["BucketKeyEnabled"] == "True":
            print(bcolors.OKBLUE + " * BucketKeyEnabled: " + str(rule["BucketKeyEnabled"]) + bcolors.ENDC)
        else:
            print(bcolors.FAIL + " * BucketKeyEnabled: " + str(rule["BucketKeyEnabled"]) + bcolors.ENDC)
    return

getAllBuckets()
