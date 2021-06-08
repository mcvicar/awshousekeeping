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
      getBucketLifeCycle(bucket_name)
  except ClientError as e:
    print(bcolors.FAIL + "No buckets exist? " + e + bcolors.ENDC)
  return

def getBucketLifeCycle(bucket_name):
    try:
      bucket_lifecycle = s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
      formatLifeCycleRule(bucket_lifecycle['Rules'])
    except ClientError as e:
      if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
          print(bcolors.FAIL + " No lifecycle configuration applied... " + bcolors.ENDC)
          return []
      else:
          print("No rules exist? " + e.response)
          return
    return

def formatLifeCycleRule(rules):
    for rule in rules:
        print(bcolors.OKBLUE + " * " + rule["ID"] + bcolors.ENDC)
        if rule["Status"] == "Enabled":
            print(bcolors.OKBLUE + " * " + rule["Status"] + bcolors.ENDC)
        else:
            print(bcolors.FAIL + " * " + rule["Status"] + bcolors.ENDC)
        print(bcolors.OKBLUE + " * " + str(rule["NoncurrentVersionExpiration"]["NoncurrentDays"]) + " days" +bcolors.ENDC)
    return


getAllBuckets()
