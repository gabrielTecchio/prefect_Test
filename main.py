import requests
import pandas_gbq
import pandas as pd
from prefect import flow, task
import os

os.environ["PYTHONUTF8"] = "1"  # Forces UTF-8 encoding in subprocesses.

@task
def requestReponses(url: float) -> list:
    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # print(data)
        return pd.DataFrame(data)
    else:
        print(f"Request failed with status code {response.status_code}")
        return None

@task
def sendToBQ(dataFrame: pd.core.frame.DataFrame, projID:str, dados:str, tabela:str) -> str:
    pandas_gbq.to_gbq(dataFrame, f"{projID}.{dados}.{tabela}", if_exists="replace", project_id=projID)

@flow(log_prints=True)
def flowBCBtoGBQ(codigo_serie: int):
    #codigo_serie = 21774 # 11 = SELIC; 1207 = PIB; 21774 = População
    #codigo_serie = None
    # while not codigo_serie:
        #codigo_serie: int = int(input("Enter a number (11 = SELIC; 1207 = PIB; 21774 = População; 11426 = IPCA): "))
    match codigo_serie:
            case 11:
                print("SELIC")
                tabela = "tabela-selic-teste"
            case 1207:
                print("PIB")
                tabela = "tabela-pib-teste"
            case 21774:
                print("População")
                tabela = "tabela-populacao-teste"
            case 11426:
                print("IPCA")
                tabela = "tabela-ipca-teste"
            case 1:
                print("Exchange Rate (US Dollar)")
                tabela = "tabela-dolar-teste"
            case _:
                codigo_serie = None

    project_id = "treinamentos-420711"
    conj_dados = "tabela_selic"

    # Define the API endpoint
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json"

    df = requestReponses(url)
    print(type(df))
    sendToBQ(df, project_id, conj_dados, tabela)
    return "Succes"

if __name__ == "__main__":
    # Enter a number (11 = SELIC; 1207 = PIB; 21774 = População; 11426 = IPCA)
    flowBCBtoGBQ.serve(
        name="my-first-deployment",
        tags=["onboarding"],
        parameters={"codigo_serie": 1},
        interval=60
    )