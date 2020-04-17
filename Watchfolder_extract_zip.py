import boto3
import io
import json
import zipfile


def lambda_handler(event, context):
    
    s3 = boto3.client('s3')
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    FileObj = s3.get_object(Bucket=bucket, Key=key)
    buff = io.BytesIO(FileObj["Body"].read())

    zipf = zipfile.ZipFile(buff, mode='r')
    for file in zipf.infolist():
        fileName = file.filename
        putFile = s3.put_object(Bucket=bucket, Key="zipoutput/{}".format(fileName), Body=zipf.read(file))

    s3.delete_object(Bucket=bucket, Key=key)

    return {
        "statusCode": 200,
        "body": json.dumps('Unzip file is completed!')
    }
