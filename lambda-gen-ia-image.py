import json
import boto3
import base64
import datetime

client_bedrock = boto3.client('bedrock-runtime')
client_s3 = boto3.client('s3')

def lambda_handler(event, context):
    print(input_prompt)
    input_prompt=event['prompt']
    print(input_prompt)

    response_bedrock = client_bedrock.invoke_model( contentType='application/json',
                                                    accept='application/json',
                                                    modelId='amazon.titan-image-generator-v2:0',
                                                    body=json.dumps({"textToImageParams":{"text":input_prompt},"taskType":"TEXT_IMAGE","imageGenerationConfig":{"cfgScale":8,"seed":42,"quality":"standard","width":512,"height":512,"numberOfImages":1}}))

    print(response_bedrock)   
       
    response_bedrock_byte=json.loads(response_bedrock['body'].read())
    print(response_bedrock_byte)

    response_bedrock_base64 = response_bedrock_byte['images'][0]
    response_bedrock_finalimage = base64.b64decode(response_bedrock_base64)
    print(response_bedrock_finalimage)
    
    poster_name = 'image_name'+ datetime.datetime.today().strftime('%Y-%M-%D-%M-%S')
    
    response_s3=client_s3.put_object(
        Bucket='908671954593-image-eliezer-us-east-1',
        Body=response_bedrock_finalimage,
        Key=poster_name)

    generate_presigned_url = client_s3.generate_presigned_url('get_object', Params={'Bucket':'908671954593-image-eliezer-us-east-1','Key':poster_name}, ExpiresIn=3600)
    print(generate_presigned_url)
    return {
        'statusCode': 200,
        'body': generate_presigned_url
    }