# awshousekeeping
Some basic scripts to keep the AWS account clean and tidy

## S3 Lifecycles
List out all your buskets and check they have a lifecycle attached to them...
`python s3-lifecycles.py --region eu-west-1 profile`

## S3 Encryption
List out all your buskets and check they have a encryption applied to them...
`python s3-encryption.py --region eu-west-1 profile`

## Install
Have python3 and boto3 installed
