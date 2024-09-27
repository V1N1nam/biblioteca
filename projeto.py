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

def input_data_brasil(mensagem):
    while True:
        data_str = input(mensagem)
        try:
            data = datetime.strptime(data_str, '%d/%m/%Y')
            return data.strftime('%d/%m/%Y')  # Retorna a data formatada no padrão brasileiro
        except ValueError:
            print("Data inválida! Insira no formato DD/MM/AAAA.")

def cadastrar_livro():
    titulo = input_string("Digite o título do livro: ")
    autor = input_string("Digite o autor do livro: ")
    genero = input_string("Digite o gênero do livro: ")
    ano_publicacao = input_int("Digite o ano de publicação: ")
    isbn = input("Digite o ISBN do livro: ")  # O ISBN pode conter números e letras
    quantidade = input_int("Digite a quantidade de exemplares: ")

    livro = {
        'titulo': titulo,
        'autor': autor,
        'genero': genero,
        'ano_publicacao': ano_publicacao,
        'isbn': isbn,
        'quantidade': quantidade,
        'disponivel': quantidade
    }
    livros_collection.insert_one(livro)
    print("Livro cadastrado com sucesso!")

def cadastrar_usuario():
    nome = input_string("Digite o nome do usuário: ")
    email = input("Digite o e-mail do usuário: ")
    data_nascimento = input_data_brasil("Digite a data de nascimento (dd/mm/aaaa): ")
    documento = input("Digite o número do documento (CPF ou RG): ")

    usuario = {
        'nome': nome,
        'email': email,
        'data_nascimento': data_nascimento,
        'documento': documento
    }
    usuarios_collection.insert_one(usuario)
    print("Usuário cadastrado com sucesso!")

def registrar_emprestimo():
    isbn = input("Digite o ISBN do livro para empréstimo: ")
    documento_usuario = input("Digite o número do documento do usuário: ")

    livro = livros_collection.find_one({'isbn': isbn})
    usuario = usuarios_collection.find_one({'documento': documento_usuario})

    if livro and usuario:
        if livro['disponivel'] > 0:
            data_emprestimo = datetime.now()
            data_devolucao = data_emprestimo + timedelta(days=14)
            emprestimo = {
                'usuario_id': usuario['_id'],
                'livro_id': livro['_id'],
                'data_emprestimo': data_emprestimo,
                'data_devolucao': data_devolucao,
                'devolvido': False
            }
            emprestimos_collection.insert_one(emprestimo)
            livros_collection.update_one({'_id': livro['_id']}, {'$inc': {'disponivel': -1}})
            print(f"Empréstimo registrado! Devolução prevista para {data_devolucao.strftime('%d/%m/%Y')}")
        else:
            print("Não há exemplares disponíveis!")
    else:
        print("Livro ou usuário não encontrado!")