## Autores

* Gabriel Dias Vale
* Daniel Jacó Pereira dos Santos
* Evely Paz da Silva

## Como Executar o Projeto

Siga os passos abaixo para configurar e iniciar a aplicação.

**1. Descompacte o arquivo**

Descompacte o arquivo `.zip` do projeto em uma pasta de sua preferência.

**2. Navegue até a pasta do projeto**

Abra um terminal (CMD, PowerShell, Terminal, etc.) e use o comando `cd` para entrar na pasta que você acabou de criar.

```bash
cd caminho/para/a/pasta/do/projeto
```

**3. Crie e Ative um Ambiente Virtual**

É altamente recomendado criar um ambiente virtual para isolar as dependências do projeto.

```bash
# Comando para criar o ambiente virtual
python -m venv .venv
```

Agora, ative o ambiente:

* **No Windows (CMD ou PowerShell):**
    ```bash
    .\.venv\Scripts\activate
    ```

* **No Linux ou macOS:**
    ```bash
    source .venv/bin/activate
    ```

**4. Instale as Dependências**

Com o ambiente virtual ativo, instale todas as bibliotecas necessárias a partir do arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

**5. Povoe o Banco de Dados**

Este projeto não é enviado com os dados pré-existentes. Para criar e popular o banco de dados (`avaliacao.csv`), execute o script de povoamento:

```bash
python populate_db.py
```
Este comando irá criar o arquivo `avaliacao.csv` com os dados iniciais para teste.

**6. Inicie o Servidor da API**

Agora, com tudo pronto, inicie o servidor FastAPI com o Uvicorn:

```bash
uvicorn app.main:app --reload
```

**7. Acesse a Aplicação**

O servidor estará rodando. Abra seu navegador de internet e acesse a seguinte URL:

[**http://127.0.0.1:8000/**](http://127.0.0.1:8000/)

Você será automaticamente redirecionado para a página de documentação interativa (`/docs`), onde poderá testar todos os endpoints da API.

## Visão Geral da API

A documentação interativa e completa está disponível em `/docs` após iniciar o servidor. Os principais recursos incluem:

* **CRUD completo de Avaliações:** Crie, leia, atualize e remova avaliações.
* **Busca:** Filtre avaliações pelo título da mídia.
* **Manutenção:** Limpe registros deletados (`vacuum`) e exporte todos os dados em formato `.zip`.
* **Utilitários:** Gere hashes (MD5, SHA1, SHA256) de qualquer string de dados.