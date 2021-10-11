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

    #get the blob storage connection details
    blob_connection_string = os.environ.get("blob_connection_string")
    blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
    
    #get the input container name where the audio file is stored and where the converted text file has to be uploaded
    input_container_name = os.environ.get("input_container_name")
    input_filename = os.environ.get("input_filename")

    #get the blob storage details where the output summary needs to be stored
    output_container_name = os.environ.get("output_container_name")

    #connect to the storage and download the text/doc (raw data)
    blob_container_client = blob_service_client.get_container_client(container=input_container_name)
    blob_client = blob_service_client.get_blob_client(container=input_container_name, blob=input_filename)
    data = blob_client.download_blob()
    data = data.readall()
    data = data.decode()
    str_text = data.strip()

    #EndPoint of your cognitive Services
    text_analytics_base_url = os.environ.get("text_analytics_base_url")
        
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

    #collect the output from the API
    json_output = json.dumps(json_output, indent=4, sort_keys=True)
    print("#############################################################  Raw Text #####################################################################")
    print(str_text)
    print("#############################################################  summary  #####################################################################")
    print(json_output)


    #Prepare & Uploade the summary (json) to the output container
    input_filename_json = input_filename+r"-txt-summary-out.json"
    def json_str_upload_to_blob(localfilename):
        blob = BlobClient.from_connection_string(conn_str=blob_connection_string, container_name=output_container_name, blob_name=input_filename_json)
        data = localfilename
        blob.upload_blob(data, overwrite=True)

    json_str_upload_to_blob(json_output)
    return json_output
