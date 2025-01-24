import streamlit as st
import pandas as pd
import io
from datetime import datetime


#######################################################################################################################################
# Definir a configuração da página (deve ser a primeira função Streamlit no script)
def pageTeoriaRisco():
     
##############################################################################################################################################
#INCLUINDO O LOGO DA EMPRESA
     col01, col02 = st.columns([2.9, 7.0])
     with col01:
          # URL da imagem do site
          url_imagem = 'https://companyprime.com.br/wp-content/uploads/2018/10/logo-companyprime2.png'
          st.image(url_imagem, width=180)
     with col02:
          st.markdown("""<h2 style='font-size: 50px; font-family: Arial, sans-serif; color: #4B0082;'>Cálculo Teoria do Risco</h2>""", unsafe_allow_html=True)
     st.write("---") #Pular Linha

######################################################################################################################################################
######################################################################################################################################################
# Definição de Cores, Letra e Tamanho do Titulo e Subtitulo

     #Formatação - Titulo dos Gráfico
     titulo_font='Arial'      #Define a fonte do Titulo
     titulo_tam_graf = '28px' #Definição do tamnho do Titulo

     #Formatação - Subtitulo dos Gráfico (Comentários)
     subtitulo_font='Arial'     #Define a fonte do Titulo
     subtitulo_tam = '11px'    #Definição do tamnho do Titulo
     cor_subtitulo = "#FF5733"  # Defina a cor do Subtitulo

     # Linha após o Titulo e Subtitulo
     linha_cor = 'blue'       #Cor da Linha
     linha_espessura = '1px'  #Espessura da linha

     # Utilizando HTML e CSS embutidos para estilizar a linha horizontal (st.markdown da primeira linha abaixo do logo)
     st.markdown("""<style>
               .my-underline {
               border-top: 13px solid blue; /* Cor Azul e espessura 2px */
               padding-top: 10px; /* Ajuste opcional para o espaçamento acima da linha */
          }
          </style>""", unsafe_allow_html=True)

##############################################################################################################################################
#PASSO 1: IMPORT DA BASESINFORMAÇÕES ADICIONAIS PARA CÁLCULO DA TEORIA DO RISCO
# Importar o DataFrame do formato Parquet

     # URL do arquivo Parquet no GitHub
     url = 'https://github.com/usuario/repo/raw/main/caminho/para/o/arquivo/BD_Sinistro_Fusaro_Teoria_Risco.parquet'

     # Leitura do arquivo Parquet direto do GitHub
     df_sinistro = pd.read_parquet(url, engine='pyarrow')

     #df_sinistro = pd.read_parquet('C:/Users/fabricio/OneDrive - MB CONSULTORIA EMPRESARIAL E CONTABIL LTDA/2.Projetos/TEORIA_RISCO/BD_Sinistro_Fusaro_Teoria_Risco.parquet', engine='pyarrow')

##############################################################################################################################################
#PASSO 2: INFORMAÇÕES ADICIONAIS PARA CÁLCULO DA TEORIA DO RISCO
     subheader_html = f"""
                         <div style='font-size:{titulo_tam_graf}; font-family:{titulo_font}; font-weight:bold;'> Informações Complementares </div>
                         <hr style='border:{linha_espessura} solid {linha_cor}; margin-top: 0; margin-bottom: 10px' /> """
                         #<div style='color:{cor_subtitulo}; font-size:{subtitulo_tam}; font-family:{subtitulo_font}; margin-bottom: 0;'> Informações complementares para o cálculo. </div>
     st.markdown(subheader_html, unsafe_allow_html=True)


#*********************************************************************************************************************************************
#2.1:  SELEÇÃO DO RAMO AGRUPADO CONFORME SES SUSEP(FIP)
     col1, col2, col3=st.columns([0.3, 0.3, 0.3])
     with col1:
          filtro_ramoAgrup = (df_sinistro[['GRACODIGO', 'GRANOME']].drop_duplicates().sort_values(by='GRACODIGO'))
          filtro_ramoAgrup = filtro_ramoAgrup.dropna(subset=['GRANOME']) # Remover linhas com valores nulos "None"
          filtro_ramoAgrup = filtro_ramoAgrup.drop(columns=['GRACODIGO'])
          select_ramoAgrup = st.selectbox("Selecione Ramo Agrupado (Fonte: SUSEP)", options=filtro_ramoAgrup['GRANOME'].tolist())
     
     df_sinistro_select = df_sinistro.query("GRANOME == @select_ramoAgrup")
     
