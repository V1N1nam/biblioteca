# config.py

from pymongo import MongoClient

def get_database():
    # Substitua o URI abaixo pela sua string de conexão do MongoDB
    URI = "mongodb://localhost:27017/"
    
    # Conectando ao cliente MongoDB
    client = MongoClient(URI)
    
    # Retorna o banco de dados 'biblioteca'
    return client['biblioteca']
