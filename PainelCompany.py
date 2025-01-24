import streamlit as st
import requests
import subprocess
import time

from teoria_risco import pageTeoriaRisco

##############################################################################################################################################
#CHAMADA DO MOTOR OU ATUALIZAÇÃO DAS TABELAS DE RELATIVIDADEDES
st.set_page_config(layout="wide")

with st.sidebar:
   #st.title("Motor de Cálculo")
   page = st.selectbox('Selecione a Opção Desejada',['Teoria do Risco'],index=None, placeholder="")

if page == 'Teoria do Risco':
    pageTeoriaRisco()

##############################################################################################################################################
#CHAMADA AUTOMATICA DA TELA DO MOTOR
streamlit_app = 'PainelCompany.py'

# URL do aplicativo
url = "http://localhost:8501"

# Verifica se o Streamlit está acessível
def is_streamlit_accessible():
      try:
          response = requests.get(url)
          return response.status_code == 200
      except requests.ConnectionError:
          return False
      
#Inicia o Streamlit
if not is_streamlit_accessible():
    process = subprocess.Popen(["streamlit", "run", streamlit_app])       

# Adiciona alguns segundos antes de iniciar o App
time.sleep(5)

##############################################################################################################################################
#CHAMADA MANUAL DA TELA DO MOTOR (Colar no Terminal)
# streamlit run c:/Users/fabri/OneDrive/4.Projetos/BMG/01.Programa_Python/Motor_calculo/PainelMotor.py"