#*********************************************************************************************************************************************
#2.2:  SELEÇÃO DO RAMO ABERTO CONFORME SES SUSEP(FIP)
     with col2:
          filtro_ramo = (df_sinistro_select[['coramo', 'noramo']].drop_duplicates().sort_values(by='coramo'))
          filtro_ramo = filtro_ramo.drop(columns=['coramo'])
          select_ramo = st.multiselect("Selecione Ramo Aberto (Fonte: SUSEP)", options=filtro_ramo['noramo'].tolist())

     df_sinistro_select = df_sinistro_select.query("noramo in @select_ramo")

#*********************************************************************************************************************************************
#2.3: Coeficiente de Confiança
     coef_confiança = {"nivel_significancia" : [0.50, 1.00, 2.00, 2.50, 5.00, 7.50, 10.00, 12.50, 15.00],
                    "coeficiente_confianca"  : [99.50, 99.00, 98.00, 97.50, 95.00, 92.50, 90.00, 87.50, 85.00],
                                   "escore"  : [2.5758, 2.3263, 2.0537, 1.9600, 1.6449, 1.4395, 1.2816, 1.1503, 1.0364]}

     coef_significancia = pd.DataFrame(coef_confiança)

     # Criar uma lista de opções formatadas (concatenando as colunas)
     opcoes = [
     f"Nível: {row['nivel_significancia']}% | Confiança: {row['coeficiente_confianca']}% | Escore: {row['escore']:.4f}" 
     for _, row in coef_significancia.iterrows()]

     # Localizar o índice da opção padrão
     opcao_default = "Nível: 5.0% | Confiança: 95.0% | Escore: 1.6449"
     indice_default = opcoes.index(opcao_default)

     with col3:
          response_coef_significancia = st.selectbox("Selecione o Coeficiente de Confiança", opcoes, index=indice_default)
     
          # Extraindo as informações da opção selecionada
          valores = response_coef_significancia.replace("Nível:", "").replace("Confiança:", "").replace("Escore:", "").split("|")
          nivel_significancia   = float(valores[0].strip().replace("%", ""))
          coeficiente_confianca = float(valores[1].strip().replace("%", ""))
          escore = float(valores[2].strip())

          # Filtrar o DataFrame com base na opção selecionada
          coef_significancia_filtrado = coef_significancia[(coef_significancia["nivel_significancia"] == nivel_significancia) &
                         (coef_significancia["coeficiente_confianca"] == coeficiente_confianca) &
                         (coef_significancia["escore"] == escore)]

          coef_significancia_filtrado['chave']=1

     st.write("") #Pular Linha

#*********************************************************************************************************************************************
#2.4:  NER-NUMERO EXPOSICAO RISCO
     col4, col5, col6=st.columns([0.3, 0.3, 0.3])
     with col4:
          df_NER = st.number_input("Digite NER-Número de Exposição ao Risco",
                                       min_value=0.00,  # Valor mínimo permitido
                                       step=1000.,      # Incremento de 1.000,00
                                       format="%.0f"    # Formato numérico sem casas decimais
                                       )
          if df_NER > 0:
               valor_formatado = f"{df_NER:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
               st.write(f"NER Digitado: {valor_formatado}")
          
     # Criação do DataFrame para o input_NER
     input_NER = pd.DataFrame({"chave" : [1], "NER_NUMERO_EXPOSICAO_RISCO": [df_NER]})


#*********************************************************************************************************************************************
#2.5:  ISE-IMPORTANCIA SEGURADA EXPOSTA
     with col5:
          df_ISE = st.number_input("Digite IS-Importância Segurada Exposta",
                                      min_value=0.00,  # Valor mínimo permitido
                                      step=10000.,     # Incremento de 1.000,00
                                      format="%.2f"    # Formato numérico sem casas decimais
                                       )
          

          if df_ISE > 0:
               col11, col12=st.columns([0.3, 0.3])
               with col11:

                    valor_formatado = f"{df_ISE:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    st.write(f"ISE Digitado: {valor_formatado}")

               with col12:
                    input_ISE = pd.DataFrame({"chave" : [1], "ISE_IMPORTANCIA_SEGURADA_EXPOSTA": [df_ISE]})

                    ISMEDIA = pd.merge(input_ISE, input_NER, on='chave', how='left')     
                    ISMEDIA['IS_MEDIA'] = (ISMEDIA['ISE_IMPORTANCIA_SEGURADA_EXPOSTA'] / ISMEDIA['NER_NUMERO_EXPOSICAO_RISCO'])

                    is_media_valor = ISMEDIA['IS_MEDIA'].iloc[0]
                    is_formatado = f"{is_media_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    st.write(f"IS Média: {is_formatado}")
               
     st.write("---") #Pular Linha
