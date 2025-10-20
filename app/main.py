from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.responses import HTMLResponse 
from typing import List
from app.database import MiniDB
from app.models import Avaliacao, AvaliacaoCreate, AvaliacaoUpdate
from fastapi.responses import HTMLResponse, RedirectResponse
import zipfile
import io
import hashlib
from fastapi.responses import StreamingResponse

app = FastAPI(
    title="API de Avaliações de Mídias",
    description="Uma API focada em criar e gerenciar avaliações de mídias.",
    version="3.0.0",
    docs_url=None, 
    redoc_url=None
)

db = MiniDB('avaliacao')
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
@app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
async def custom_swagger_ui_html():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <title>Documentação da API - Avaliações de Mídias</title>
        <style>
            body { margin: 0; padding: 0; }
            .swagger-ui .topbar { background-color: #2c3e50; }
            .swagger-ui .topbar .link img { content: url('https://i.imgur.com/8E3A6J4.png'); width: 120px; }
            #custom-logo-container { text-align: center; padding: 20px; background-color: #f7f7f7; }
        </style>
    </head>
    <body>
        <div id="custom-logo-container">
            <img src="https://png.pngtree.com/png-vector/20240621/ourmid/pngtree-gaming-5-star-rating-vector-png-image_12804957.png" alt="Logo Avaliações" style="max-height: 280px;">
        </div>
        
        <div id="swagger-ui"></div>
        
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            const ui = SwaggerUIBundle({
                url: '/openapi.json', // Pede ao FastAPI o "mapa" da API
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout"
            })
        </script>
    </body>
    </html>
    """)

@app.post("/avaliacoes/", response_model=Avaliacao, status_code=201, summary="Criar uma nova avaliação", tags=["1. Criar (POST)"])
def create_avaliacao(avaliacao: AvaliacaoCreate):
    return db.insert(avaliacao.dict())
@app.get("/avaliacoes/", response_model=List[Avaliacao], summary="Listar todas as avaliações", tags=["2. Ler (GET)"])
def get_avaliacoes(page: int = 1, page_size: int = 10):
    return db.get_all(page=page, page_size=page_size)

@app.get("/avaliacoes/buscar/", response_model=List[Avaliacao], summary="Buscar avaliações por título da mídia", tags=["2. Ler (GET)"])
def search_avaliacoes(titulo: str = Query(..., description="Parte do título da mídia para buscar")):
    return db.search_by_title(titulo)

@app.get("/avaliacoes/{avaliacao_id}", response_model=Avaliacao, summary="Obter uma avaliação por ID", tags=["2. Ler (GET)"])
def get_avaliacao(avaliacao_id: int):
    avaliacao = db.get_by_id(avaliacao_id)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return avaliacao
    
@app.get("/avaliacoes/contar", summary="Contar total de avaliações", tags=["2. Ler (GET)"])
def count_avaliacoes():
    return {"total_avaliacoes": db.count()}


@app.put("/avaliacoes/{avaliacao_id}", response_model=Avaliacao, summary="Atualizar uma avaliação", tags=["3. Atualizar (PUT)"])
def update_avaliacao(avaliacao_id: int, avaliacao_update: AvaliacaoUpdate):
    updated = db.update(avaliacao_id, avaliacao_update.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada para atualização")
    return updated

@app.delete("/avaliacoes/{avaliacao_id}", status_code=204, summary="Remover uma avaliação", tags=["4. Remover (DELETE)"])
def delete_avaliacao(avaliacao_id: int):
    success = db.soft_delete(avaliacao_id)
    if not success:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada para remoção")
    return Response(status_code=204)
@app.post("/manutencao/vacuum", status_code=200, summary="Limpar registros deletados", tags=["5. Manutenção"])
def vacuum_db():
    db.vacuum()
    return {"message": "Operação de vacuum concluída com sucesso."}
 
@app.get("/exportar/avaliacoes.zip", summary="Exportar dados como CSV compactado", tags=["5. Manutenção"])
def export_avaliacoes_zip():
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(db.csv_file, arcname="avaliacoes.csv")

    return StreamingResponse(
        iter([zip_buffer.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename=avaliacoes_export.zip"}
    )
@app.post("/utilitarios/hash", summary="Gerar hash de um dado", tags=["6. Utilitários"])
def generate_hash(data: str = Query(..., description="O dado a ser processado"), 
                  algorithm: str = Query("sha256", enum=["md5", "sha1", "sha256"])):

    hasher = hashlib.new(algorithm)
    hasher.update(data.encode('utf-8'))
    return {"original_data": data, "algorithm": algorithm, "hashed_value": hasher.hexdigest()}