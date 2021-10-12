# Azure Cognitive Services - Text Summarization - Sample Code

### Azure Cognitive Services has various pre-trained model that can be easily consumed via API's & SDK's. While, there are several models available under this Azure Service, the Text Analytics API which is part of the 'Language Model' allows developers to create apps that can process natural langunage (NLP) and easily integrate them in the apps.

The following features that comes as part of [Text Analytics APi](https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/);
* Language Detection
* Entity Recognition
* Key Phrase Extraction
* Sentiment Analytsis
* Text Summarization
    
### This repo. has a sample code that would help you to get started with creating an Azure Function app and calling the Text Analytics API from the function.

### Quick Start
1. Install Azure Text Analytics Library
```
pip install azure-ai-textanalytics
```
2. Install Azure Storage Blob Library
```
pip install azure-storage-blob
```
3. Login to Azure Portal and create 'Cognitive services multi-service account' or 'Text Analytics' account
4. Once the service is created, collect the 'Key', the service 'Endpoint' URL and Region
5. Blob Connection & Container information
     * For Connecting to Azure Blob Storage - create a Shared Access Signature(SAS) and get the SAS URL
     * Note the Input container in which the raw text is available (source data)
     * Note the Input file name from the Input container
     * Note the Output container to which the summarized output needs to be stored
6. Update local.settings.json with the information collected from 4 & 5 above
