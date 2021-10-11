import requests
from pprint import pprint
import json
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import http.client

def sample_extractive_summarization():
    # Credential & Endpoint
    credential  = os.environ.get("cog_key")
    #endpoint = os.environ.get("endpoint")
    subscription_key = credential

    #get the blob storage details where the audio file is stored and where the converted text file has to be uploaded
    blob_connection_string = os.environ.get("blob_connection_string")
    blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
    input_container_name = "output-text"
    output_container_name = "output-summary-json"
    input_filename = "Diabetes interview 2.wav-converted.txt"
    blob_container_client = blob_service_client.get_container_client(container=input_container_name)
    blob_client = blob_service_client.get_blob_client(container=input_container_name, blob=input_filename)

    data = blob_client.download_blob()
    data = data.readall()
    data = data.decode()
    str_text = data.strip()

    #EndPoint
    text_analytics_base_url = 'https://arvind-csa-demo-text-analytics.cognitiveservices.azure.com/text/analytics/v3.2-preview.1/analyze/'
        
    #form the json string in the required structure to pass as the input to the api call
    documents = {
                    "analysisInput": {
                        "documents": [
                        {
                            "language": "en",
                            "id": "1",
                            "text": str_text
                        }
                        ]
                    },
                    "tasks": {
                        "extractiveSummarizationTasks": [
                        {
                            "parameters": {
                            "model-version": "latest",
                            "sentenceCount": 3,
                            "sortBy": "Offset"
                            }
                        }
                        ]
                    }
                    }


    #submit post request with headers and content
    post_results = requests.post(url=text_analytics_base_url,headers={"Ocp-Apim-Subscription-Key": subscription_key}, json=documents)

    status_code = 0
    IsItStillRunning = True
    while IsItStillRunning:
        get_results = requests.get(post_results.headers["operation-location"], headers={"Ocp-Apim-Subscription-Key":subscription_key})
        print(get_results.status_code)
        summarydata = get_results.json
        #print(summarydata)
        IsItStillRunning = get_results.json()["status"] in ("running","notStarted","idle")
        json_output = get_results.json()
        #print(json_output)

    #file_name = r"speech-to-text-nlp-output.json"
    json_output = json.dumps(json_output, indent=4, sort_keys=True)
    print("#############################################################  Raw Text #####################################################################")
    print(str_text)
    print("#############################################################  Raw Text #####################################################################")
    print(json_output)


    input_filename_json = input_filename+r"-txt-summary-out.json"
    def json_str_upload_to_blob(localfilename):
        blob = BlobClient.from_connection_string(conn_str=blob_connection_string, container_name=output_container_name, blob_name=input_filename_json)
        data = localfilename
        blob.upload_blob(data, overwrite=True)

    json_str_upload_to_blob(json_output)
    return json_output
