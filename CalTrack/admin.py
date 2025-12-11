import os
from datetime import datetime

# ================ ARQUIVOS ================
pasta_arq = os.path.dirname(os.path.abspath(__file__))

arq_alimentos = os.path.join(pasta_arq, "alimentos.txt")
arq_usuarios = os.path.join(pasta_arq, "usuarios.txt")
arq_tentativas = os.path.join(pasta_arq, "tentativas.txt")
arq_receitas = os.path.join(pasta_arq, "receitas.txt")
arq_calorias_diarias = os.path.join(pasta_arq, "calorias_diarias.txt")

# Criar arquivos se não existirem
for arq in [arq_tentativas, arq_receitas, arq_calorias_diarias]:
    if not os.path.exists(arq):
        with open(arq, "w", encoding="utf-8") as f:
            pass

# Criar admin padrão se não existir
if not os.path.exists(arq_usuarios):
    with open(arq_usuarios, "w", encoding="utf-8") as f:
        f.write(
            "Nome: Administrador, Idade: 30, Peso: 70.0, Altura: 1.75, Email: admin@caltrack.com, Usuário: admin, Senha: admin123, Tipo: admin\n"
        )


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


# ================ FORMATAÇÃO AUTOMÁTICA DE ALIMENTOS ================
def formatar_alimentos():
    """
    Formata e organiza o arquivo de alimentos automaticamente:
    - Remove linhas vazias e inválidas
    - Normaliza o formato (nome:calorias)
    - Converte nomes para minúsculas
    - Remove espaços extras
    - Ordena alfabeticamente
    - Remove duplicatas (mantém a última entrada)
    """
    try:
        with open(arq_alimentos, "r", encoding="utf-8") as f:
            linhas = f.readlines()
    except FileNotFoundError:
        return
    
    alimentos = {}
    
    for linha in linhas:
        linha = linha.strip()
        if not linha or ":" not in linha:
            continue
        
        # Separar nome e calorias
        partes = linha.split(":", 1)
        if len(partes) != 2:
            continue
        
        nome = partes[0].strip().lower()
        calorias_str = partes[1].strip()
        
        # Validar que calorias é um número
        try:
            calorias = int(calorias_str)
            if calorias >= 0:
                alimentos[nome] = calorias
        except ValueError:
            continue
    
    # Ordenar alfabeticamente e salvar
    alimentos_ordenados = sorted(alimentos.items(), key=lambda x: x[0])
    
    with open(arq_alimentos, "w", encoding="utf-8") as f:
        for nome, calorias in alimentos_ordenados:
            f.write(f"{nome}:{calorias}\n")


def carregar_alimentos():
    """
    Carrega os alimentos do arquivo, formatando automaticamente se necessário.
    Retorna um dicionário {nome: calorias}
    """
    formatar_alimentos()  # Formata antes de carregar
    
    banco = {}
    try:
        with open(arq_alimentos, "r", encoding="utf-8") as f:
            for linha in f:
                if ":" in linha:
                    nome, cal = linha.strip().split(":", 1)
                    banco[nome.lower()] = int(cal)
    except FileNotFoundError:
        pass
    
    return banco


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


# ================ RECUPERAÇÃO DE SENHA (MENU PRINCIPAL) ================
def recuperar_senha_menu():
    """Permite recuperar senha direto do menu principal"""
    print("\n" + "=" * 40)
    print("   REDEFINIR SENHA")
    print("=" * 40)
    
    usuario = input("\nDigite seu nome de usuário: ").strip()
    
    # Verificar se o usuário existe
    usuario_existe = False
    with open(arq_usuarios, "r", encoding="utf-8") as f:
        for linha in f:
            if f"Usuário: {usuario}" in linha:
                usuario_existe = True
                break
    
    if not usuario_existe:
        print(f"\n❌ Usuário '{usuario}' não encontrado.")
        input("\nPressione ENTER para continuar...")
        return
    
    # Solicitar email
    email = input("Digite o email cadastrado: ").strip()
    
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
                print("👉 Você já pode fazer login com a nova senha.")
                set_tentativas(usuario, 0)
                input("\nPressione ENTER para continuar...")
                return

    print("\n❌ Email incorreto.")
    input("\nPressione ENTER para continuar...")



