import admin  # Importando o módulo admin para usar suas funções

def exibir_menu():
    print("\n" + "="*50)
    print("   ██████╗ █████╗ ██╗     ████████╗██████╗  █████╗  ██████╗██╗  ██╗")
    print("  ██╔════╝██╔══██╗██║     ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝")
    print("  ██║     ███████║██║        ██║   ██████╔╝███████║██║     █████╔╝ ")
    print("  ██║     ██╔══██║██║        ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ")
    print("  ╚██████╗██║  ██║███████╗   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗")
    print("   ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝")
    print("="*50)
    print("        🥗 Sistema de Rastreamento de Calorias 🥗")
    print("="*50)
    print("\n📋 Você é novo por aqui?")
    print("   • Digite 'sim' para criar uma conta")
    print("   • Digite 'não' para fazer login")
    print("   • Digite 'senha' para redefinir sua senha")
    print("   • Digite '0' para sair")
    print("\n" + "-"*50)

def main():
    while True:
        exibir_menu()
        cad = input("\n👉 Sua escolha: ").strip().lower()

        if cad == '0':
            print("\n" + "="*50)
            print("   Obrigado por usar o CalTrack!")
            print("   Até logo! 👋")
            print("="*50)
            break
        elif cad == "sim":
            admin.cadastrar_usuario()
        elif cad == "não" or cad == "nao":
            admin.fazer_login()
        elif cad == "senha":
            admin.recuperar_senha_menu()
        else:
            print("\n⚠️ Resposta inválida. Digite 'sim', 'não', 'senha' ou '0'.")
            input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    main()