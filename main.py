from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
import numpy as np

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(
    "keyfirebase.json")

firebase_admin.initialize_app(cred)
db = firestore.client()


class Imovel(BaseModel):
    tipo: str
    Descricao: str
    valor: float
    rua: str
    andar: Optional[int] = None
    garagens: Optional[int] = None
    condominio: Optional[int] = None


app = FastAPI()

id = db.collection("Imovel").document('IDcasa').get()


@app.get("/git/")
async def redireciona():
    return RedirectResponse("https://github.com/RAS-UFPB")


@app.get("/imoveis/")
def retornaImoveis():
    banco = []
    result = db.collection("Imovel").get()
    for results in result:
        banco.append(results.to_dict())
    return banco


@app.post("/imoveis/")
async def addImoveis(imovel: Imovel):
    db.collection('Imovel').document(imovel.tipo).set(
        {'nome': imovel.tipo, 'descricao': imovel.Descricao, 'valor': imovel.valor, 'rua': imovel.rua, 'andar': imovel.andar, 'garagens': imovel.garagens, 'condominio': imovel.condominio})
    return imovel


@app.delete("/imoveis/")
async def removeDado(colecao: str, documento: str):
    db.collection(colecao).document(documento).delete()
    return "removido"
