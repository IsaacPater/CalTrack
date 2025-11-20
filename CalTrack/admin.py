import os
sair = 0
pasta_arq = os.path.dirname(os.path.abspath(__file__))
arq_alimentos = os.path.join(pasta_arq, "alimentos.txt") 
arq_usuarios = os.path.join(pasta_arq, "usuarios.txt")
def cadastrar_usuario():
    print("Seja bem-vindo! \nVamos fazer seu cadastro!")
    nome = input("Digite seu nome completo: ") 
    idade = int(input("Digite sua idade: "))    
    peso = float(input('Digite seu peso (em KG): '))  
    altura = float(input('Digite sua altura (em metros): ')) 
    email = input('Digite seu email: ')  
    usr = input("Crie seu nome de usuário: ")  

    # Abre o arquivo 'usuarios.txt' em modo leitura e lê todas as linhas. Obs.: o encoding é p n dar erro se tiver acento.
    with open(arq_usuarios, 'r', encoding='utf-8') as arquivo:
        usuarios = [linha.strip() for linha in arquivo] # strip() remove espaços em branco (ou quebras de linha) no início e no fim de uma string.

    # Inicializa listas que vão guardar emails e nomes de usuário já cadastrados
    emails_existentes = []
    usuarios_existentes = []

    # Para cada linha do arquivo, separa os campos e procura por "Email:" e "Usuário:"
    for linha in usuarios:
        partes = linha.split(', ')  # o split() divide uma string em partes, criando uma lista com os pedaços separados (cada campo separado por ", ")
        for parte in partes:
            if parte.startswith('Email:'): # startswith() serve para verificar se uma string começa com um determinado texto, que nesse caso é email
                # Remove o prefixo "Email: " e adiciona só o email à lista
                email_existente = parte.replace('Email: ', '').strip() # replace() serve para substituir partes de uma string por outra, e aí primeiro c coloca a part antiga e dps a q c quer colocar no lugar, e nesse caso só tá tirando a palavra email do arquivo  
                emails_existentes.append(email_existente)
            elif parte.startswith('Usuário:'):
                # Remove o prefixo "Usuário: " e adiciona o nome de usuário à lista
                usuario_existente = parte.replace('Usuário: ', '').strip()
                usuarios_existentes.append(usuario_existente)

    # Enquanto o email digitado estiver na lista de emails existentes, pede outro email.
    while email in emails_existentes:
        print("Email já cadastrado, tente outro.")
        email = input('Digite seu email: ')

    # Enquanto o nome de usuário digitado já existir, pede outro nome de usuário.
    while usr in usuarios_existentes:
        print("Nome de usuário já cadastrado, tente outro.")
        usr = input("Crie seu nome de usuário: ")

    print("Cadastro válido! Você pode continuar.") 
    senha = input("Crie uma senha: ") 

    # Abre o arquivo em modo append ('a') e adiciona a nova linha com o formato definido
    with open(arq_usuarios, 'a', encoding='utf-8') as arquivo: # abrir o arquivo com with garante que ele vai ser fechado automaticamente, e é mais seguro
        arquivo.write(f'\nNome: {nome}, Idade: {idade}, Peso: {peso}, Altura: {altura}, Email: {email}, Usuário: {usr}, Senha: {senha}')

    # Mensagem final de sucesso no cadastro
    print(f"Cadastro concluído! Bem-vindo(a), {nome}!")


def fazer_login():
    usuario = input("Digite seu nome de usuário: ")
    snh = input("Digite sua senha: ").strip()

    # Lê todas as linhas do arquivo
    with open(arq_usuarios, 'r', encoding='utf-8') as arquivo:
        usuarios = arquivo.readlines()

    login_valido = False  # Flag para indicar se o login foi bem-sucedido

    # Percorre cada linha do arquivo procurando uma linha que contenha tanto Usuário quanto Senha
    for linha in usuarios:
        if f"Usuário: {usuario}" in linha and f"Senha: {snh}" in linha:
            login_valido = True
            break  # Para o loop ao encontrar correspondência

    if login_valido:
        # Se login válido, exibe menu de opções
        print(f"Login realizado com sucesso! Bem-vindo(a), {usuario}!")
        print(" MENU ")
        print("1 - Receitas")
        print("2 - Calculadora de calorias")
        print("3 - Meta diária")
        print("4 - Alterar peso e altura")
        print("0 - Sair")
        
        opc = int(input("Qual a opção desejada? : "))  # Pede a opção do menu
        if opc == 1:
            receitas()  # Chama função receitas
        elif opc == 2:
            contador_calorico()  # Chama função contador_calorico
        elif opc == 3:
            meta()  # Chama função meta
        elif opc == 4:
            alterar_caracteristicas()  # Chama função para alterar peso/altura
        elif opc == 0:
            confirma = input("Deseja mesmo sair? \n('sim'/'não'): ").lower()  # Confirma saída
            if confirma == 'sim':
                print('Desconectando...')
        else:
            print("Opção inválida.")  # Trata opção incorreta do menu
    else:
        # Se login inválido, avisa o usuário
        print("Usuário ou senha incorretos.")


