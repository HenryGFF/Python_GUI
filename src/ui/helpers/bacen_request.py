import datetime
from datetime import timedelta

import requests

def get_ptax(data):
    data_inicial = data - timedelta(days=14)

    dt = data.strftime('%d/%m/%Y')
    di = data_inicial.strftime('%d/%m/%Y')

    url = (
    "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados"
    f"?formato=json&dataInicial={di}&dataFinal={dt}"
    )

    r = requests.get(url, timeout=10)

    print("Status:", r.status_code)

    dados = r.json()
    return dados

def get_ptax_single_date(date):
    dados = get_ptax(date)
    return dados[-1] #último dia útil
#formato: {'data': '30/01/2026', 'valor': '5.2301'}

def get_ptax_period(start_date, end_date):
    ptax_list = []
    delta = end_date - start_date

    for i in range(delta.days+1):
        dia = start_date + timedelta(days=i)
        dados = get_ptax(dia)
        ptax_list.append(dados[-1])

    return ptax_list
#formtato: [{'data': '30/01/2026', 'valor': '5.2301'}, {'data': '30/01/2026', 'valor': '5.2301'}, {'data': '02/02/2026', 'valor': '5.2587'}, {'data': '03/02/2026', 'valor': '5.2236'}, {'data': '04/02/2026', 'valor': '5.2359'}, {'data': '05/02/2026', 'valor': '5.2580'}, {'data': '06/02/2026', 'valor': '5.2341'}, {'data': '06/02/2026', 'valor': '5.2341'}]