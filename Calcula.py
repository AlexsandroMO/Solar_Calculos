#CALCULO_SOLAR
#Create: 18/06/2019
#By: Alexsandro Oliveira

#https://developers.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes#parse-useragent


import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
import lxml
#import xlrd

#===============================
#CEP
#===============================

global position


def cepcorreios(consultCEP):

  url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm'

  payload = {'relaxation': consultCEP,
            'tipoCEP':'ALL',
            'semelhante':'N'}

  r = requests.post(url, data=payload)
  soup = BeautifulSoup(r.text, 'html.parser')
  dados = soup.find_all('td')

  return dados

def cepcoord(consultCEP):

  url = 'https://www.mapacep.com.br/busca-cep.php'

  payload = { 'keywords': consultCEP,
              'submit': 'Pesquisar'
            }

  r = requests.post(url, data=payload)
  soup = BeautifulSoup(r.text, 'html.parser')
  dados2 = soup.find_all('title')

  return dados2

def calculogeral(cep):
  dados = cepcorreios(cep)
  dados2= cepcoord(cep)

  title = ['Local: ', 'Bairro: ', 'Cidade: ', 'CEP: ']
  edress = []

  #----------------------
  cont = 0
  for a in dados:
    for b in a:
      edress.append(title[cont] + b)
      print(b)
    cont += 1
  #----------------------

  for a in edress:
    print(a)

  local_name = dados[2].get_text()[:len(dados[2].get_text()) -4:]
  print('Local = ', local_name)

  for a in dados2:
    for b in a:
      coordenadas = b.split()

  lat = coordenadas[len(coordenadas) - 3][-12:11:]
  log = coordenadas[len(coordenadas) - 1]

  print(lat)
  print(log)

  ##Acesso CRESESB

  table = []

  url = 'http://www.cresesb.cepel.br/index.php?section=sundata'

  payload = { 'latitude_dec':lat[1:len(lat):],
              'latitude':lat,
              'hemi_lat': '0',
              'longitude_dec': log[1:len(log):],
              'longitude': log,
              'formato': '1',
              'lang': 'pt',
              'section': 'sundata'}

  header = {  'Accept': 'text/html,application/xhtml+xmlapplication/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
              'Cache-Control': 'max-age=0',
              'Connection': 'keep-alive',
              'Content-Length': '136',
              'Content-Type': 'application/x-www-form-urlencoded',
              'Cookie': 'switchgroup_news=0; switchgroup1=none',
              'Host': 'www.cresesb.cepel.br',
              'Origin': 'http://www.cresesb.cepel.br',
              'Referer': 'http://www.cresesb.cepel.br/index.php',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' }

  r = requests.post(url, data=payload)

  print(r.status_code) #if return was 200, all ok
  if r.status_code == requests.codes.ok:
    print('Continua Programa... \n')

    print('\n')

  soup = BeautifulSoup(r.text, 'lxml')

  y = soup.select('table #tb_sundata > tbody > tr')
  soup2 = BeautifulSoup(str(y), 'lxml')
  z = soup2.find_all('tr')

  dados = []
  for a in z:
    dados.append(a.get_text())
    
  dd = []
  var = []
  position = 0
  for a in dados:
    texto = a.split('\n')
    var.append(texto)
  cont = 0
  for b in var:
    for c in b[3:]:
      if c == unidecode(str(local_name)):
        print(' positin: ', cont)
        position = '{}'.format(cont)
        #print(b[8:len(b)-1])
        dd.append(b[8:len(b)-1])

    cont += 1

  mes = [
        'Distância [km]',
        'Jan',
        'Fev',
        'Mar',
        'Abr',
        'Mai',
        'Jun',
        'Jul',
        'Ago',
        'Set',
        'Out',
        'Nov',
        'Dez',
        'Média',
        'Delta'
  ]

  df = pd.DataFrame(data=dd,columns=mes)
  print('Irradiação solar diária média [kWh/m2.dia]')
  print(df)

  print('\n\n')

  #===================================================

  print(position)

  y2 = soup.select('table .tb_sundata > tbody > tr')
  soup3 = BeautifulSoup(str(y2), 'lxml')
  z2 = soup3.find_all('tr')

  dados2 = []
  for a in z2:
    dados2.append(a.get_text())
    
  dd2 = []
  var2 = []
  for a in dados2:
    texto2 = a.split('\n')
    var2.append(texto2)

  global result

  result = 0
  if int(position) == 0:
    print(var2[1])
    result = var2[1]
    
  elif int(position) == 1:
    print(var2[5])
    result = var2[5]
    
  elif int(position) == 2:
    print(var2[9])
    result = var2[9]

  mes2 = [
        'Jan',
        'Fev',
        'Mar',
        'Abr',
        'Mai',
        'Jun',
        'Jul',
        'Ago',
        'Set',
        'Out',
        'Nov',
        'Dez',
        'Média',
        'Delta'
  ]

  bass = pd.DataFrame(data=[result[4:18]], columns=mes2)
  result_table = [bass, local_name]

  return result_table


#===============================
#Lat e Log
#===============================

def consultlog_lat(cep):
  dados2= cepcoord(cep)

  for a in dados2:
    for b in a:
      coordenadas = b.split()

  lat = coordenadas[len(coordenadas) - 3][-12:11:]
  log = coordenadas[len(coordenadas) - 1]

  print(lat)
  print(log)

  result_lat_log = []
  result_lat_log.append(lat)
  result_lat_log.append(log)

  print(result_lat_log)
  
  return result_lat_log



#===========================
## Calcular Tabelas e Ler
#===========================


def calcula_DataFrame(cep, prop_name, kwp, w_, kwh, var_efic_ano, tx, inf_eneg, kit, frete, var_proj, var_inst):

  #Ler Planilhas
  df_Ano_Saldo = pd.read_csv('DATA_FRAME/df_Ano_Saldo.csv')
  df_Gera_Econ = pd.read_csv('DATA_FRAME/df_Gera_Econ.csv')
  df_P_Base1 = pd.read_csv('DATA_FRAME/df_P_Base1.csv')
  df_P_Base2 = pd.read_csv('DATA_FRAME/df_P_Base2.csv')
  df_rs_p = pd.read_csv('DATA_FRAME/df_rs_p.csv')
  ##df_TMS = pd.read_csv('DATA_FRAME/df_TMS.csv')

  #Atualiza tabela vinda do cresesb

  table_Solar = calculogeral(cep)
  
  table_Solar[0]
  local_name = table_Solar[1]
  print(local_name)

  for a in range(0, 14):
    new_tab = table_Solar[0].loc[0][a].split(',')
    Solar_table = float(new_tab[0] + '.' + new_tab[1])
    table_Solar[0].loc[0][a] = Solar_table

  ###P_Base1

  df_P_Base1['B'].loc[0] = local_name
  df_P_Base1['B'].loc[1] = kwp
  df_P_Base1['B'].loc[2] = w_
  df_P_Base1['B'].loc[3] = kwh
  df_P_Base1['B'].loc[4] = round(((df_P_Base1['B'].loc[1] * 1000) / df_P_Base1['B'].loc[2]),2)
  df_P_Base1['B'].loc[5] = round((df_P_Base1['B'].loc[1] * 8),2)
  #df_P_Base1['B'].loc[6] = norte - ver isso
  #df_P_Base1['B'].loc[7] = 23 - ver isso
  df_P_Base1

  ###P_Base2

  df_P_Base2['B'].loc[0] = var_efic_ano
  df_P_Base2['B'].loc[1] = tx
  df_P_Base2['B'].loc[2] = inf_eneg
  df_P_Base2['B'].loc[3] = kit
  df_P_Base2['B'].loc[4] = frete
  df_P_Base2['B'].loc[5] = var_proj
  df_P_Base2['B'].loc[6] = var_inst
  df_P_Base2['B'].loc[7] = round((1+(df_P_Base2['B'].loc[1]/100)),2) #Formula
  df_P_Base2['B'].loc[8] = round((1+(df_P_Base2['B'].loc[2]/100)),2) #Formula
  df_P_Base2['B'].loc[9] = round((df_P_Base2['B'].loc[3] + df_P_Base2['B'].loc[4] + df_P_Base2['B'].loc[5] + df_P_Base2['B'].loc[6]),2)
  df_P_Base2['B'].loc[10] = round(((df_P_Base2['B'].loc[3] + df_P_Base2['B'].loc[4] + df_P_Base2['B'].loc[5] + df_P_Base2['B'].loc[6])/(df_P_Base1['B'].loc[1]*1000)),2) #Formula
  df_P_Base2['B'].loc[11] = round((df_P_Base2['B'].loc[9]*0.1),2) #Formula
  df_P_Base2

  ###RS_P

  df_rs_p['KWH_GERADO'].loc[14] = 0.83

  for a in range(0, 12):
    df_rs_p['KWH_GERADO'].loc[a] = round((table_Solar[0].loc[0][a] * 30 * df_rs_p['KWH_GERADO'].loc[14] * df_P_Base1['B'].loc[1]),2)

  df_rs_p['KWH_GERADO'].loc[12] = round((df_rs_p['KWH_GERADO'].sum()),2)
  df_rs_p['KWH_GERADO'].loc[13] = round((df_rs_p['KWH_GERADO'].loc[12] / 12),2)

  ###Gera_Econ

  for a in range(0,12):
    df_Gera_Econ['TOTAL_Geracao'].loc[a] = round((df_rs_p['KWH_GERADO'].loc[a]),2)
    
  for a in range(0,12):
    df_Gera_Econ['TOTAL_Economia'].loc[a] = round((df_Gera_Econ['TOTAL_Geracao'].loc[a] * df_P_Base1['B'].loc[3]),2)
    

  df_Gera_Econ['TOTAL_Geracao'].loc[12] = round(df_Gera_Econ['TOTAL_Geracao'].loc[0:11].sum(),2)
  df_Gera_Econ['TOTAL_Economia'].loc[12] = round(df_Gera_Econ['TOTAL_Economia'].loc[0:11].sum(),2)

  ###Gera_Econ

  df_Ano_Saldo['Var_Econ_Poup_Acum'].loc[0] = df_Gera_Econ['TOTAL_Economia'].loc[12]
  for a in range(1,25):
    df_Ano_Saldo['Var_Econ_Poup_Acum'].loc[a] = round((df_Ano_Saldo['Var_Econ_Poup_Acum'].loc[a - 1] * (df_P_Base2['B'].loc[0] * df_P_Base2['B'].loc[8])),2)
    
    df_Ano_Saldo['Poup_Acum_Ger'].loc[0] = df_Gera_Econ['TOTAL_Economia'].loc[12]
  for a in range(1,25):
    df_Ano_Saldo['Poup_Acum_Ger'].loc[a] = round(((df_Ano_Saldo['Poup_Acum_Ger'].loc[a - 1] * df_P_Base2['B'].loc[7]) + df_Ano_Saldo['Var_Econ_Poup_Acum'].loc[a]),2)
    
  df_Ano_Saldo['Var_Invest'] = df_P_Base2['B'].loc[9]

  for a in range(0,25):
    df_Ano_Saldo['Retorno_Invest'].loc[a] = (df_Ano_Saldo['Poup_Acum_Ger'].loc[a] - df_Ano_Saldo['Var_Invest'].loc[a])

  result_geral = [df_Ano_Saldo, df_Gera_Econ, df_P_Base1, df_P_Base2, df_rs_p]
  
  return result_geral


