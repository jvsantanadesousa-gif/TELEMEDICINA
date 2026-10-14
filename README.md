# 🩺 Dashboard de Telemedicina - TCC

Este projeto é um painel web desenvolvido em Python utilizando o framework Streamlit. Ele faz parte do meu Trabalho de Conclusão de Curso (Engenharia Elétrica) e tem como objetivo demonstrar a viabilidade técnica de uma arquitetura de telemedicina baseada em sensores IoT.

## 📌 O Problema
Em consultas de telemedicina tradicionais, o médico depende exclusivamente do relato visual ou verbal do paciente. Este projeto propõe a integração de um Gateway IoT operado localmente por um enfermeiro(a).

## ⚙️ Como Funciona a Arquitetura
1. **Coleta:** O enfermeiro afere os dados do paciente (BPM, SpO2 e Pressão Arterial) utilizando biossensores conectados a um microcontrolador (ex: ESP32).
2. **Transmissão:** O microcontrolador atua como Gateway e envia as medições brutas em tempo real via rede.
3. **Apresentação:** Este painel web recebe os dados, atualizando a interface gráfica e o histórico do paciente instantaneamente na tela do médico, sem necessidade de recarregar a página.

## 🚀 Como executar localmente
1. Instale as dependências: `pip install -r requirements.txt`
2. Rode a aplicação: `streamlit run app.py`
