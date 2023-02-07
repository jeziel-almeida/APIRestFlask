from itertools import count
from typing import Optional

from flask import Flask, jsonify, request
from flask_pydantic_spec import FlaskPydanticSpec, Request, Response
from pydantic import BaseModel, Field
from tinydb import Query, TinyDB

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Live de Python')
spec.register(server)
database = TinyDB('database.json')
c = count()


class Pessoa(BaseModel):
    id: Optional[int] = Field(default_factory=lambda: next(c))
    nome: str
    idade: int


class Pessoas(BaseModel):
    pessoas: list[Pessoa]
    count: int


@server.get('/pessoas')
@spec.validate(resp=Response(HTTP_200=Pessoas))
def buscar_pessoas():
    """Retorna todas as pessoas do banco de dados."""
    return jsonify(
        Pessoas(pessoas=database.all(), count=len(database.all())).dict()
    )


@server.post('/pessoas')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_201=Pessoa))
def inserir_pessoa():
    """Insere uma Pessoa no banco de dados."""
    body = request.context.body.dict()
    database.insert(body)
    return body


@server.put('/pessoas/<int:id>')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_200=Pessoa))
def altera_pessoa(id):
    """Altera uma Pessoa no banco de dados."""
    body = request.context.body.dict()
    database.update(body, Query().id == id)
    return jsonify(body)


@server.delete('/pessoas/<int:id>')
@spec.validate(resp=Response('HTTP_204'))
def deleta_pessoa(id):
    """Deleta uma Pessoa no banco de dados."""
    database.remove(Query().id == id)
    return jsonify({})


server.run()
