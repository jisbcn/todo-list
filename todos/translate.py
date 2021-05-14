import json
import logging
import boto3
import os
from todos import decimalencoder

dynamodb = boto3.resource('dynamodb')


def translate(event, context):
   table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
            
# fetch todo from the database
    result = table.get_item(
          Key={
              'id': event['pathParameters']['id']
              }
                            )
    lenguaje = event['pathParameters']['language']

    client = boto3.client('translate', region_name="us-east-1")
    traduce=client.translate_text(Text=result['Item']['text'], 
            SourceLanguageCode="auto", TargetLanguageCode=lenguaje)
    
    result['Item']['text']=traduce['TranslatedText']
    response = {
            "statusCode": 200,
            "body": json.dumps(result['Item'],
            cls=decimalencoder.DecimalEncoder)
            }                                                        }
return response
