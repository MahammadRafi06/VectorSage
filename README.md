# "PharmaSight: AI-Powered Drug Reaction Insights"

# Human Drug Adverse Reactions Analysis and Reporting

## Project Overview

This project aims to analyze human drug adverse reactions by leveraging various data processing, extraction, and machine learning tools. The data is sourced from OpenFDA and PubChem, processed in Azure Databricks using PySpark and Spark SQL, and ultimately used to build an AI-powered application using LangChain, FAISS, and GPT-4. The final output includes both structured data in the form of Lighthouse Architecture and unstructured reports saved as PDFs.

## Project Workflow

### 1. Data Extraction
- **Source**: OpenFDA (for drug adverse reactions data)
- **Tool Used**: Azure Data Factory
  - **Config File**: A deeply nested JSON containing URLs to downloadable files.
  - **Activities**: 
    - **Lookup Activity**: Extracted the URLs from the JSON file.
    - **ForEach Activity**: Iterated over the URLs to download the data.
    - **Copy Activity**: Used HTML connectors to download the data files.

### 2. Data Processing
- **Platform**: Azure Databricks
- **Tools**: PySpark and Spark SQL
- **Data Structure**: The downloaded files contained deeply nested data.
- **Processing**: Cleaned and transformed the data into a structured format following the Lighthouse Architecture.

### 3. Reporting
- **Tool Used**: Azure SQL Data Studio
- **Reports**: Generated unstructured reports from the processed data.
- **Output**: Saved the reports as PDFs.

### 4. Chemical Compounds Data Extraction
- **Source**: PubChem
- **Tools Used**: 
  - **Playwright**: For browser automation.
  - **Asyncio**: For handling asynchronous tasks.
- **Data**: Programmatically downloaded chemical compound properties data.

### 5. Application Development
- **Framework**: Streamlit
- **AI Integration**:
  - **LangChain**: For building a language model application.
  - **Huggingface Embeddings**: For creating text embeddings.
  - **FAISS Vector Store**: For efficient similarity search.
  - **OpenAI GPT-4**: For natural language understanding and generation.
  - **Chat Prompts & Retrievers**: For effective interaction with the AI model.
- **Output**: An interactive AI-powered app that analyzes and provides insights based on the processed data.

## Installation

### Prerequisites
- Python 3.8+
- Azure Subscription (for Azure Data Factory, Azure Databricks, Azure SQL Data Studio)
- Streamlit
- LangChain, FAISS, Huggingface, OpenAI Python libraries

### Setup

1. **Clone the Repository**
    ```bash
    git clone https://github.com/MahammadRafi06/Drug-Reaction-Trends-and-Insights-with-AI
    ```

2. **Install Python Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Azure Data Factory**
   - Configure the Data Factory pipeline with the provided JSON configuration file.

4. **Set Up Azure Databricks**
   - Import the PySpark and Spark SQL scripts to process the data.

4. **Download PDF Files and Create Unstructured(pdf) reports**
   - Run python scripts.

6. **Run the Streamlit App**
    ```bash
    streamlit run app.py
    ```

## Usage

1. **Data Extraction**: Run the Azure Data Factory pipeline to download the data.
2. **Data Processing**: Use the PySpark scripts in Azure Databricks to clean and structure the data.
3. **Reporting**: Generate reports using Azure SQL Data Studio and save them as PDFs.
4. **Chemical Data Extraction**: Run the Python scripts to download chemical properties from PubChem.
5. **Application**: Use the Streamlit app to interact with the AI model and retrieve insights based on the data.

## Project Structure

```plaintext
├── data/                    # a subset of raw data files used
├── python_scripts/          # .py files to download pdf fiels from PubChem
├── Sql_files/               # Databricks and Azure SQL scripts for data processing and extraction
├── app.py                   # Streamlit application code
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
OpenFDA for providing the drug adverse reactions data.
PubChem for chemical compounds data.
Azure for cloud computing resources.
LangChain for the AI integration tools.
Streamlit for the web application framework.
OpenAI for providing the GPT-4 model.
