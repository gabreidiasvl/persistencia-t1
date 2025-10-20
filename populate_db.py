import os
import random
from faker import Faker
from app.database import MiniDB

def populate(num_records=1000):
    db_file = 'avaliacao.csv'
    seq_file = 'avaliacao.seq'
    
    if os.path.exists(db_file):
        os.remove(db_file)
    if os.path.exists(seq_file):
        os.remove(seq_file)
    print("Arquivos de banco de dados antigos removidos.")

    db = MiniDB('avaliacao')
    fake = Faker('pt_BR')

    midias_reais = [
        {"titulo": "O Poderoso Chefão", "tipo": "Filme"}, {"titulo": "Pulp Fiction", "tipo": "Filme"},
        {"titulo": "O Senhor dos Anéis: O Retorno do Rei", "tipo": "Filme"}, {"titulo": "Batman: O Cavaleiro das Trevas", "tipo": "Filme"},
        {"titulo": "A Origem", "tipo": "Filme"}, {"titulo": "Parasita", "tipo": "Filme"},
        {"titulo": "Matrix", "tipo": "Filme"}, {"titulo": "Cidade de Deus", "tipo": "Filme"},
        {"titulo": "A Viagem de Chihiro", "tipo": "Filme"}, {"titulo": "Interestelar", "tipo": "Filme"},
        {"titulo": "Breaking Bad", "tipo": "Série"}, {"titulo": "Game of Thrones", "tipo": "Série"},
        {"titulo": "Stranger Things", "tipo": "Série"}, {"titulo": "The Office", "tipo": "Série"},
        {"titulo": "Black Mirror", "tipo": "Série"}, {"titulo": "Dark", "tipo": "Série"},
        {"titulo": "Attack on Titan", "tipo": "Anime"}, {"titulo": "Death Note", "tipo": "Anime"},
        {"titulo": "Fullmetal Alchemist: Brotherhood", "tipo": "Anime"}, {"titulo": "Demon Slayer", "tipo": "Anime"},
        {"titulo": "Naruto", "tipo": "Anime"}, {"titulo": "Jujutsu Kaisen", "tipo": "Anime"},
        {"titulo": "Avenida Brasil", "tipo": "Novela"}, {"titulo": "O Clone", "tipo": "Novela"},
        {"titulo": "Senhora do Destino", "tipo": "Novela"}, {"titulo": "Vale Tudo", "tipo": "Novela"}
    ]

    comentarios_por_nota = {
        5: ["Perfeito! Uma obra-prima.", "Incrível, assistiria de novo.", "Recomendo para todo mundo!", "Sensacional!", "Top 10 da minha vida."],
        4: ["Muito bom, gostei bastante.", "Quase perfeito, vale muito a pena.", "Ótima história e personagens.", "Surpreendeu positivamente."],
        3: ["Bom, mas nada de especial.", "Divertido para passar o tempo.", "É ok, mas não me marcou.", "Tem seus altos e baixos."],
        2: ["Não gostei muito.", "Achei a premissa fraca.", "Esperava bem mais, foi uma decepção.", "Não funcionou pra mim."],
        1: ["Péssimo, perdi meu tempo.", "Não recomendo de jeito nenhum.", "Terrível, um dos piores que já vi.", "Muito ruim."]
    }

    print(f"Gerando e inserindo {num_records} avaliações...")

    for i in range(num_records):
        midia_sorteada = random.choice(midias_reais)
        
        nota = random.randint(1, 5)
        comentario_aleatorio = random.choice(comentarios_por_nota[nota])

        avaliacao = {
            "nome_usuario": fake.name(),
            "titulo_midia": midia_sorteada["titulo"],
            "tipo_midia": midia_sorteada["tipo"],
            "estrelas": nota,
            "comentario": comentario_aleatorio
        }
        
        db.insert(avaliacao)
        if (i + 1) % 100 == 0:
            print(f"  {i + 1}/{num_records} registros inseridos.")

    print("\nPovoamento em massa concluído com sucesso!")
    print(f"Total de avaliações no banco: {db.count()}")

if __name__ == "__main__":
    populate()