from dataclasses import dataclass
from typing import List

@dataclass
class VotacaoItem:
    nome: str
    quantidade: int
    percentual: float
    grupo: str
    municipio: str

@dataclass
class VotacaoPorMunicipio:
    estim1_pref: List[VotacaoItem]
    espontanea: List[VotacaoItem]