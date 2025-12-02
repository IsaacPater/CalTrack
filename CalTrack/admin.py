import os

# ================ ARQUIVOS ================
sair = 0
pasta_arq = os.path.dirname(os.path.abspath(__file__))

arq_alimentos = os.path.join(pasta_arq, "alimentos.txt")
arq_usuarios = os.path.join(pasta_arq, "usuarios.txt")
arq_tentativas = os.path.join(pasta_arq, "tentativas.txt")

# Criar arquivo de tentativas se não existir
if not os.path.exists(arq_tentativas):
    with open(arq_tentativas, "w", encoding="utf-8") as f:
        pass


# ================ FUNÇÕES DE TENTATIVAS ================
def get_tentativas(usuario):
    with open(arq_tentativas, "r", encoding="utf-8") as f:
        for linha in f:
            if ":" in linha:
                u, t = linha.strip().split(":")
                if u == usuario:
                    return int(t)
    return 0


def set_tentativas(usuario, tentativas):
    linhas = []
    atualizado = False

    with open(arq_tentativas, "r", encoding="utf-8") as f:
        for linha in f:
            if ":" not in linha:
                continue
            u, t = linha.strip().split(":")
            if u == usuario:
                linhas.append(f"{usuario}:{tentativas}\n")
                atualizado = True
            else:
                linhas.append(linha)

    if not atualizado:
        linhas.append(f"{usuario}:{tentativas}\n")

    with open(arq_tentativas, "w", encoding="utf-8") as f:
        f.writelines(linhas)


# ================ RECUPERAÇÃO DE SENHA ================
def recuperar_senha(usuario):
    print("\n===== RECUPERAÇÃO DE SENHA =====")
    email = input("Digite o email cadastrado: ")

    with open(arq_usuarios, "r", encoding="utf-8") as f:
        for linha in f:
            if f"Usuário: {usuario}" in linha and f"Email: {email}" in linha:
                print("\n✔ Email encontrado!")
                nova = input("Digite a nova senha (mínimo 8 caracteres): ")

                while len(nova) < 8:
                    print("A senha deve ter pelo menos 8 caracteres.")
                    nova = input("Digite novamente: ")

                partes = linha.strip().split(", ")
                for i in range(len(partes)):
                    if partes[i].startswith("Senha:"):
                        partes[i] = f"Senha: {nova}"

                nova_linha = ", ".join(partes)

                with open(arq_usuarios, "r", encoding="utf-8") as arq:
                    todas = arq.readlines()

                with open(arq_usuarios, "w", encoding="utf-8") as arq:
                    for l in todas:
                        if l.strip() == linha.strip():
                            arq.write(nova_linha + "\n")
                        else:
                            arq.write(l)

                print("\n✅ Senha alterada com sucesso!")
                set_tentativas(usuario, 0)
                return

    print("\n❌ Email incorreto.")


# ================ CADASTRO ================
def cadastrar_usuario():
    print("Seja bem-vindo! \nVamos fazer seu cadastro!")

    while True:
        nome = input("Digite seu nome completo: ").strip()
        if all(parte.isalpha() for parte in nome.split()):
            break
        else:
            print("⚠️ Digite apenas letras.")

    idade = ""
    while not idade.isdigit():
        idade = input("Digite sua idade: ")
        if not idade.isdigit():
            print("⚠️ Digite apenas números.")
    idade = int(idade)

    while True:
        peso = input("Digite seu peso (em KG): ").replace(",", ".")
        if peso.replace(".", "", 1).isdigit():
            peso = float(peso)
            break
        else:
            print("⚠️ Valor inválido.")

    while True:
        altura = input("Digite sua altura (em metros): ").replace(",", ".")
        if altura.replace(".", "", 1).isdigit():
            altura = float(altura)
            break
        else:
            print("⚠️ Valor inválido.")

    email = input("Digite seu email: ")
    usr = input("Crie seu nome de usuário: ")

    with open(arq_usuarios, 'r', encoding='utf-8') as arquivo:
        usuarios = [linha.strip() for linha in arquivo]

    emails_existentes = []
    usuarios_existentes = []

    for linha in usuarios:
        partes = linha.split(", ")
        for parte in partes:
            if parte.startswith("Email:"):
                emails_existentes.append(parte.replace("Email: ", "").strip())
            elif parte.startswith("Usuário:"):
                usuarios_existentes.append(parte.replace("Usuário: ", "").strip())

    while email in emails_existentes:
        print("Email já cadastrado.")
        email = input("Digite outro email: ")

    while usr in usuarios_existentes:
        print("Usuário já cadastrado.")
        usr = input("Digite outro nome de usuário: ")

    while True:
        senha = input("Crie uma senha (min 8 caracteres): ")
        if len(senha) < 8:
            print("Senha curta demais.")
        else:
            break

    with open(arq_usuarios, 'a', encoding='utf-8') as arquivo:
        arquivo.write(f'\nNome: {nome}, Idade: {idade}, Peso: {peso}, Altura: {altura}, Email: {email}, Usuário: {usr}, Senha: {senha}')

    print(f"Cadastro concluído! Bem-vindo(a), {nome}!")
    input("ENTER para voltar...")


