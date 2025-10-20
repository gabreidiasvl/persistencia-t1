from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class AvaliacaoBase(BaseModel):
    nome_usuario: str = Field(..., description="Nome do usuário que fez a avaliação")
    titulo_midia: str = Field(..., description="Título do filme, série ou anime avaliado")
    tipo_midia: str = Field(..., description="Tipo da mídia (Filme, Série, Anime)")
    estrelas: int = Field(..., ge=1, le=5, description="Nota em estrelas, de 1 a 5")
    comentario: Optional[str] = Field(None, description="Comentário sobre a mídia")

class AvaliacaoCreate(AvaliacaoBase):
    pass

class AvaliacaoUpdate(BaseModel):
    estrelas: int = Field(..., ge=1, le=5, description="Nova nota em estrelas")
    comentario: Optional[str] = Field(None, description="Novo comentário") 

class Avaliacao(AvaliacaoBase):
    id: int
    deleted: bool
    model_config = ConfigDict(from_attributes=True)