# ================ CADASTRO ================
def cadastrar_usuario():
    print("\n" + "=" * 40)
    print("   CADASTRO DE NOVO USUÁRIO")
    print("=" * 40)

    while True:
        nome = input("Digite seu nome completo: ").strip()
        if all(parte.isalpha() or parte == "" for parte in nome.split()):
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

    print("Informe seu sexo:")
    print("1 - Masculino")
    print("2 - Feminino")

    while True:
        sexo = input("Escolha (1 ou 2): ").strip()
        if sexo == "1":
            sexo = "masculino"
            break
        elif sexo == "2":
            sexo = "feminino"
            break
        else:
            print("⚠️ Opção inválida. Digite 1 ou 2.")

    email = input("Digite seu email: ")
    usr = input("Crie seu nome de usuário: ")

    with open(arq_usuarios, "r", encoding="utf-8") as arquivo:
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

    with open(arq_usuarios, "a", encoding="utf-8") as arquivo:
        arquivo.write(
            f"Nome: {nome}, Idade: {idade}, Peso: {peso}, Altura: {altura}, Sexo: {sexo}, Email: {email}, Usuário: {usr}, Senha: {senha}, Tipo: usuario\n"
        )

    print(f"\n✅ Cadastro concluído! Bem-vindo(a), {nome}!")
    input("\nPressione ENTER para continuar...")


# ================ LOGIN ================
def fazer_login():
    usuario = input("\nDigite seu nome de usuário: ")

    tentativas = get_tentativas(usuario)

    if tentativas >= 5:
        print("\n⚠ Tentativas esgotadas!")
        print("👉 Recuperação de senha necessária.")
        recuperar_senha(usuario)
        return

    snh = input("Digite sua senha: ").strip()

    with open(arq_usuarios, "r", encoding="utf-8") as arquivo:
        usuarios = arquivo.readlines()

    login_valido = False
    tipo_usuario = "usuario"
    nome_completo = ""

    for linha in usuarios:
        partes = linha.strip().split(", ")
        dados = {}

        for parte in partes:
            if ": " in parte:
                chave, valor = parte.split(": ", 1)
                dados[chave] = valor

        if dados.get("Usuário") == usuario and dados.get("Senha") == snh:
            login_valido = True
            tipo_usuario = dados.get("Tipo", "usuario")
            nome_completo = dados.get("Nome", usuario)
            break

    if login_valido:
        print(f"\n✅ Login bem-sucedido! Bem-vindo(a), {nome_completo}!")
        set_tentativas(usuario, 0)

        if tipo_usuario == "admin":
            menu_admin(usuario)
        else:
            menu_usuario(usuario)
    else:
        tentativas += 1
        set_tentativas(usuario, tentativas)

        print("❌ Usuário ou senha incorretos.")

        if tentativas >= 5:
            print("\n⚠ Você errou 5 vezes.")
            op = input("Deseja recuperar a senha? (sim/não): ").strip().lower()
            if op == "sim":
                recuperar_senha(usuario)

        input("\nPressione ENTER para continuar...")


# ================ MENU ADMIN ================
def menu_admin(usuario):
    while True:
        print("\n" + "=" * 40)
        print("   MENU ADMINISTRADOR")
        print("=" * 40)
        print("1 - Gerenciar Usuários")
        print("2 - Gerenciar Alimentos")
        print("3 - Gerenciar Receitas")
        print("4 - Contador de Calorias")
        print("5 - Ver Receitas")
        print("0 - Sair")
        print("=" * 40)

        opc = input("Escolha: ").strip()

        if opc == "1":
            gerenciar_usuarios()
        elif opc == "2":
            gerenciar_alimentos()
        elif opc == "3":
            gerenciar_receitas()
        elif opc == "4":
            contador_calorico(usuario)
        elif opc == "5":
            ver_receitas()
        elif opc == "0":
            confirma = input("Deseja mesmo sair? (sim/não): ").lower()
            if confirma == "sim":
                print("Saindo...")
                break
        else:
            print("⚠️ Opção inválida.")


