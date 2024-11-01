# -*- coding: UTF-8 -*-
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
from pandas_gbq import to_gbq
from prefect import flow, task
import requests

# Get BCB reponse
@task
def requestReponses():
    # Make the GET request
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json"
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # print(data)
        df = pd.DataFrame(data)
        print(df.head())
        valor = df.iloc[-1]["Valor"]
        print(f"BCB return for Value: {valor}")
        return valor
    else:
        print(f"Request failed with status code {response.status_code}")
        return None

# Function to create data to BigQuery
@task
def create_msg(msg: str = "This is a log msg from function create_msg!") -> pd.DataFrame:
    print("Creating msg!")
    # Create a DataFrame with the current date, time, and message
    data = {
        "date": [datetime.now().date()],
        "time": [datetime.now().time()],
        "message": [msg]
    }
    return pd.DataFrame(data)

# Function to write data to BigQuery
@task
def send_to_gbq(df, PROJECT_ID, DATASET_NAME, TABLE_NAME, cred):
    print("Send data to GBQ!")
    # Define the full table ID
    table_id = f"{DATASET_NAME}.{TABLE_NAME}"

    # Write the data to BigQuery, replacing the table if it doesn't exist
    to_gbq(df, table_id, project_id=PROJECT_ID, if_exists="append", credentials=cred)
    return("Data logged to BigQuery successfully.")

@flow(log_prints=True)
def myFlow():
    # Define your Google Cloud project ID and BigQuery dataset and table names
    PROJECT_ID = "treinamentos-420711"  # Replace with your Google Cloud project ID
    DATASET_NAME = "tabela_selic"  # Replace with your BigQuery dataset name
    TABLE_NAME = "test_log"  # Replace with your desired table name

    # Path to your Google Cloud service account key file
    SERVICE_ACCOUNT_FILE = "key.json"  # Replace with the path to your JSON key file

    # Authenticate using the service account file
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

    new_value = requestReponses()
    df = create_msg(f"New msg BCB answer {new_value}!")
    finalResult = send_to_gbq(df, PROJECT_ID, DATASET_NAME, TABLE_NAME, credentials)
    print(finalResult)

# Run the function
if __name__ == "__main__":
    myFlow()
