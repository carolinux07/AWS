import json
import boto3
import os
from urllib.parse import unquote_plus


def lambda_handler(event, context):
        
    s3 = boto3.client('s3')
    client = boto3.client('textract')
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    document = unquote_plus(event['Records'][0]['s3']['object']['key'])
    key = event['Records'][0]['s3']['object']['key']

    response = client.detect_document_text(
    Document={'S3Object': {'Bucket': bucket, 'Name': document}})

    lines = []
    for detection in response['Blocks']:
        if detection['BlockType'] == 'LINE':
            #if 'PROD:' in detection['Text']:
            print("DetectedText: ", detection['Text'])
            lines.append(detection['Text'])
            
    with open("/tmp/object.json", "w") as data:
        json.dump(lines, data, indent=1)
    
    key = 'zipresultado/' + key.split("/")[-1].replace(".jpg","").replace(".JPG","") + '.txt'
    s3.upload_file("/tmp/object.json", bucket, key)        
    
    s3.delete_object(Bucket=bucket, Key=document)
