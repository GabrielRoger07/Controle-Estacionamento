import threading
from protocoloTCP_IP import ServidorTCP_IP

HOSTNAME = 'localhost'
# A faixa de portas destinada para minha matrícula é de 10871 a 10880
PORTA_DO_PRIMEIRO_ANDAR = 10871
PORTA_DO_SEGUNDO_ANDAR = 10872

if __name__ == '__main__':
    # Iniciando servidor
    principal = ServidorTCP_IP(HOSTNAME, PORTA_DO_PRIMEIRO_ANDAR, PORTA_DO_SEGUNDO_ANDAR)
    print('Foi inicializado o servidor em ' + HOSTNAME + ' : ' + str(PORTA_DO_PRIMEIRO_ANDAR) + ' e ' + HOSTNAME + ' : ' + str(PORTA_DO_SEGUNDO_ANDAR))

    while(1):
        try:
            # Realizando conexão da central com o primeiro andar
            socketPrimeiroAndar, enderecoPrimeiroAndar = principal.aceitarConexao(PORTA_DO_PRIMEIRO_ANDAR)
            print('A conexão com o primeiro andar foi realizada com sucesso')
            threadPrimeiroAndar = threading.Thread(target=principal.recebimentoDeMensagemAndar, args=(socketPrimeiroAndar, enderecoPrimeiroAndar, 1))
            threadPrimeiroAndar.daemon = True
            threadPrimeiroAndar.start()

            # Realizando conexão da central com o segundo andar
            socketSegundoAndar, enderecoSegundoAndar = principal.aceitarConexao(PORTA_DO_SEGUNDO_ANDAR)
            print('A conexão com o segundo andar foi realizada com sucesso')
            threadSegundoAndar = threading.Thread(target=principal.recebimentoDeMensagemAndar, args=(socketSegundoAndar, enderecoSegundoAndar, 2))
            threadSegundoAndar.daemon = True
            threadSegundoAndar.start()

        except KeyboardInterrupt:
            print("O programa foi finalizado pelo usuário")
            break
        except:
            print("Não foi possível realizar a conexão com o primeiro ou o segundo andar")
            socketPrimeiroAndar.close()
            socketSegundoAndar.close()
            break

    socketPrimeiroAndar.close()
    socketSegundoAndar.close()
    print("As conexões foram finalizadas")

# Para executar estacionamento 1 no terminal:
# ssh gabrielcruz@164.41.98.15 -p 13508
# scp -P 13508 -r ./trabalho1 gabrielcruz@164.41.98.15:/home/gabrielcruz

# Para executar estacionamento 2 no terminal:
# ssh gabrielcruz@164.41.98.28 -p 13508
# scp -P 13508 -r ./Trabalho1 gabrielcruz@164.41.98.28:/home/gabrielcruz