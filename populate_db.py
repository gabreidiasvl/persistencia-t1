import os
from app.database import MiniDB

def populate():
    db_file = 'avaliacao.csv'
    seq_file = 'avaliacao.seq'
    
    if os.path.exists(db_file):
        os.remove(db_file)
    if os.path.exists(seq_file):
        os.remove(seq_file)
    print("Arquivos de banco de dados antigos removidos.")

    db = MiniDB('avaliacao')

    avaliacoes = [
        {"nome_usuario": "Alice", "titulo_midia": "Parasita", "tipo_midia": "Filme", "estrelas": 5, "comentario": "Uma obra-prima! Chocante e brilhante."},
        {"nome_usuario": "Bruno", "titulo_midia": "Parasita", "tipo_midia": "Filme", "estrelas": 5, "comentario": "Melhor filme do ano, sem dúvidas."},
        {"nome_usuario": "Bruno", "titulo_midia": "Breaking Bad", "tipo_midia": "Série", "estrelas": 5, "comentario": "A melhor série que já assisti."},
        {"nome_usuario": "Carla", "titulo_midia": "Breaking Bad", "tipo_midia": "Série", "estrelas": 4, "comentario": "O final é um pouco lento, mas a jornada vale a pena."},
        {"nome_usuario": "Alice", "titulo_midia": "Attack on Titan", "tipo_midia": "Anime", "estrelas": 5, "comentario": "Insano! A história é complexa e os plot twists são incríveis."},
        {"nome_usuario": "Davi", "titulo_midia": "A Viagem de Chihiro", "tipo_midia": "Filme", "estrelas": 5, "comentario": "Animação perfeita do Studio Ghibli."},
        {"nome_usuario": "Carla", "titulo_midia": "Attack on Titan", "tipo_midia": "Anime", "estrelas": 5, "comentario": "Uma animação de altíssimo nível."}
    ]
    
    print(f"Inserindo {len(avaliacoes)} avaliações...")
    for avaliacao in avaliacoes:
        db.insert(avaliacao)
        
    print("\nPovoamento concluído com sucesso!")
    print(f"Total de avaliações no banco: {db.count()}")

if __name__ == "__main__":
    populate()