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
# BARRA LATERAL (SIDEBAR) - DADOS DO ATENDIMENTO
# ==========================================
st.sidebar.header("📋 Informações da Consulta")
st.sidebar.markdown("**Paciente:** João Silva")
st.sidebar.markdown("**Idade:** 65 anos")
st.sidebar.markdown("**ID Paciente:** #10492")
st.sidebar.markdown("---")
st.sidebar.markdown("**Enfermeiro(a) local:** Maria Souza")
st.sidebar.success("🟢 Status: Gateway Conectado")

# ==========================================
# CABEÇALHO PRINCIPAL
# ==========================================
st.title("🩺 Dashboard de Telemedicina - Acompanhamento Assistido")
st.markdown("Monitoramento de sinais vitais enviados em tempo real pelo Gateway (Enfermeiro) para o Médico.")
st.markdown("---")

# ==========================================
# GERENCIAMENTO DE ESTADO (MEMÓRIA DO APP)
# ==========================================
if 'historico' not in st.session_state:
    st.session_state.historico = pd.DataFrame(
        columns=['Horário', 'BPM', 'SpO2 (%)', 'Pressão Sistólica', 'Pressão Diastólica']
    )

# ==========================================
# FUNÇÃO DE EMULAÇÃO DE DADOS (O GATEWAY)
# ==========================================
def obter_dados_do_sensor():
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
        "Pressão Diastólica": dia_bp
    }

# ==========================================
# LÓGICA DE ATUALIZAÇÃO DOS DADOS
# ==========================================
novo_dado = obter_dados_do_sensor()
novo_df = pd.DataFrame([novo_dado])
st.session_state.historico = pd.concat([novo_df, st.session_state.historico]).head(20)

# ==========================================
# RENDERIZAÇÃO DA INTERFACE VISUAL
# ==========================================
placeholder = st.empty()

with placeholder.container():
    leitura_atual = st.session_state.historico.iloc[0]
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric(label="❤️ Batimentos Cardíacos", value=f"{leitura_atual['BPM']} BPM")
    col2.metric(label="💨 Saturação de Oxigênio", value=f"{leitura_atual['SpO2 (%)']} %")
    col3.metric(label="🩸 Pressão Arterial", value=f"{leitura_atual['Pressão Sistólica']}/{leitura_atual['Pressão Diastólica']} mmHg")
    
    st.markdown("---")
    
    st.markdown("### 📈 Monitoramento Contínuo de Batimentos (BPM)")
    dados_grafico = st.session_state.historico[['Horário', 'BPM']].copy()
    dados_grafico = dados_grafico.set_index('Horário')
    dados_grafico = dados_grafico.iloc[::-1] 
    st.line_chart(dados_grafico)
    
    st.markdown("---")
    
    st.markdown("### 📋 Últimas Medições Recebidas do Gateway")
    st.dataframe(st.session_state.historico, use_container_width=True, hide_index=True)

# ==========================================
# LOOP DE TEMPO REAL (EMULAÇÃO DE FLUXO)
# ==========================================
time.sleep(3)
st.rerun()
