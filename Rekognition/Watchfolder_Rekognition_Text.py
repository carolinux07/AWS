import boto3
import json
    

def move_frame(bucket, key, s3):
    
    # Step 1: copy frame from "output" to "processing2"
    destination_key = key.replace("output/", "processing2/")
    s3.copy_object(CopySource={"Bucket": bucket, "Key": key}, Bucket=bucket, Key=destination_key)
    
    # Step 2: delete photo from "output"
    s3.delete_object(Bucket=bucket, Key=key)
    
    # Return updated key for following functions
    return destination_key
    

def ask_rekognition_api_for_text(bucket, key, client):
    
    image = {"S3Object": {"Bucket": bucket, "Name": key}}
    
    # Ask the API for text in the frame
    response = client.detect_text(Image=image)
    
    lines = []
    for detection in response['TextDetections']:
        if detection['Type'] == 'LINE':
            print("DetectedText: ", detection['DetectedText'])
            lines.append(detection['DetectedText'])
    return lines
    
    
def send_json(bucket, key, lines, s3):

    with open("/tmp/object.json", "w") as data:
        json.dump(lines, data, indent=1)
    
    key = 'resultado/' + key.split("/")[-1].replace(".jpg","").replace(".JPG","") + '.txt'

    s3.upload_file("/tmp/object.json", bucket, key)

    return key
    

def delete_frame(bucket, key, s3):
    
    # Step 1: delete frame from "processing2"
    s3.delete_object(Bucket=bucket, Key=key)

    # Nothing to return here
    return None
    

def lambda_handler(event, context):

    s3 = boto3.client('s3')
    client = boto3.client("rekognition")
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
   
    key = move_frame(bucket, key, s3)
    lines = ask_rekognition_api_for_text(bucket, key, client)
    path = send_json(bucket, key, lines, s3)
    delete_frame(bucket, key, s3)
    
    return {"statusCode": 200, "body": json.dumps(key)}
