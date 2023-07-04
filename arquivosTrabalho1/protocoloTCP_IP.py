import socket

HOSTNAME = 'localhost'
PORTA_DO_PRIMEIRO_ANDAR = 10871
PORTA_DO_SEGUNDO_ANDAR = 10872


class ServidorTCP_IP:
    def __init__(self, hostname, porta_do_primeiro_andar, porta_do_segundo_andar):
        
        self.hostname = hostname
        self.porta_do_primeiro_andar = porta_do_primeiro_andar
        self.porta_do_segundo_andar = porta_do_segundo_andar

        self.vagasPrimeiroAndar = {i: 0 for i in range(1, 9)}
        self.vagasSegundoAndar = {i: 0 for i in range(1, 9)}
        
        # socketPrimeiroAndar e socketSegundoAndar são usadas para criar conexões com cliente
        self.socketPrimeiroAndar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketPrimeiroAndar.bind((self.hostname, self.porta_do_primeiro_andar))
        self.socketPrimeiroAndar.listen()

        self.socketSegundoAndar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketSegundoAndar.bind((self.hostname, self.porta_do_segundo_andar))
        self.socketSegundoAndar.listen()

        self.numCarrosEstacionamento = 0
        self.numCarrosPrimeiroAndar = 0
        self.numCarrosSegundoAndar = 0

    # O método aceitarConexão é o responsável por aceitar a conexão com o cliente
    def aceitarConexao(self, porta):
        if porta == self.porta_do_primeiro_andar:
            socketCliente, enderecoCliente = self.socketPrimeiroAndar.accept()
        elif porta == self.porta_do_segundo_andar:
            socketCliente, enderecoCliente = self.socketSegundoAndar.accept()
        else:
            raise ValueError("O número da porta não é válido")

        return socketCliente, enderecoCliente
    
    # O método tratamentoDeMensagem é o responsável por realizar alterações nas variáveis que armazenam quantidade de carros
    # no estacionamento, por meio das mensagens recebidas
    def tratamentoDeMensagem(self, mensagem):
        msg = mensagem.decode()
        opcoes = {
            "Entrou um carro!": (1, 1, 0),
            "Saiu um carro!": (-1, -1, 0),
            "Um carro subiu para o segundo andar!": (1, -1, 1),
            "Um carro desceu para o primeiro andar!": (-1, 1, -1)
        }
        if msg in opcoes:
            op1, op2, op3 = opcoes[msg]
            self.numCarrosEstacionamento += op1
            self.numCarrosPrimeiroAndar += op2
            self.numCarrosSegundoAndar += op3
        elif "VAGAS ANDAR1:" in msg:
            self.vagasPrimeiroAndar = msg
        elif "VAGAS ANDAR2:" in msg:
            self.vagasSegundoAndar = msg

    # O método recebimentoDeMensagemAndar é o responsável por receber as mensagens dos clientes conectados a um 
    # determinado andar do estacionamento e processá-las.
    def recebimentoDeMensagemAndar(self, socketCliente, address, andar):
        print('Está sendo recebido mensagens do andar {} {}'.format(andar, address))
        while(1):
            print('\nSeja bem vindo ao nosso estacionamento!!!')
            print('Neste momento, existem ' + str(self.numCarrosEstacionamento) + ' carros no estacionamento')
            if self.numCarrosEstacionamento > 15:
                print('O estacionamento está lotado!\n')
                mensagemDeLotacao = "Primeiro andar lotado!"
                socketCliente.send(mensagemDeLotacao.encode())

            print('Neste momento, existem ' + str(self.numCarrosPrimeiroAndar) + ' carros no primeiro andar')
            print('Neste momento, existem ' + str(self.numCarrosSegundoAndar) + ' carros no segundo andar')
            if self.numCarrosSegundoAndar > 7:
                print('O segundo andar está lotado!\n')
                mensagemDeLotacao = "Segundo andar lotado!"
                socketCliente.send(mensagemDeLotacao.encode())

            print('\n')
            # print('Quantidade de vagas no primeiro andar: ')
            print(self.vagasPrimeiroAndar)
            print('\n')
            # print('Quantidade de vagas no segundo andar: ')
            print(self.vagasSegundoAndar)

            try:
                data = socketCliente.recv(1024) # 1024 é o tamanho do buffer
                self.tratamentoDeMensagem(data)
            except:
                print('Erro ao receber mensagem do andar {} {}'.format(andar, address))
                socketCliente.close()
                break


class ClienteTCP_IP_ANDAR():
    # O construtor da classe inicializa um objeto com o porta e ip do servidor, cria um socket, estabelece conexão com o servidor e define o tamanho do buffer
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.buffer_size = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    # Método que envia mensagem para o servidor através da conexão do socket
    def enviaMensagem(self, mensagem):

        # O método encode permite que strings sejam codificadas em bytes, de forma que possam ser transmitidas através de conexões de rede
        # O método sendall garante que todos os dados sejam enviados de uma só vez, não apenas uma parte dele
        self.socket.sendall(mensagem.encode())

    # Método que fica em loop infinito e recebe mensagens do servidor
    def recebeMensagem(self):
        while(1):
            mensagem = self.socket.recv(1024)
            if mensagem.decode() == "Primeiro andar lotado!":
                print('Foi recebido a mensagem que o segundo andar está lotado')
            elif mensagem.decode() == "Segundo andar lotado!":
                print('Foi recebido a mensagem que o estacionamento está lotado')

    # Método que encerra a conexão do socket com o servidor     
    def finalizaConexao(self):
        self.socket.close()