##############################################################################################################################################
#PASSO 3: TENDÊNCIA ESTATISTICA ANALITICA
     subheader_html = f"""
                    <div style='font-size:{titulo_tam_graf}; font-family:{titulo_font}; font-weight:bold;'> Resultado Teoria do Risco Por Cobertura</div>
                    <div style='color:{cor_subtitulo}; font-size:{subtitulo_tam}; font-family:{subtitulo_font}; margin-bottom: 0;'> Resumo por Cobertura </div>
                    <hr style='border:{linha_espessura} solid {linha_cor}; margin-top: 0; margin-bottom: 10px' /> """
     st.markdown(subheader_html, unsafe_allow_html=True)

#*********************************************************************************************************************************************
#3.1: CALCULO DA TENDÊNCIA ESTATISTICA

     df_sinistro_select['MSO_MONTANTE_SIN_OCO'] = (df_sinistro_select['INDENIZACAO'] + df_sinistro_select['HONORARIO'] + df_sinistro_select['DESPESA'])
     
     #CRIA O MONTANTE DE SINISTRO AO QUADRADO POR LINHA
     df_sinistro_select['MSO_MONTANTE_SIN_OCO_QUADRADO'] = df_sinistro_select['MSO_MONTANTE_SIN_OCO'] ** 2

     #CRIA A QUANTIDADE DE SINISTRO - Cria o campo NSO_NUMERO_SIN_OCO contando apenas uma vez cada Claims_Number
     df_sinistro_select['NSO_NUMERO_SIN_OCO'] = df_sinistro_select['Claims_Number'].drop_duplicates().groupby(df_sinistro_select['Claims_Number']).transform('count')
     df_sinistro_select['NSO_NUMERO_SIN_OCO'] = df_sinistro_select['NSO_NUMERO_SIN_OCO'].fillna(0)

     #AGRUPA AS INFORMAÇÕES DA BASE
     df_agrupado = df_sinistro_select.groupby(['GRANOME', 'Cobertura']).agg({'NSO_NUMERO_SIN_OCO'   : 'sum',
                                                                             'MSO_MONTANTE_SIN_OCO'  : 'sum',
                                                                             'MSO_MONTANTE_SIN_OCO_QUADRADO' :'sum'}).reset_index()

     # Calcula os totais gerais
     total_geral = {'GRANOME'                       : 'TOTAL GERAL',
                    'Cobertura'                     : '',  # Deixe vazio se não há um valor específico para essa coluna
                    'NSO_NUMERO_SIN_OCO'            : df_agrupado['NSO_NUMERO_SIN_OCO'].sum(),
                    'MSO_MONTANTE_SIN_OCO'          : df_agrupado['MSO_MONTANTE_SIN_OCO'].sum(),
                    'MSO_MONTANTE_SIN_OCO_QUADRADO' : df_agrupado['MSO_MONTANTE_SIN_OCO_QUADRADO'].sum()
}
     # Adiciona a linha "Total Geral" ao DataFrame
     df_agrupado = pd.concat([df_agrupado, pd.DataFrame([total_geral])], ignore_index=True)


     #CRIA A CHAVE PARA O MERGE
     df_agrupado['chave']=1
     df_agrupado = pd.merge(df_agrupado, coef_significancia_filtrado, on='chave', how='left')
     df_agrupado = pd.merge(df_agrupado, input_NER, on='chave', how='left')
     df_agrupado = pd.merge(df_agrupado, input_ISE, on='chave', how='left')

     #CRIA TRC-TAXA RISCO COLETIVO
     
     df_agrupado['TRC_TAXA_RISCO_COLETIVO'] = df_agrupado['MSO_MONTANTE_SIN_OCO'] / df_agrupado['ISE_IMPORTANCIA_SEGURADA_EXPOSTA']*100

     #CRIA TP-TAXA PURA
     df_agrupado['TP_TAXA_PURA'] = ((df_agrupado['MSO_MONTANTE_SIN_OCO'] + df_agrupado['escore']*(df_agrupado['MSO_MONTANTE_SIN_OCO_QUADRADO']**0.5))/df_agrupado['ISE_IMPORTANCIA_SEGURADA_EXPOSTA'])*100


     #CRIA CARREGAMENTO ESTATISTICO DE SEGURANÇA OU VR(TP-TAXA_PURA / TRC-TAXA_RISCO_COLETIVO)
     df_agrupado['TRC_TP_CARREGAMENTO_ESTATISTICO'] = ((((df_agrupado['TP_TAXA_PURA'] / df_agrupado['TRC_TAXA_RISCO_COLETIVO']))-1)*100)
          
     df_agrupado = df_agrupado.rename(columns={'GRANOME'                          : 'Ramo Agrupado',
                                               #'noramo'                           : 'Ramo',
                                               'Cobertura'                        : 'Cobertura',       
                                               'NER_NUMERO_EXPOSICAO_RISCO'       : 'Expostos Risco',
                                               'ISE_IMPORTANCIA_SEGURADA_EXPOSTA' : 'IS Exposta',
                                               'NSO_NUMERO_SIN_OCO'               : 'Qtde Sin. Ocorrido',
                                               'MSO_MONTANTE_SIN_OCO'             : 'Valor Sin. Ocorrido',
                                               'MSO_MONTANTE_SIN_OCO_QUADRADO'    : 'MSO^2 - Montante Sin. Oco',
                                               'TRC_TAXA_RISCO_COLETIVO'          : 'TR-Taxa Risco',
                                               'TP_TAXA_PURA'                     : 'TP-Taxa Pura',
                                               'TRC_TP_CARREGAMENTO_ESTATISTICO'  : 'TP/TR - Final'})

     df_TR_saida = df_agrupado[['Ramo Agrupado',
                                #'Ramo',
                                'Cobertura',
                                'Expostos Risco',
                                'IS Exposta',
                                'Qtde Sin. Ocorrido',
                                'Valor Sin. Ocorrido',
                                #'MSO^2 - Montante Sin. Oco',
                                'TR-Taxa Risco',
                                'TP-Taxa Pura',
                                'TP/TR - Final']]
     
     # Aplica a formatação de % nos campos abaixo
     campos_percentuais = ['TR-Taxa Risco', 'TP-Taxa Pura', 'TP/TR - Final']
     for campo in campos_percentuais:
          df_TR_saida[campo] = df_TR_saida[campo].apply(lambda x: f"{x:.4f}".replace('.', ',') + '%')

     st.write(df_TR_saida)

