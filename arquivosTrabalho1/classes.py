import socket
import RPi.GPIO as GPIO
import time

class Cancela:
    def __init__(self, sensorDeAbertura, motorCancela, sensorDeFechamento, TCP_Andar, sinalDeLotado, ehSaida):
        self.sensorDeAbertura = sensorDeAbertura
        self.motorCancela = motorCancela
        self.sensorDeFechamento = sensorDeFechamento
        self.sinalDeLotado = sinalDeLotado
        self.TCP_Andar = TCP_Andar
        self.ehSaida = ehSaida

        self.socket = None

        # Definindo o modo de numeração BCM para acessar os pinos da Rasp
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.sensorDeAbertura, GPIO.IN)
        GPIO.setup(self.sensorDeFechamento, GPIO.IN)
        GPIO.setup(self.motorCancela, GPIO.OUT)
        GPIO.setup(self.sinalDeLotado, GPIO.OUT)
        GPIO.output(self.motorCancela, GPIO.LOW)
        GPIO.output(self.sinalDeLotado, GPIO.LOW)

    def abrirCancela(self):
        GPIO.output(self.motorCancela, GPIO.HIGH)

    def verificarCancela(self):
        while(1):
            while not GPIO.input(self.sensorDeAbertura):
                time.sleep(0.1)

            self.abrirCancela()

            while not GPIO.input(self.sensorDeFechamento):
                time.sleep(0.1)

            self.fecharCancela()

            time.sleep(1)

    def fecharCancela(self):
        if self.ehSaida:
            mensagem = "Entrou um carro!"
        else:
            mensagem = "Saiu um carro!"

        self.TCP_Andar.enviaMensagem(mensagem)
        time.sleep(0.5)
        GPIO.output(self.motorCancela, GPIO.LOW)


class SensorPassagem:
    def __init__(self, sensor_de_passagem_1, sensor_de_passagem_2, sinalDeLotado, TCP_Andar):
        self.SENSOR_DE_PASSAGEM_1 = sensor_de_passagem_1
        self.SENSOR_DE_PASSAGEM_2 = sensor_de_passagem_2
        self.sinalDeLotado = sinalDeLotado
        self.TCP_Andar = TCP_Andar
        self.acionamento = []

        self.socket = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SENSOR_DE_PASSAGEM_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.SENSOR_DE_PASSAGEM_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(self.sinalDeLotado, GPIO.OUT)

        GPIO.output(self.sinalDeLotado, GPIO.LOW)

        GPIO.add_event_detect(self.SENSOR_DE_PASSAGEM_1, GPIO.BOTH, callback=self._sensor_1_callback)
        GPIO.add_event_detect(self.SENSOR_DE_PASSAGEM_2, GPIO.BOTH, callback=self._sensor_2_callback)

    def _sensor_1_callback(self, pin):
        if GPIO.input(self.SENSOR_DE_PASSAGEM_1):
            self.acionamento.append(0)
            
    def _sensor_2_callback(self, pin):
        if GPIO.input(self.SENSOR_DE_PASSAGEM_2):
            self.acionamento.append(1)

    # Método usado para gerenciar os sensores que estão entre o primeiro andar e o segundo andar
    # A variável acionamento indicará se o carro desceu ou subiu, de acordo com a ordem no array
    def monitoramentoDeSensor(self):
        while(1):
            if len(self.acionamento) == 2:
                if self.acionamento == [0, 1]:
                    mensagem = "Um carro subiu para o segundo andar!"
                    self.TCP_Andar.enviaMensagem(mensagem)
                elif self.acionamento == [1, 0]:
                    mensagem = "Um carro desceu para o primeiro andar!"
                    self.TCP_Andar.enviaMensagem(mensagem)
                
                self.acionamento = []
            
            time.sleep(0.1)


class Vaga:
    def __init__(self, endereco_01, endereco_02, endereco_03, sensor_de_vaga, andar, TCP_Andar):
        self.ENDERECO_01 = endereco_01
        self.ENDERECO_02 = endereco_02
        self.ENDERECO_03 = endereco_03
        self.SENSOR_DE_VAGA = sensor_de_vaga
        self.distribuicaoDeVagas = { '0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0 }
        self.andar = andar
        self.TCP_Andar = TCP_Andar

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ENDERECO_01, GPIO.OUT)
        GPIO.setup(self.ENDERECO_02, GPIO.OUT)
        GPIO.setup(self.ENDERECO_03, GPIO.OUT)
        GPIO.setup(self.SENSOR_DE_VAGA, GPIO.IN)
        GPIO.output(self.ENDERECO_01, GPIO.LOW)
        GPIO.output(self.ENDERECO_02, GPIO.LOW)
        GPIO.output(self.ENDERECO_03, GPIO.LOW)
    
    def mostrarVagas(self):
        total = ""
        for chave, valor in self.distribuicaoDeVagas.items():
            total += f'{chave} : {valor}\n'
        return total

    def verificarVagas(self):
        while(1):
            for i in range(8):
                sensor = 0
                valorBinario = "{0:b}".format(i).zfill(3)

                GPIO.output(self.ENDERECO_01, int(valorBinario[2]))
                GPIO.output(self.ENDERECO_02, int(valorBinario[1]))
                GPIO.output(self.ENDERECO_03, int(valorBinario[0]))

                if GPIO.input(self.SENSOR_DE_VAGA):
                    if self.distribuicaoDeVagas[str(i)] == 0:
                        self.distribuicaoDeVagas[str(i)] = 1
                        vagas_andar = "VAGAS ANDAR" + str(self.andar) + ": \n" + self.mostrarVagas()
                        self.TCP_Andar.enviaMensagem(vagas_andar)
                    
                    sensor = 1
                    
                    print(self.mostrarVagas() + "\n")

                if((self.distribuicaoDeVagas[str(i)] == 1) and (sensor == 0)):
                    self.distribuicaoDeVagas[str(i)] = 0
                    vagas_andar = "VAGAS ANDAR" + str(self.andar) + ": \n" + self.mostrarVagas()
                    self.TCP_Andar.enviaMensagem(vagas_andar)

                time.sleep(0.5)

            time.sleep(1)