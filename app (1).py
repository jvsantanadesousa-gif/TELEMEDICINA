import time
import json
import random
import math
from datetime import datetime

class GatewayTelemedicina:
    def __init__(self, paciente_id):
        self.paciente_id = paciente_id
        
        # --- Variáveis Iniciais de Estado ---
        # Sinais Contínuos (iniciam em zero ou normal)
        self.spo2 = 98
        self.freq_cardiaca = 75
        self.ecg_t = 0 # Tempo para gerar a onda senoidal do ECG
        
        # Dados Estáticos (Lidos apenas uma vez por consulta)
        self.peso = 0.0
        self.altura = 0.0
        self.pressao_sistolica = 0
        self.pressao_diastolica = 0
        
        # Flag para controlar quando enviar os estáticos
        self.dados_estaticos_coletados = False
        
        print(f"--- Sistema de Aquisição Iniciado para o Paciente {self.paciente_id} ---")
        print("Aguardando leitura dos sensores...\n")

    # ==========================================
    # MÉTODOS DE LEITURA DOS SENSORES (SIMULAÇÃO)
    # ==========================================
    
    def ler_sinais_continuos(self):
        """Simula a leitura USB/BLE contínua do Oxímetro e do ECG"""
        # SpO2 varia levemente entre 96 e 99%
        self.spo2 = random.randint(96, 99)
        
        # Frequência Cardíaca varia levemente entre 70 e 80 bpm
        self.freq_cardiaca += random.randint(-1, 1)
        if self.freq_cardiaca < 60: self.freq_cardiaca = 60
        if self.freq_cardiaca > 90: self.freq_cardiaca = 90
            
        # Simula uma onda de ECG simplificada (senóide com picos)
        self.ecg_t += 0.1
        onda_ecg = math.sin(self.ecg_t * 5) + (2 * math.sin(self.ecg_t * 10)) # Ruído/Pico
        valor_ecg = round(onda_ecg, 3)
        
        return {
            "tipo_dado": "STREAMING",
            "timestamp": datetime.now().isoformat(),
            "paciente_id": self.paciente_id,
            "spo2_perc": self.spo2,
            "bpm": self.freq_cardiaca,
            "onda_ecg_mv": valor_ecg
        }

    def realizar_medicao_estatica(self):
        """Simula o aperto de botão do manguito de pressão e estabilização da balança"""
        print("\n>>> INICIANDO MEDIÇÃO ESTÁTICA (PRESSÃO, PESO, ALTURA)...")
        time.sleep(2) # Simula o tempo que a braçadeira leva para inflar e a balança estabilizar
        
        self.pressao_sistolica = random.randint(110, 130)
        self.pressao_diastolica = random.randint(70, 85)
        self.peso = round(random.uniform(70.0, 75.0), 1) # Ex: 72.4 kg
        self.altura = 1.75 # Ex: 1.75 m
        
        self.dados_estaticos_coletados = True
        print(">>> MEDIÇÃO CONCLUÍDA!\n")
        
        return {
            "tipo_dado": "ESTATICO",
            "timestamp": datetime.now().isoformat(),
            "paciente_id": self.paciente_id,
            "pressao_sis": self.pressao_sistolica,
            "pressao_dia": self.pressao_diastolica,
            "peso_kg": self.peso,
            "altura_m": self.altura,
            "imc": round(self.peso / (self.altura ** 2), 2)
        }

    # ==========================================
    # MÓDULO DE TRANSMISSÃO (GATEWAY PARA NUVEM)
    # ==========================================
    
    def transmitir_para_nuvem(self, pacote_dados):
        """No sistema real, aqui iria o código MQTT.publish() ou requests.post()"""
        json_payload = json.dumps(pacote_dados)
        
        if pacote_dados["tipo_dado"] == "STREAMING":
            print(f"[TCP/WebSockets] => Enviando contínuo: {json_payload}")
        else:
            print(f"\n[API REST] => ENVIANDO PRONTUÁRIO ESTÁTICO: {json_payload}\n")

# ==========================================
# ROTINA PRINCIPAL (O LOOP DA ENFERMEIRA)
# ==========================================
if __name__ == "__main__":
    # Inicia o software para o paciente 999
    gateway = GatewayTelemedicina(paciente_id="PCT-999")
    
    ciclos = 0
    try:
        # Loop infinito simulando o carrinho de telemedicina ligado
        while True:
            # 1. Todo segundo, manda os dados contínuos do coração (ECG, SpO2)
            pacote_continuo = gateway.ler_sinais_continuos()
            gateway.transmitir_para_nuvem(pacote_continuo)
            
            # 2. Simula que a enfermeira fez a medição de Pressão e Peso após 5 segundos de consulta
            ciclos += 1
            if ciclos == 5 and not gateway.dados_estaticos_coletados:
                pacote_estatico = gateway.realizar_medicao_estatica()
                gateway.transmitir_para_nuvem(pacote_estatico)
                
            # Aguarda 1 segundo antes de gerar o próximo ponto no gráfico
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nSistema Desligado pela Enfermagem. Encerrando porta COM.")