# ================ LOGIN (CORRIGIDO) ================
def fazer_login():
    usuario = input("Digite seu nome de usuário: ")

    tentativas = get_tentativas(usuario)

    if tentativas >= 5:
        print("\n⚠ Tentativas esgotadas!")
        print("👉 Recuperação de senha necessária.")
        recuperar_senha(usuario)
        return

    snh = input("Digite sua senha: ").strip()

    with open(arq_usuarios, 'r', encoding='utf-8') as arquivo:
        usuarios = arquivo.readlines()

    login_valido = False

    # ----------- CORREÇÃO AQUI -----------
    for linha in usuarios:
        partes = linha.strip().split(", ")
        dados = {}

        for parte in partes:
            if ": " in parte:
                chave, valor = parte.split(": ", 1)
                dados[chave] = valor

        if dados.get("Usuário") == usuario and dados.get("Senha") == snh:
            login_valido = True
            break
    # -------------------------------------

    if login_valido:
        print(f"\n✅ Login bem-sucedido! Bem-vindo(a), {usuario}!")
        set_tentativas(usuario, 0)

        while True:
            print("\n" + "="*40)
            print(" MENU PRINCIPAL ")
            print("1 - Receitas")
            print("2 - Calculadora de calorias")
            print("3 - Meta diária")
            print("4 - Alterar peso e altura")
            print("0 - Sair")
            print("="*40)

            opc = input("Escolha: ").strip()

            if opc == "1":
                receitas()
            elif opc == "2":
                contador_calorico()
            elif opc == "3":
                meta()
            elif opc == "4":
                alterar_caracteristicas()
            elif opc == "0":
                confirma = input("Deseja mesmo sair? (sim/não): ").lower()
                if confirma == "sim":
                    print("Saindo...")
                    break
            else:
                print("Opção inválida.")
    else:
        tentativas += 1
        set_tentativas(usuario, tentativas)

        print("❌ Usuário ou senha incorretos.")

        if tentativas >= 5:
            print("\n⚠ Você errou 5 vezes.")
            op = input("Deseja recuperar a senha? (sim/não): ").strip().lower()
            if op == "sim":
                recuperar_senha(usuario)

        input("ENTER para voltar...")


# ================ RESTO DO SEU CÓDIGO ================
def receitas():
    print("\n=== Receitas ===")
    print("- Feijoada com carne")
    print("  Cozinhe o feijão e a carne juntos.\n")
    input("ENTER para voltar...")


def contador_calorico():
    banco = {}
    try:
        with open(arq_alimentos, 'r', encoding='utf-8') as bd:
            for linha in bd:
                if ":" in linha:
                    nome, cal = linha.strip().split(":")
                    banco[nome.lower()] = int(cal)
    except FileNotFoundError:
        print(f"\nAviso: {bd} não encontrado.")

    for chave, valor in banco.items():
        print(f'{chave}: {valor} cal')

    kcal = 0
    while True:
        alimento = input('\nDigite o alimento ingerido (0 para sair): ').strip().lower()
        if alimento == '0':
            break
        for chave, valor in banco.items():
            if alimento in chave:
                kcal += valor

    print(f'\nVocê ingeriu {kcal} calorias hoje.')


def meta():
    print("Digite 1 para ganhar ou 0 para perder peso.")
    info = int(input("Qual seu objetivo? "))
    if info == 0:
        print("Para perder peso, consuma menos calorias.")
    else:
        print("Para ganhar peso, consuma mais calorias.")


def alterar_caracteristicas():
    usuario = input("Digite seu nome de usuário: ")
    senha = input("Digite sua senha: ")

    with open(arq_usuarios, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    usuario_encontrado = False
    novas_linhas = []

    for linha in linhas:
        if f"Usuário: {usuario}" in linha and f"Senha: {senha}" in linha:
            usuario_encontrado = True
            print("\nUsuário encontrado!")
            novo_peso = float(input("Novo peso: "))
            nova_altura = float(input("Nova altura: "))

            partes = linha.strip().split(", ")
            for i in range(len(partes)):
                if partes[i].startswith("Peso:"):
                    partes[i] = f"Peso: {novo_peso}"
                elif partes[i].startswith("Altura:"):
                    partes[i] = f"Altura: {nova_altura}"

            nova_linha = ", ".join(partes)
            novas_linhas.append(nova_linha + "\n")
        else:
            novas_linhas.append(linha)

    with open(arq_usuarios, 'w', encoding='utf-8') as arquivo:
        arquivo.writelines(novas_linhas)

    if usuario_encontrado:
        print("\nAlterações feitas com sucesso!")
    else:
        print("\nUsuário ou senha incorretos.")