# ================ MENU USUÁRIO ================
def menu_usuario(usuario):
    while True:
        print("\n" + "=" * 40)
        print("   MENU PRINCIPAL")
        print("=" * 40)
        print("1 - Ver Receitas")
        print("2 - Contador de Calorias")
        print("3 - Ver Histórico de Calorias")
        print("4 - Meta Diária")
        print("5 - Alterar Peso e Altura")
        print("6 - Editar Histórico de Calorias")
        print("0 - Sair")
        print("=" * 40)

        opc = input("Escolha: ").strip()

        if opc == "1":
            ver_receitas()
        elif opc == "2":
            contador_calorico(usuario)
        elif opc == "3":
            ver_historico_calorias(usuario)
        elif opc == "4":
            meta()
        elif opc == "5":
            alterar_caracteristicas(usuario)
        elif opc == "6":
            editar_historico_calorias(usuario)
        elif opc == "0":
            confirma = input("Deseja mesmo sair? (sim/não): ").lower()
            if confirma == "sim":
                print("Saindo...")
                break
        else:
            print("⚠️ Opção inválida.")


# ================ GERENCIAR USUÁRIOS ================
def gerenciar_usuarios():
    while True:
        print("\n" + "=" * 40)
        print("   GERENCIAR USUÁRIOS")
        print("=" * 40)
        print("1 - Listar Usuários")
        print("2 - Deletar Usuário")
        print("3 - Ver Detalhes de Usuário")
        print("0 - Voltar")
        print("=" * 40)

        opc = input("Escolha: ").strip()

        if opc == "1":
            listar_usuarios()
        elif opc == "2":
            deletar_usuario()
        elif opc == "3":
            ver_detalhes_usuario()
        elif opc == "0":
            break
        else:
            print("⚠️ Opção inválida.")


def listar_usuarios():
    print("\n" + "=" * 40)
    print("   LISTA DE USUÁRIOS")
    print("=" * 40)

    with open(arq_usuarios, "r", encoding="utf-8") as arquivo:
        usuarios = arquivo.readlines()

    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for linha in usuarios:
        partes = linha.strip().split(", ")
        dados = {}
        for parte in partes:
            if ": " in parte:
                chave, valor = parte.split(": ", 1)
                dados[chave] = valor

        usuario = dados.get("Usuário", "N/A")
        nome = dados.get("Nome", "N/A")
        tipo = dados.get("Tipo", "usuario")
        print(f"• {usuario} - {nome} [{tipo}]")

    input("\nPressione ENTER para continuar...")


