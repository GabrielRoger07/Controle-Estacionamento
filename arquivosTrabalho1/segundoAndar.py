import threading
from classes import SensorPassagem, Vaga
from protocoloTCP_IP import ClienteTCP_IP_ANDAR

HOSTNAME = 'localhost'
PORTA_DO_SEGUNDO_ANDAR = 10872

if __name__ == "__main__":

    TCP_SegundoAndar = ClienteTCP_IP_ANDAR(
    host = HOSTNAME,
    port = PORTA_DO_SEGUNDO_ANDAR
    )

    vagas = Vaga(
        endereco_01 = 13,
        endereco_02 = 6,
        endereco_03 = 5,
        sensor_de_vaga = 20,
        andar = 2,
        TCP_Andar = TCP_SegundoAndar
    )

    sensores_passagem = SensorPassagem(
        sinalDeLotado = 8,
        sensor_de_passagem_1 = 16,
        sensor_de_passagem_2 = 21,
        TCP_Andar = TCP_SegundoAndar
    )
    
    threads = []

    threadParaVaga = threading.Thread(target=vagas.verificarVagas)
    threadParaVaga.daemon = True
    threads.append(threadParaVaga)

    threadParaSensorDePassagem = threading.Thread(target=sensores_passagem.monitoramentoDeSensor)
    threadParaSensorDePassagem.daemon = True
    threads.append(threadParaSensorDePassagem)

    threadParaReceberMensagem = threading.Thread(target=TCP_SegundoAndar.recebeMensagem)
    threadParaReceberMensagem.daemon = True
    threads.append(threadParaReceberMensagem)

    for i in threads:
        i.start()

    for i in threads:
        i.join()