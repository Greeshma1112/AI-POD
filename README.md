# Rental Car Inspection Digitization

This project automates the digitization of vehicle inspection forms for rental cars. Using Azure AI Document Intelligence and Azure Blob Storage, it extracts structured data from uploaded PDFs and presents it through a user-friendly Streamlit interface.

## Features

- Upload and process vehicle inspection PDF forms
- Extract text using Azure Document Intelligence (prebuilt-layout model)
- Store uploaded PDFs securely in Azure Blob Storage
- Automatically organize and display extracted layout data

## Technologies Used

- **Python**
- **Streamlit** – for the web interface
- **Azure AI Document Intelligence** – for form recognition and layout extraction
- **Azure Blob Storage** – to securely store uploaded files
- **Azure SDK for Python** – for seamless cloud integration
- **dotenv** – for secure configuration management