def deletar_usuario():
    usuario = input("\nDigite o nome de usuário a deletar: ").strip()

    if usuario == "admin":
        print("❌ Não é possível deletar o administrador principal.")
        input("\nPressione ENTER para continuar...")
        return

    with open(arq_usuarios, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    novas_linhas = []
    encontrado = False

    for linha in linhas:
        if f"Usuário: {usuario}" in linha:
            encontrado = True
            print(f"✅ Usuário '{usuario}' deletado com sucesso!")
        else:
            novas_linhas.append(linha)

    if encontrado:
        with open(arq_usuarios, "w", encoding="utf-8") as arquivo:
            arquivo.writelines(novas_linhas)
    else:
        print(f"❌ Usuário '{usuario}' não encontrado.")

    input("\nPressione ENTER para continuar...")


def ver_detalhes_usuario():
    usuario = input("\nDigite o nome de usuário: ").strip()

    with open(arq_usuarios, "r", encoding="utf-8") as arquivo:
        usuarios = arquivo.readlines()

    for linha in usuarios:
        if f"Usuário: {usuario}" in linha:
            print("\n" + "=" * 40)
            print("   DETALHES DO USUÁRIO")
            print("=" * 40)
            partes = linha.strip().split(", ")
            for parte in partes:
                print(f"• {parte}")
            input("\nPressione ENTER para continuar...")
            return

    print(f"❌ Usuário '{usuario}' não encontrado.")
    input("\nPressione ENTER para continuar...")


# ================ GERENCIAR ALIMENTOS ================
def gerenciar_alimentos():
    while True:
        print("\n" + "=" * 40)
        print("   GERENCIAR ALIMENTOS")
        print("=" * 40)
        print("1 - Listar Alimentos")
        print("2 - Adicionar Alimento")
        print("3 - Editar Alimento")
        print("4 - Deletar Alimento")
        print("0 - Voltar")
        print("=" * 40)

        opc = input("Escolha: ").strip()

        if opc == "1":
            listar_alimentos()
        elif opc == "2":
            adicionar_alimento()
        elif opc == "3":
            editar_alimento()
        elif opc == "4":
            deletar_alimento()
        elif opc == "0":
            break
        else:
            print("⚠️ Opção inválida.")


def listar_alimentos():
    print("\n" + "=" * 40)
    print("   LISTA DE ALIMENTOS")
    print("=" * 40)

    banco = carregar_alimentos()
    
    if not banco:
        print("Nenhum alimento cadastrado.")
    else:
        for nome, cal in sorted(banco.items()):
            print(f"• {nome.capitalize()}: {cal} kcal")

    input("\nPressione ENTER para continuar...")


def adicionar_alimento():
    nome = input("\nNome do alimento: ").strip().lower()

    while True:
        calorias = input("Calorias (por 100g): ").strip()
        if calorias.isdigit():
            calorias = int(calorias)
            break
        else:
            print("⚠️ Digite apenas números.")

    with open(arq_alimentos, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome}:{calorias}\n")
    
    formatar_alimentos()  # Organiza alfabeticamente após adicionar

    print(f"✅ Alimento '{nome}' adicionado com sucesso!")
    input("\nPressione ENTER para continuar...")


def editar_alimento():
    nome = input("\nNome do alimento a editar: ").strip().lower()

    with open(arq_alimentos, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    novas_linhas = []
    encontrado = False

    for linha in linhas:
        if ":" in linha:
            alimento, cal = linha.strip().split(":")
            if alimento.lower() == nome:
                encontrado = True
                print(f"Alimento encontrado: {alimento} - {cal} kcal")

                while True:
                    novas_calorias = input("Novas calorias: ").strip()
                    if novas_calorias.isdigit():
                        novas_calorias = int(novas_calorias)
                        break
                    else:
                        print("⚠️ Digite apenas números.")

                novas_linhas.append(f"{alimento}:{novas_calorias}\n")
                print(f"✅ Alimento '{alimento}' atualizado!")
            else:
                novas_linhas.append(linha)
        else:
            novas_linhas.append(linha)

    if encontrado:
        with open(arq_alimentos, "w", encoding="utf-8") as arquivo:
            arquivo.writelines(novas_linhas)
        formatar_alimentos()  # Reorganiza após edição
    else:
        print(f"❌ Alimento '{nome}' não encontrado.")

    input("\nPressione ENTER para continuar...")


def deletar_alimento():
    nome = input("\nNome do alimento a deletar: ").strip().lower()

    with open(arq_alimentos, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    novas_linhas = []
    encontrado = False

    for linha in linhas:
        if ":" in linha:
            alimento, cal = linha.strip().split(":")
            if alimento.lower() == nome:
                encontrado = True
                print(f"✅ Alimento '{alimento}' deletado!")
            else:
                novas_linhas.append(linha)
        else:
            novas_linhas.append(linha)

    if encontrado:
        with open(arq_alimentos, "w", encoding="utf-8") as arquivo:
            arquivo.writelines(novas_linhas)
        formatar_alimentos()  # Reorganiza após deleção
    else:
        print(f"❌ Alimento '{nome}' não encontrado.")

    input("\nPressione ENTER para continuar...")


# ================ GERENCIAR RECEITAS ================
def gerenciar_receitas():
    while True:
        print("\n" + "=" * 40)
        print("   GERENCIAR RECEITAS")
        print("=" * 40)
        print("1 - Adicionar Receita")
        print("2 - Editar Receita")
        print("3 - Deletar Receita")
        print("4 - Ver Receitas")
        print("0 - Voltar")
        print("=" * 40)

        opc = input("Escolha: ").strip()

        if opc == "1":
            adicionar_receita()
        elif opc == "2":
            editar_receita()
        elif opc == "3":
            deletar_receita()
        elif opc == "4":
            ver_receitas()
        elif opc == "0":
            break
        else:
            print("⚠️ Opção inválida.")


def adicionar_receita():
    print("\n" + "=" * 40)
    print("   ADICIONAR RECEITA")
    print("=" * 40)

    nome = input("Nome da receita: ").strip()
    ingredientes = input("Ingredientes (separados por vírgula): ").strip()
    instrucoes = input("Instruções de preparo: ").strip()

    while True:
        calorias = input("Calorias totais: ").strip()
        if calorias.isdigit():
            calorias = int(calorias)
            break
        else:
            print("⚠️ Digite apenas números.")

    with open(arq_receitas, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome}|{ingredientes}|{instrucoes}|{calorias}\n")

    print(f"✅ Receita '{nome}' adicionada com sucesso!")
    input("\nPressione ENTER para continuar...")


def editar_receita():
    nome = input("\nNome da receita a editar: ").strip()

    with open(arq_receitas, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    novas_linhas = []
    encontrado = False

    for linha in linhas:
        if "|" in linha:
            partes = linha.strip().split("|")
            if len(partes) >= 4 and partes[0].lower() == nome.lower():
                encontrado = True
                print(f"\nReceita encontrada: {partes[0]}")
                print(f"Ingredientes atuais: {partes[1]}")
                print(f"Instruções atuais: {partes[2]}")
                print(f"Calorias atuais: {partes[3]}")

                novos_ingredientes = input(
                    "\nNovos ingredientes (ENTER para manter): "
                ).strip()
                novas_instrucoes = input(
                    "Novas instruções (ENTER para manter): "
                ).strip()
                novas_calorias = input("Novas calorias (ENTER para manter): ").strip()

                if novos_ingredientes:
                    partes[1] = novos_ingredientes
                if novas_instrucoes:
                    partes[2] = novas_instrucoes
                if novas_calorias and novas_calorias.isdigit():
                    partes[3] = novas_calorias

                novas_linhas.append("|".join(partes) + "\n")
                print(f"✅ Receita '{partes[0]}' atualizada!")
            else:
                novas_linhas.append(linha)
        else:
            novas_linhas.append(linha)

    if encontrado:
        with open(arq_receitas, "w", encoding="utf-8") as arquivo:
            arquivo.writelines(novas_linhas)
    else:
        print(f"❌ Receita '{nome}' não encontrada.")

    input("\nPressione ENTER para continuar...")


def deletar_receita():
    nome = input("\nNome da receita a deletar: ").strip()

    with open(arq_receitas, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    novas_linhas = []
    encontrado = False

    for linha in linhas:
        if "|" in linha:
            partes = linha.strip().split("|")
            if len(partes) >= 1 and partes[0].lower() == nome.lower():
                encontrado = True
                print(f"✅ Receita '{partes[0]}' deletada!")
            else:
                novas_linhas.append(linha)
        else:
            novas_linhas.append(linha)

    if encontrado:
        with open(arq_receitas, "w", encoding="utf-8") as arquivo:
            arquivo.writelines(novas_linhas)
    else:
        print(f"❌ Receita '{nome}' não encontrada.")

    input("\nPressione ENTER para continuar...")


def ver_receitas():
    print("\n" + "=" * 40)
    print("   RECEITAS DISPONÍVEIS")
    print("=" * 40)

    try:
        with open(arq_receitas, "r", encoding="utf-8") as arquivo:
            receitas = arquivo.readlines()

        if not receitas:
            print("Nenhuma receita cadastrada.")
        else:
            for i, linha in enumerate(receitas, 1):
                if "|" in linha:
                    partes = linha.strip().split("|")
                    if len(partes) >= 4:
                        print(f"\n{i}. {partes[0]}")
                        print(f"   Ingredientes: {partes[1]}")
                        print(f"   Preparo: {partes[2]}")
                        print(f"   Calorias: {partes[3]} kcal")
    except FileNotFoundError:
        print("Arquivo de receitas não encontrado.")

    input("\nPressione ENTER para continuar...")


# ================ CONTADOR DE CALORIAS ================
def contador_calorico(usuario):
    print("\n" + "=" * 40)
    print("   CONTADOR DE CALORIAS")
    print("=" * 40)

    banco = carregar_alimentos()
    
    if not banco:
        print("\n⚠️ Aviso: Nenhum alimento cadastrado.")
        input("\nPressione ENTER para continuar...")
        return

    print("\nAlimentos disponíveis:")
    for chave, valor in banco.items():
        print(f"  • {chave.capitalize()}: {valor} kcal/100g")

    kcal_total = 0
    alimentos_consumidos = []

    print("\nDigite os alimentos consumidos (0 para finalizar):")

    while True:
        alimento = input("\nAlimento: ").strip().lower()
        if alimento == "0":
            break

        encontrado = False
        for chave, valor in banco.items():
            if alimento in chave:
                quantidade = input(f"Quantidade em gramas de {chave}: ").strip()
                if quantidade.isdigit():
                    quantidade = int(quantidade)
                    calorias = int((valor * quantidade) / 100)
                    kcal_total += calorias
                    alimentos_consumidos.append((chave, quantidade, calorias))
                    print(f"✅ Adicionado: {chave} ({quantidade}g) = {calorias} kcal")
                    encontrado = True
                    break
                else:
                    print("⚠️ Quantidade inválida.")
                    encontrado = True
                    break

        if not encontrado:
            print(f"❌ Alimento '{alimento}' não encontrado no banco de dados.")

    # Salvar no histórico
    data_atual = datetime.now().strftime("%Y-%m-%d")
    with open(arq_calorias_diarias, "a", encoding="utf-8") as arquivo:
        for alimento, quantidade, calorias in alimentos_consumidos:
            arquivo.write(
                f"{usuario}|{data_atual}|{alimento}|{quantidade}g|{calorias}\n"
            )

    print(f"\n{'=' * 40}")
    print("   RESUMO DO DIA")
    print(f"{'=' * 40}")
    print(f"Total de calorias consumidas: {kcal_total} kcal")
    print("Registros salvos com sucesso!")

    input("\nPressione ENTER para continuar...")


# ================ VER HISTÓRICO DE CALORIAS ================
def ver_historico_calorias(usuario):
    print("\n" + "=" * 40)
    print("   HISTÓRICO DE CALORIAS")
    print("=" * 40)

    try:
        with open(arq_calorias_diarias, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        registros_usuario = []
        for linha in linhas:
            if "|" in linha:
                partes = linha.strip().split("|")
                if len(partes) >= 5 and partes[0] == usuario:
                    registros_usuario.append(partes)

        if not registros_usuario:
            print(f"\nNenhum registro encontrado para o usuário '{usuario}'.")
        else:
            # Agrupar por data
            por_data = {}
            for registro in registros_usuario:
                data = registro[1]
                alimento = registro[2]
                quantidade = registro[3]
                calorias = int(registro[4])

                if data not in por_data:
                    por_data[data] = []
                por_data[data].append((alimento, quantidade, calorias))

            # Exibir por data
            for data in sorted(por_data.keys(), reverse=True):
                total_dia = sum(cal for _, _, cal in por_data[data])
                print(f"\n📅 {data} - Total: {total_dia} kcal")
                for alimento, quantidade, calorias in por_data[data]:
                    print(
                        f"   • {alimento.capitalize()} ({quantidade}): {calorias} kcal"
                    )

    except FileNotFoundError:
        print("\nNenhum histórico encontrado.")

    input("\nPressione ENTER para continuar...")


# ================ EDITAR HISTÓRICO DE CALORIAS ================
def editar_historico_calorias(usuario):
    """Permite editar ou deletar registros do histórico de calorias"""
    print("\n" + "=" * 40)
    print("   EDITAR HISTÓRICO DE CALORIAS")
    print("=" * 40)

    try:
        with open(arq_calorias_diarias, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        # Filtrar registros do usuário
        registros_usuario = []
        outros_registros = []
        
        for linha in linhas:
            if "|" in linha:
                partes = linha.strip().split("|")
                if len(partes) >= 5 and partes[0] == usuario:
                    registros_usuario.append(linha)
                else:
                    outros_registros.append(linha)
            else:
                outros_registros.append(linha)

        if not registros_usuario:
            print(f"\n❌ Nenhum registro encontrado para o usuário '{usuario}'.")
            input("\nPressione ENTER para continuar...")
            return

        # Exibir registros com índices
        print("\n📋 Seus registros de calorias:\n")
        for i, linha in enumerate(registros_usuario, 1):
            partes = linha.strip().split("|")
            if len(partes) >= 5:
                data = partes[1]
                alimento = partes[2]
                quantidade = partes[3]
                calorias = partes[4]
                print(f"{i}. [{data}] {alimento.capitalize()} - {quantidade} = {calorias} kcal")

        print("\n" + "-" * 40)
        escolha = input("\nDigite o número do registro a editar (0 para cancelar): ").strip()

        if escolha == "0":
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(registros_usuario):
            print("\n❌ Número inválido.")
            input("\nPressione ENTER para continuar...")
            return

        indice = int(escolha) - 1
        registro_selecionado = registros_usuario[indice].strip().split("|")

        # Mostrar detalhes do registro selecionado
        print("\n" + "=" * 40)
        print("   REGISTRO SELECIONADO")
        print("=" * 40)
        print(f"Data: {registro_selecionado[1]}")
        print(f"Alimento: {registro_selecionado[2].capitalize()}")
        print(f"Quantidade: {registro_selecionado[3]}")
        print(f"Calorias: {registro_selecionado[4]} kcal")

        # Menu de edição
        print("\n" + "-" * 40)
        print("O que deseja fazer?")
        print("1 - Alterar quantidade")
        print("2 - Deletar registro")
        print("0 - Cancelar")
        print("-" * 40)

        acao = input("\nSua escolha: ").strip()

        if acao == "0":
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        elif acao == "1":
            # Alterar quantidade
            nova_quantidade = input("\nNova quantidade em gramas: ").strip()
            
            if not nova_quantidade.isdigit():
                print("\n❌ Quantidade inválida.")
                input("\nPressione ENTER para continuar...")
                return

            nova_quantidade = int(nova_quantidade)
            
            # Buscar calorias por 100g do alimento
            alimento_nome = registro_selecionado[2]
            calorias_por_100g = None
            
            try:
                with open(arq_alimentos, "r", encoding="utf-8") as bd:
                    for linha_alimento in bd:
                        if ":" in linha_alimento:
                            nome, cal = linha_alimento.strip().split(":")
                            if nome.lower() == alimento_nome.lower():
                                calorias_por_100g = int(cal)
                                break
            except FileNotFoundError:
                print("\n⚠️ Erro ao acessar banco de alimentos.")
                input("\nPressione ENTER para continuar...")
                return

            if calorias_por_100g is None:
                print(f"\n⚠️ Alimento '{alimento_nome}' não encontrado no banco de dados.")
                print("Não é possível recalcular as calorias.")
                input("\nPressione ENTER para continuar...")
                return

            # Recalcular calorias
            novas_calorias = int((calorias_por_100g * nova_quantidade) / 100)
            
            # Atualizar registro
            registro_selecionado[3] = f"{nova_quantidade}g"
            registro_selecionado[4] = str(novas_calorias)
            
            registros_usuario[indice] = "|".join(registro_selecionado) + "\n"
            
            print(f"\n✅ Quantidade atualizada para {nova_quantidade}g")
            print(f"✅ Calorias recalculadas: {novas_calorias} kcal")

        elif acao == "2":
            # Deletar registro
            confirma = input("\n⚠️ Tem certeza que deseja deletar este registro? (sim/não): ").lower()
            
            if confirma == "sim":
                registros_usuario.pop(indice)
                print("\n✅ Registro deletado com sucesso!")
            else:
                print("\nOperação cancelada.")
                input("\nPressione ENTER para continuar...")
                return

        else:
            print("\n❌ Opção inválida.")
            input("\nPressione ENTER para continuar...")
            return

        # Salvar alterações
        with open(arq_calorias_diarias, "w", encoding="utf-8") as arquivo:
            # Escrever registros de outros usuários
            arquivo.writelines(outros_registros)
            # Escrever registros atualizados do usuário atual
            arquivo.writelines(registros_usuario)

        print("✅ Alterações salvas com sucesso!")

    except FileNotFoundError:
        print("\n❌ Arquivo de histórico não encontrado.")
    except Exception as e:
        print(f"\n❌ Erro ao editar histórico: {e}")

    input("\nPressione ENTER para continuar...")


# ================ META DIÁRIA ================
def meta():
    print("\n" + "=" * 40)
    print("   META DIÁRIA")
    print("=" * 40)
    print("\nDigite 1 para GANHAR peso ou 0 para PERDER peso.")

    while True:
        info = input("Qual seu objetivo? ").strip()
        if info in ["0", "1"]:
            info = int(info)
            break
        else:
            print("⚠️ Digite apenas 0 ou 1.")

    if info == 0:
        print("\n📉 Para PERDER peso:")
        print("   • Consuma MENOS calorias do que gasta")
        print("   • Recomendado: déficit de 300-500 kcal/dia")
        print("   • Pratique exercícios regularmente")
    else:
        print("\n📈 Para GANHAR peso:")
        print("   • Consuma MAIS calorias do que gasta")
        print("   • Recomendado: superávit de 300-500 kcal/dia")
        print("   • Foque em alimentos nutritivos")

    input("\nPressione ENTER para continuar...")


# ================ ALTERAR CARACTERÍSTICAS ================
def alterar_caracteristicas(usuario):
    print("\n" + "=" * 40)
    print("   ALTERAR PESO E ALTURA")
    print("=" * 40)

    senha = input("\nDigite sua senha para confirmar: ")

    with open(arq_usuarios, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    usuario_encontrado = False
    novas_linhas = []

    for linha in linhas:
        if f"Usuário: {usuario}" in linha and f"Senha: {senha}" in linha:
            usuario_encontrado = True
            print("\n✅ Usuário autenticado!")

            while True:
                novo_peso = input("Novo peso (kg): ").replace(",", ".")
                if novo_peso.replace(".", "", 1).isdigit():
                    novo_peso = float(novo_peso)
                    break
                else:
                    print("⚠️ Valor inválido.")

            while True:
                nova_altura = input("Nova altura (m): ").replace(",", ".")
                if nova_altura.replace(".", "", 1).isdigit():
                    nova_altura = float(nova_altura)
                    break
                else:
                    print("⚠️ Valor inválido.")

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

    with open(arq_usuarios, "w", encoding="utf-8") as arquivo:
        arquivo.writelines(novas_linhas)

    if usuario_encontrado:
        print("\n✅ Alterações feitas com sucesso!")
    else:
        print("\n❌ Senha incorreta.")

    input("\nPressione ENTER para continuar...")
