import admin  # Importando o módulo admin para usar suas funções

def exibir_menu():
    
    print("\n" + "="*40)
    print("   Olá! Bem-vindo ao CalTrack!")
    print("="*40)
    print("Responda com 'sim' ou 'não'.")
    print("Ou digite 0 para sair.\n")

def main():
    while True:
        exibir_menu()
        cad = input("Você é novo por aqui? ").strip().lower()

        if cad == '0':
            print("\nSaindo do programa... Até logo!")
            break
        elif cad == "sim":
            admin.cadastrar_usuario()
        elif cad == "não":
            admin.fazer_login()
        else:
            print("\n⚠️ Resposta inválida. Digite 'sim', 'não' ou '0'.")

if __name__ == "__main__":
    main()