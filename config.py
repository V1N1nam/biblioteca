from pymongo import MongoClient

def get_database():
    # URI segura para conexão ao MongoDB
    URI = "mongodb+srv://V1N1_nam:19092001Vi@cluster0.mthqg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    try:
        # Conectando ao cliente MongoDB
        client = MongoClient(URI)
        
        # Imprime a mensagem de sucesso
        print("Conectado ao MongoDB com sucesso!")
        
        # Retorna o banco de dados 'biblioteca'
        return client['biblioteca']
    
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        return None
