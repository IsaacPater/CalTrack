sair = 0
import admin # importando o arquivo admin pra poder usar as funções que estão nele
while sair == 0:
    print("\nOlá! Bem-vindo ao CalTrack!")
    print("Responda com 'sim' ou 'não'.")
    print("Ou digite 0 para sair.\n")

    cad = input("Você é novo por aqui? ").lower() # lower() torna toda a string minúscula, funciona pra evitar erro caso o usuário digite alguma maiúscula
    if cad == '0':
        sair = 1
        print("Saindo do programa...")
    elif cad == "sim":
        admin.cadastrar_usuario() # chamando a função dentro do arquivo admin
    elif cad == 'não':
        admin.fazer_login()
    else:
        print("Resposta inválida. Digite 'sim', 'não' ou '0'.")