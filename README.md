# bina-situator
1)"bina.py" - Bina pra gerar evento da ligação VoIP pro Situator
  
    Este script é escrito em Python e usa as bibliotecas "asterisk.ami" e "requests".
    Usado para se conectar a uma Interface do Gerenciador Asterisk (AMI) e ouvir determinados eventos, especificamente eventos "Newstate" (nova ligação) com um "ChannelStateDesc" (status da ligação) de "Ringing" (chamando), uma "Exten" de "100" (fila) e um "CallerIDName" (nome do ramal) de "Supervisao Atendimento"

    Ele usa a biblioteca AMI para se conectar ao AMI no localhost (127.0.0.1) (próprio asterisk) com o nome de usuário "cxpanel" e segredo "cxmanager*con". Ele então adiciona um ouvinte de eventos para ouvir os eventos especificados.

    Quando ele recebe um evento, ele extrai o valor do campo "ConnectedLineNum" do evento e o usa para construir um payload JSON, que ele então envia para um ponto final HTTP "'ip do Situator'/api/remote-events" com uma solicitação HTTP POST.

    Em seguida, ele entra em um loop infinito que pausa por 10 segundos em cada iteração, o que permite que o script continue ouvindo eventos, até que o programa seja interrompido.


2)"atende.py" - Script pra auto atendimento da fila no Situator

    Usando as bibliotecas "asterisk.ami" e "os", esse script se conecta a uma Interface do Gerenciador Asterisk (AMI) e ouve determinados eventos, especificamente eventos "Newstate" com um "ChannelStateDesc" de "Up" e uma "Exten" diferente de 100 (geralmente, ramal da fila que atendeu a ligação).

    Ele usa a biblioteca AMI para se conectar ao AMI no localhost (127.0.0.1) (próprio asterisk) com o nome de usuário "cxpanel" e segredo "cxmanager*con". Ele então adiciona um ouvinte de eventos para ouvir os eventos especificados.

    Quando ele recebe um evento, ele extrai os valores dos campos "ConnectedLineNum" e "Exten" do evento e os usa para construir um comando que é passado para o sistema operacional através da função os.system. O comando é um comando curl que faz uma solicitação HTTP POST para o ponto final "'ip do Situator'/api/voip/events" com o payload json que contém as propriedades "src" e "dst" com os valores dos campos "ConnectedLineNum" e "Exten".


3)"disca.php" - Click-to-Call adaptado pro Situator (inserir em /var/www/disca/)

    Este script é escrito em PHP e é usado para fazer uma chamada telefônica através do
    sistema PBX Asterisk.

    O script começa definindo algumas variáveis, como o endereço IP do host do servidor Asterisk, o nome de usuário e a senha para acessar a Interface do Gerenciador Asterisk (AMI), o canal (extensão) que será usado para fazer a chamada, o contexto onde a chamada será feita, o tempo de espera, prioridade e tentativas máximas da chamada.

    Ele então pega os parâmetros "number" e "exten" da superglobal $_REQUEST que corresponde aos parâmetros GET ou POST passados para o script.

    Ele verifica se o número passado é nulo e verifica se o número contém a palavra local, se tiver, o script vai sair, caso contrário, ele vai usar a função fsockopen para abrir uma conexão de socket com o localhost na porta 5038. Ele envia o comando de login para o AMI, em seguida, ele envia um comando originate com os parâmetros que foram passados para o script.

    Ele também envia um comando Logoff e, em seguida, fecha a conexão de socket.