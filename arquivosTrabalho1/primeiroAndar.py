import threading
from classes import Cancela, Vaga
from protocoloTCP_IP import ClienteTCP_IP_ANDAR

HOSTNAME = 'localhost'
PORTA_DO_PRIMEIRO_ANDAR = 10871

if __name__ == "__main__":

    TCP_PrimeiroAndar = ClienteTCP_IP_ANDAR(
    host = HOSTNAME,
    port = PORTA_DO_PRIMEIRO_ANDAR
    )

    cancelaParaEntrada = Cancela(
        sensorDeAbertura = 23,
        motorCancela = 10,
        sensorDeFechamento = 24,
        sinalDeLotado = 27,
        TCP_Andar = TCP_PrimeiroAndar,
        ehSaida = True
    )

    cancelaParaSaida = Cancela(
        sensorDeAbertura = 25,
        motorCancela = 17,
        sensorDeFechamento = 12,
        sinalDeLotado = 27,
        TCP_Andar = TCP_PrimeiroAndar,
        ehSaida = False
    )

    vagas = Vaga(
        endereco_01 = 22,
        endereco_02 = 26,
        endereco_03 = 19,
        sensor_de_vaga = 18,
        andar = 1,
        TCP_Andar = TCP_PrimeiroAndar
    )

    threads = []

    threadParaCancelaEntrada = threading.Thread(target=cancelaParaEntrada.verificarCancela)
    threadParaCancelaEntrada.daemon = True
    threads.append(threadParaCancelaEntrada)

    threadParaVaga = threading.Thread(target=vagas.verificarVagas)
    threadParaVaga.daemon = True
    threads.append(threadParaVaga)
    
    threadParaCancelaSaida = threading.Thread(target=cancelaParaSaida.verificarCancela)
    threadParaCancelaSaida.daemon = True
    threads.append(threadParaCancelaSaida)

    threadParaReceberMensagem = threading.Thread(target=TCP_PrimeiroAndar.recebeMensagem)
    threadParaReceberMensagem.daemon = True
    threads.append(threadParaReceberMensagem)

    for i in threads:
        i.start()

    for i in threads:
        i.join()