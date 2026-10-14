import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# ==========================================
# CONFIGURAÇÃO INICIAL DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Telemedicina - Dashboard do Médico", 
    page_icon="🩺", 
    layout="wide"
)

# ==========================================
# BARRA LATERAL (SIDEBAR) - ENTRADA MANUAL DE DADOS
# ==========================================
st.sidebar.header("📋 Cadastro e Entrada de Dados")

# Campos interativos com chave de estado (preserva o valor durante o auto-refresh)
nome_paciente = st.sidebar.text_input("Nome do Paciente", value="João Silva", key="input_nome")
idade_paciente = st.sidebar.number_input("Idade (anos)", min_value=0, max_value=120, value=65, step=1, key="input_idade")
id_paciente = st.sidebar.text_input("ID do Paciente", value="#10492", key="input_id")
enfermeiro = st.sidebar.text_input("Enfermeiro(a) local", value="Maria Souza", key="input_enfermeiro")

st.sidebar.markdown("---")
st.sidebar.subheader("⚖️ Entrada Manual de Peso e Altura")

# Campos para você digitar manualmente o Peso e a Altura
peso = st.sidebar.number_input("Peso (kg)", min_value=1.0, max_value=300.0, value=72.5, step=0.1, key="input_peso")
altura = st.sidebar.number_input("Altura (m)", min_value=0.50, max_value=2.50, value=1.75, step=0.01, key="input_altura")

# Cálculo automático do IMC a partir dos valores que você digitar
imc = round(peso / (altura ** 2), 2) if altura > 0 else 0.0

st.sidebar.markdown("---")
st.sidebar.success("🟢 Status: Gateway Conectado")

# ==========================================
# CABEÇALHO PRINCIPAL
# ==========================================
st.title("🩺 Dashboard de Telemedicina - Acompanhamento Assistido")
st.markdown(f"**Paciente:** {nome_paciente} | **Idade:** {idade_paciente} anos | **ID:** {id_paciente} | **Enfermeiro(a):** {enfermeiro}")
st.markdown("Monitoramento em tempo real integrando medições manuais e sinais vitais dos sensores.")
st.markdown("---")

# ==========================================
# GERENCIAMENTO DE ESTADO (MEMÓRIA DO APP)
# ==========================================
if 'historico' not in st.session_state:
    st.session_state.historico = pd.DataFrame(
        columns=[
            'Horário', 
            'BPM', 
            'SpO2 (%)', 
            'Pressão Sistólica', 
            'Pressão Diastólica',
            'Peso (kg)',
            'Altura (m)',
            'IMC'
        ]
    )

# ==========================================
# FUNÇÃO DE EMULAÇÃO DE DADOS DOS SENSORES
# ==========================================
def obter_dados_do_sensor(peso_val, altura_val, imc_val):
    now = datetime.now().strftime("%H:%M:%S")
    bpm = np.random.randint(60, 100)           
    spo2 = np.random.randint(95, 100)          
    sys_bp = np.random.randint(110, 130)       
    dia_bp = np.random.randint(70, 85)         
    
    return {
        "Horário": now, 
        "BPM": bpm, 
        "SpO2 (%)": spo2, 
        "Pressão Sistólica": sys_bp, 
        "Pressão Diastólica": dia_bp,
        "Peso (kg)": peso_val,
        "Altura (m)": altura_val,
        "IMC": imc_val
    }

# ==========================================
# LÓGICA DE ATUALIZAÇÃO DOS DADOS
# ==========================================
novo_dado = obter_dados_do_sensor(peso, altura, imc)
novo_df = pd.DataFrame([novo_dado])
st.session_state.historico = pd.concat([novo_df, st.session_state.historico]).head(20)

# ==========================================
# RENDERIZAÇÃO DA INTERFACE VISUAL
# ==========================================
placeholder = st.empty()

with placeholder.container():
    leitura_atual = st.session_state.historico.iloc[0]
    
    # BLOCO 1: SINAIS VITAIS DINÂMICOS (SENSORES)
    st.subheader("🩸 Sinais Vitais (Tempo Real - Sensores)")
    col1, col2, col3 = st.columns(3)
    
    col1.metric(label="❤️ Batimentos Cardíacos", value=f"{leitura_atual['BPM']} BPM")
    col2.metric(label="💨 Saturação de Oxigênio", value=f"{leitura_atual['SpO2 (%)']} %")
    col3.metric(label="🩸 Pressão Arterial", value=f"{leitura_atual['Pressão Sistólica']}/{leitura_atual['Pressão Diastólica']} mmHg")
    
    st.markdown("---")
    
    # BLOCO 2: DADOS ANTROPOMÉTRICOS (DIGITADOS MANUAMENTE)
    st.subheader("⚖️ Antropometria (Entrada Manual)")
    col4, col5, col6 = st.columns(3)
    
    col4.metric(label="⚖️ Peso Corporal", value=f"{leitura_atual['Peso (kg)']} kg")
    col5.metric(label="📏 Altura", value=f"{leitura_atual['Altura (m)']} m")
    col6.metric(label="📊 IMC Calculado", value=f"{leitura_atual['IMC']} kg/m²")
    
    st.markdown("---")
    
    # BLOCO 3: GRÁFICO DE ACOMPANHAMENTO
    st.markdown("### 📈 Monitoramento Contínuo de Batimentos (BPM)")
    dados_grafico = st.session_state.historico[['Horário', 'BPM']].copy()
    dados_grafico = dados_grafico.set_index('Horário')
    dados_grafico = dados_grafico.iloc[::-1] 
    st.line_chart(dados_grafico)
    
    st.markdown("---")
    
    # BLOCO 4: TABELA COMPLETA DE REGISTROS
    st.markdown("### 📋 Últimas Medições Recebidas")
    st.dataframe(st.session_state.historico, use_container_width=True, hide_index=True)

# ==========================================
# LOOP DE TEMPO REAL (EMULAÇÃO DE FLUXO)
# ==========================================
time.sleep(3)
st.rerun()
