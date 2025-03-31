from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
import time
import os
from dotenv import load_dotenv

load_dotenv() 

endpoint = os.getenv('AZURE_ENDPOINT') 
key = os.getenv('AZURE_API_KEY')

credentials = CognitiveServicesCredentials(key)

client = ComputerVisionClient(
    endpoint=endpoint,
    credentials=credentials
)

def read_image(uri):
    numberOfCharsInOperationId = 36
    maxRetries = 10

    # SDK call
    #rawHttpResponse = client.read(uri, language="fa", raw=True)
    # Check if the URI is a local file path or a URL
    if uri.startswith('http'):  # If it's a URL
        image_uri = uri
    else:  # If it's a local file path
        if os.path.exists(uri):  # Make sure the file exists
            with open(uri, "rb") as image_file:
                image_uri = image_file.read()  # Read the image content
                print(image_uri)
        else:
            return "Error: Local file path does not exist"

    # SDK call
    if isinstance(image_uri, bytes):  # If it's a local image read as bytes
        rawHttpResponse = client.read_in_stream(image_uri, language="en", raw=True)
    else:  # If it's a URL
        rawHttpResponse = client.read(image_uri, language="en", raw=True)

    # Get ID from returned headers
    operationLocation = rawHttpResponse.headers["Operation-Location"]
    idLocation = len(operationLocation) - numberOfCharsInOperationId
    operationId = operationLocation[idLocation:]

    # SDK call
    result = client.get_read_result(operationId)
    
    # Try API
    retry = 0
    
    while retry < maxRetries:
        if result.status.lower () not in ['notstarted', 'running']:
            break
        time.sleep(1)
        result = client.get_read_result(operationId)
        
        retry += 1
    
    if retry == maxRetries:
        return "max retries reached"

    if result.status == OperationStatusCodes.succeeded:
        res_text = " ".join([line.text for line in result.analyze_result.read_results[0].lines])
        return res_text
    else:
        return "error"
