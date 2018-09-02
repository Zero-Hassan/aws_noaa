import boto3
import botocore

bucket = 'noaa-gfs-pds'
client = boto3.client('s3', config=botocore.client.Config(signature_version=botocore.UNSIGNED))


paginator = client.get_paginator('list_objects')
result = paginator.paginate(Bucket=bucket, Delimiter='/')

for prefix in result.search('CommonPrefixes'):
    prefixString = prefix.get('Prefix')
    print(prefixString)

variable = raw_input("Enter variable name to see files: ")
response = client.list_objects_v2(Bucket=bucket, Prefix=variable+"/")
response_meta = response.get('ResponseMetadata')

if response_meta.get('HTTPStatusCode') == 200:
    contents = response.get('Contents')
    if contents != None:
        for obj in contents:
            print(obj.get('Key'))

file_key = raw_input("Enter file name to download: ")
file_name = raw_input("local [Path]/name to save file: ")
client.download_file(bucket, file_key,file_name)
