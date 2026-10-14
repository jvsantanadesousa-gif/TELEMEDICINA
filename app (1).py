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
# GERENCIAMENTO DE ESTADO (MEMÓRIA DO APP)
# ==========================================
if 'historico' not in st.session_state:
    st.session_state.historico = pd.DataFrame(
        columns=['Horário', 'BPM', 'SpO2 (%)', 'Pressão Sistólica', 'Pressão Diastólica']
    )

if 'monitorando' not in st.session_state:
    st.session_state.monitorando = False

# ==========================================
# BARRA LATERAL (SIDEBAR) - DADOS EDITÁVEIS
# ==========================================
st.sidebar.header("📋 Cadastro da Consulta")

nome_paciente = st.sidebar.text_input("Nome do Paciente:", value="João Silva")
idade_paciente = st.sidebar.number_input("Idade:", min_value=0, max_value=120, value=65)
id_paciente = st.sidebar.text_input("ID do Paciente:", value="#10492")

st.sidebar.markdown("---")
nome_enfermeiro = st.sidebar.text_input("Enfermeiro(a) local:", value="Maria Souza")

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Controles do Sistema")

# Botão para ligar/desligar o monitoramento
if st.sidebar.button("▶️ Iniciar / ⏸️ Parar Monitoramento", type="primary"):
    st.session_state.monitorando = not st.session_state.monitorando

# Botão para LIMPAR OS DADOS E COMEÇAR DO ZERO
if st.sidebar.button("🗑️ Limpar Dados (Começar do 0)"):
    st.session_state.historico = pd.DataFrame(
        columns=['Horário', 'BPM', 'SpO2 (%)', 'Pressão Sistólica', 'Pressão Diastólica']
    )
    # Ao limpar, também paramos o monitoramento por segurança
    st.session_state.monitorando = False
    st.rerun()

# Indicador de Status Visual
st.sidebar.markdown("---")
if st.session_state.monitorando:
    st.sidebar.success("🟢 Status: Gateway Conectado e Transmitindo")
else:
    st.sidebar.error("🔴 Status: Monitoramento Pausado")

# ==========================================
# CABEÇALHO PRINCIPAL
# ==========================================
st.title("🩺 Dashboard de Telemedicina - Acompanhamento Assistido")
st.markdown(f"**Paciente em atendimento:** {nome_paciente} ({idade_paciente} anos) | **Enfermeiro(a) responsável:** {nome_enfermeiro}")
st.markdown("---")

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
# LÓGICA E RENDERIZAÇÃO
# ==========================================
if st.session_state.monitorando:
    novo_dado = obter_dados_do_sensor()
    novo_df = pd.DataFrame([novo_dado])
    st.session_state.historico = pd.concat([novo_df, st.session_state.historico]).head(20)

if not st.session_state.historico.empty:
    placeholder = st.empty()

    with placeholder.container():
        leitura_atual = st.session_state.historico.iloc[0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="❤️ Batimentos Cardíacos", value=f"{leitura_atual['BPM']} BPM")
        col2.metric(label="💨 Saturação de Oxigênio", value=f"{leitura_atual['SpO2 (%)']} %")
        col3.metric(label="🩸 Pressão Arterial", value=f"{leitura_atual['Pressão Sistólica']}/{leitura_atual['Pressão Diastólica']} mmHg")
        
        st.markdown("---")
        
        st.markdown(f"### 📈 Monitoramento Contínuo - {nome_paciente}")
        dados_grafico = st.session_state.historico[['Horário', 'BPM']].copy()
        dados_grafico = dados_grafico.set_index('Horário')
        dados_grafico = dados_grafico.iloc[::-1] 
        st.line_chart(dados_grafico)
        
        st.markdown("---")
        
        st.markdown("### 📋 Histórico de Medições")
        st.dataframe(st.session_state.historico, use_container_width=True, hide_index=True)

else:
    st.info("Nenhum dado registrado. Clique em 'Iniciar Monitoramento' na barra lateral para começar do zero.")

# ==========================================
# LOOP DE TEMPO REAL
# ==========================================
if st.session_state.monitorando:
    time.sleep(3)
    st.rerun()
