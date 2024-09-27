from config import get_database
from datetime import datetime, timedelta

# Obter a conexão com o banco de dados
db = get_database()

# Verifica explicitamente se a conexão é diferente de None
if db is not None:
    # Definir as coleções
    livros_collection = db['livros']
    usuarios_collection = db['usuarios']
    emprestimos_collection = db['emprestimos']

    print("Conexão bem-sucedida e coleções prontas para uso!")
else:
    print("Não foi possível conectar ao banco de dados.")
    exit()  # Sai do programa se a conexão falhar


def input_string(mensagem):
    while True:
        valor = input(mensagem)
        if valor.isalpha() or " " in valor:
            return valor
        else:
            print("Entrada inválida! Insira apenas caracteres alfabéticos.")


def input_int(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            print("Entrada inválida! Insira apenas números inteiros.")