#*********************************************************************************************************************************************
#4: EXPORTA A BASE DE TAXA PARA O EXCEL
     def to_excel(df_TR_saida):
          # Adiciona a coluna 'data_export' com a data e hora atual
          df_TR_saida['Data Export'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          
          # Usando BytesIO para criar o arquivo Excel em memória
          output = io.BytesIO()
          with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
               df_TR_saida.to_excel(writer, index=False, sheet_name='Resultado')
          output.seek(0)
          return output.read()

     # Adicionar o botão de exportação para Excel
     ramo_agrupado = df_TR_saida['Ramo Agrupado'].unique()[0]

     st.download_button(label="Exportar Resultado",
                        data=to_excel(df_TR_saida),  # Data é o DataFrame convertido para Excel
                        file_name=f"Teoria do Risco Por Cobertura - {ramo_agrupado}.xlsx",  # Nome do arquivo exportado
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",)  # Tipo MIME para Excel
 
#Critérios utilizados
# regra  df_sinistro = df_sinistro[df_sinistro['Tipo_Mov'].isin(['PAGOS', 'AVISADOS'])]
# df_sinistro_select['MSO_MONTANTE_SIN_OCO'] = (df_sinistro_select['INDENIZACAO'] + df_sinistro_select['HONORARIO'] + df_sinistro_select['DESPESA'])
#Ramo com a classificação SUSEP



     
     

     