# ----------- Funções do Menu Principal -----------
def receitas():
    print("Receitas:")
    print("- Feijoada com carne")
    print("Cozinhe o feijão e a carne juntos.")

    """filtro = ['Leite', 'Iogurte natural', 'Mussarela', 'Pão francês']
    alim = input("Digite os alimentos que você tem em casa: ")
    if alim in filtro:
    Pendente..."""


def contador_calorico():
    # Calculadora simples que soma calorias com base em um dicionário de referência
    banco = {}
    try:
        with open(arq_alimentos, 'r', encoding='utf-8') as bd:
            for linha in bd:
                if ":" in linha:
                    nome, cal = linha.strip().split(":")
                    banco[nome.lower()] = int(cal)
    except FileNotFoundError:
        print(f"Aviso: {bd} não encontrado.")
    for chave, valor in banco.items():
        print(f'{chave}: {valor} cal')
    kcal = 0
    while True:
        alimento = input('Digite o alimento ingerido até o momento \nOu 0 para finalizar: ')
        # qtdalimento = int(input(f'Digite a quantidade de {alimento} ingerida: ')) (Pendente...)
        if alimento == '0':
            break 
        # Verifica se o alimento digitado está nas chaves do dicionário e soma as calorias
        for chave, valor in banco.items():
            if alimento in chave:
                kcal += valor
    # Exibe o total de calorias consumidas
    print(f'Você ingeriu {kcal} calorias hoje.')

def meta():
    print('Digite 1 para ganhar ou 0 para perder peso.')
    info = int(input('Qual o seu objetivo? \nGanhar ou perder peso?'))
    if info == 0:
        print('Precisa ingerir menos calorias do que gasta.')
    else:
        print('Precisa ingerir mais calorias do que gasta.')


# Outras funções de adm 
def alterar_caracteristicas():
    usuario = input("Digite seu nome de usuário: ")
    senha = input("Digite sua senha: ")

    # Lê todas as linhas do arquivo para procurar o usuário correspondente
    with open(arq_usuarios, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    usuario_encontrado = False  # Flag para indicar se encontrou o usuário
    novas_linhas = []  # Lista que vai armazenar as linhas (atualizadas ou não)

    for linha in linhas:
        # Verifica se a linha corresponde ao usuário e à senha fornecidos
        if f"Usuário: {usuario}" in linha and f"Senha: {senha}" in linha:
            usuario_encontrado = True
            print("\nUsuário encontrado! Você pode alterar seu peso e altura.")
            novo_peso = float(input("Digite seu novo peso (em KG): "))  # Novo peso
            nova_altura = float(input("Digite sua nova altura (em metros): "))  # Nova altura

            # Divide a linha em campos e atualiza os campos de Peso e Altura
            partes = linha.strip().split(', ')
            for i in range(len(partes)):
                if partes[i].startswith("Peso:"):
                    partes[i] = f"Peso: {novo_peso}"
                elif partes[i].startswith("Altura:"):
                    partes[i] = f"Altura: {nova_altura}"

            # Reconstrói a linha com os campos atualizados e adiciona à lista de novas linhas
            nova_linha = ', '.join(partes)
            novas_linhas.append(nova_linha + "\n")
        else:
            # Se não for o usuário, mantém a linha original
            novas_linhas.append(linha)

    # Reescreve todo o arquivo com as linhas atualizadas (substitui o arquivo antigo) usando writelines q é usado quando você tem uma lista de strings (cada string representando uma linha) e quer gravar tudo no arquivo.
    with open(arq_usuarios, 'w', encoding='utf-8') as arquivo:
        arquivo.writelines(novas_linhas)

    # Mensagem final dependendo se o usuário foi encontrado ou não
    if usuario_encontrado:
        print("\n✅ Peso e altura atualizados com sucesso!")
    else:
        print("\n❌ Usuário ou senha incorretos. Não foi possível alterar os dados.")
