import streamlit as st
import os
import json
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.storage.blob import BlobServiceClient
import uuid

# Load environment variables
load_dotenv()

# Azure Blob and AI config
BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER = os.getenv("BLOB_CONTAINER")
AZURE_AI_ENDPOINT = os.getenv("AZURE_AI_ENDPOINT")
FORM_RECOGNIZER_KEY = os.getenv("FORM_RECOGNIZER_KEY")
MODEL_ID = "prebuilt-layout"

# Initialize clients
blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
doc_client = DocumentIntelligenceClient(endpoint=AZURE_AI_ENDPOINT, credential=AzureKeyCredential(FORM_RECOGNIZER_KEY))

# Ensure container exists
container_client = blob_service_client.get_container_client(BLOB_CONTAINER)
if not container_client.exists():
    container_client.create_container()

# Streamlit UI
st.title("Rental Car Inspection Digitization")
uploaded_file = st.file_uploader("Upload Inspection Form (PDF)", type=["pdf"])

if uploaded_file:
    # Safe blob name
    blob_name = f"{uuid.uuid4()}.pdf"
    blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER, blob=blob_name)
    blob_client.upload_blob(uploaded_file, overwrite=True)

    st.success(f"Uploaded to Blob Storage as: {blob_name}")

    # Download from blob for analysis
    blob_bytes = blob_client.download_blob().readall()

    # Analyze with Azure Document Intelligence
    with st.spinner("Analyzing document with Azure AI..."):
        poller = doc_client.begin_analyze_document(model_id=MODEL_ID, document=blob_bytes, features=["keyValuePairs"])
        result = poller.result()

    output = {"model_used": MODEL_ID, "key_value_pairs": {}}

    if hasattr(result, "key_value_pairs"):
        for kv in result.key_value_pairs:
            if kv.key and kv.value:
                output["key_value_pairs"][kv.key.content] = {
                    "value": kv.value.content,
                    "confidence": kv.confidence
                }

    st.subheader("Extracted Key-Value Pairs")
    st.json(output)

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    st.download_button("Download JSON", data=json.dumps(output, indent=2), file_name="inspection_data.json")
