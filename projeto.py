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

def devolver_livro():
    isbn = input("Digite o ISBN do livro a ser devolvido: ")
    documento_usuario = input("Digite o número do documento do usuário: ")

    livro = livros_collection.find_one({'isbn': isbn})
    usuario = usuarios_collection.find_one({'documento': documento_usuario})

    if livro and usuario:
        emprestimo = emprestimos_collection.find_one({
            'livro_id': livro['_id'],
            'usuario_id': usuario['_id'],
            'devolvido': False
        })
        if emprestimo:
            emprestimos_collection.update_one({'_id': emprestimo['_id']}, {'$set': {'devolvido': True, 'data_real_devolucao': datetime.now()}})
            livros_collection.update_one({'_id': livro['_id']}, {'$inc': {'disponivel': 1}})
            print("Livro devolvido com sucesso!")
        else:
            print("Empréstimo não encontrado!")
    else:
        print("Livro ou usuário não encontrado!")

def listar_livros_disponiveis():
    livros = livros_collection.find({'disponivel': {'$gt': 0}})
    for livro in livros:
        print(f"Título: {livro['titulo']}, Disponíveis: {livro['disponivel']}")

def consultar_emprestimos_abertos():
    emprestimos = emprestimos_collection.find({'devolvido': False})
    emprestimos_list = list(emprestimos)  # Converte o cursor em uma lista
    if emprestimos_list:  # Verifica se a lista não está vazia
        print("\n--- Empréstimos Abertos ---")
        for emprestimo in emprestimos_list:
            usuario = usuarios_collection.find_one({'_id': emprestimo['usuario_id']})
            livro = livros_collection.find_one({'_id': emprestimo['livro_id']})
            print(f"Usuário: {usuario['nome']}, Livro: {livro['titulo']}, "
                  f"Data de Devolução: {emprestimo['data_devolucao'].strftime('%d/%m/%Y')}")
    else:
        print("Não há empréstimos abertos.")

def listar_emprestimos_vencidos():
    emprestimos_vencidos = emprestimos_collection.find({
        'data_devolucao': {'$lt': datetime.now()},
        'devolvido': False
    })
    emprestimos_vencidos_list = list(emprestimos_vencidos)  # Converte o cursor em uma lista
    if emprestimos_vencidos_list:  # Verifica se a lista não está vazia
        print("\n--- Empréstimos Vencidos ---")
        for emprestimo in emprestimos_vencidos_list:
            usuario = usuarios_collection.find_one({'_id': emprestimo['usuario_id']})
            livro = livros_collection.find_one({'_id': emprestimo['livro_id']})
            print(f"Usuário: {usuario['nome']}, Livro: {livro['titulo']}, "
                  f"Data de Empréstimo: {emprestimo['data_emprestimo'].strftime('%d/%m/%Y')}, "
                  f"Data de Devolução: {emprestimo['data_devolucao'].strftime('%d/%m/%Y')}")
    else:
        print("Não há empréstimos vencidos.")

# Menu principal
def menu():
    while True:
        print("\n---- Menu Biblioteca ----")
        print("1. Cadastrar Livro")
        print("2. Cadastrar Usuário")
        print("3. Registrar Empréstimo")
        print("4. Devolver Livro")
        print("5. Listar Livros Disponíveis")
        print("6. Listar Empréstimos Abertos")  # Atualização do nome
        print("7. Listar Empréstimos Vencidos")  # Atualização do nome
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_livro()
        elif opcao == '2':
            cadastrar_usuario()
        elif opcao == '3':
            registrar_emprestimo()
        elif opcao == '4':
            devolver_livro()
        elif opcao == '5':
            listar_livros_disponiveis()
        elif opcao == '6':
            consultar_emprestimos_abertos()  # Chama a função de listar empréstimos abertos
        elif opcao == '7':
            listar_emprestimos_vencidos()  # Chama a função de listar empréstimos vencidos
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")


# Iniciar o menu interativo
menu()