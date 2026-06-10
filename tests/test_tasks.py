import sys
import os
import pytest

# Adiciona a pasta src ao caminho para importar os módulos
import pytest
import src.app as flask_app
import src.database as database

import src.app as flask_app
import src.database as database

# ── Configuração dos testes ──────────────────────────────

@pytest.fixture
def client():
    """Cria um cliente de teste com banco de dados temporário."""
    database.DATABASE = ':memory:'  # Usa banco em memória (não salva arquivos)
    flask_app.app.config['TESTING'] = True

    with flask_app.app.test_client() as client:
        with flask_app.app.app_context():
            database.init_db()
        yield client

# ── Testes de CREATE ─────────────────────────────────────

def test_criar_tarefa_com_sucesso(client):
    """Deve criar uma tarefa e retornar status 201."""
    resposta = client.post('/tasks', json={
        'title': 'Tarefa de teste',
        'status': 'A Fazer',
        'priority': 'Alta'
    })
    assert resposta.status_code == 201
    dados = resposta.get_json()
    assert dados['title'] == 'Tarefa de teste'
    assert dados['priority'] == 'Alta'

def test_criar_tarefa_sem_titulo(client):
    """Deve retornar erro 400 quando o título estiver vazio."""
    resposta = client.post('/tasks', json={'title': ''})
    assert resposta.status_code == 400
    assert 'error' in resposta.get_json()

# ── Testes de READ ───────────────────────────────────────

def test_listar_tarefas_vazia(client):
    """Deve retornar lista vazia quando não há tarefas."""
    resposta = client.get('/tasks')
    assert resposta.status_code == 200
    assert resposta.get_json() == []

def test_listar_tarefas_com_dados(client):
    """Deve retornar a tarefa criada na listagem."""
    client.post('/tasks', json={'title': 'Tarefa listada'})
    resposta = client.get('/tasks')
    dados = resposta.get_json()
    assert len(dados) == 1
    assert dados[0]['title'] == 'Tarefa listada'

# ── Testes de UPDATE ─────────────────────────────────────

def test_atualizar_tarefa(client):
    """Deve atualizar o status de uma tarefa existente."""
    client.post('/tasks', json={'title': 'Tarefa para editar'})
    resposta = client.put('/tasks/1', json={'status': 'Em Progresso'})
    assert resposta.status_code == 200
    assert resposta.get_json()['status'] == 'Em Progresso'

def test_atualizar_tarefa_inexistente(client):
    """Deve retornar 404 ao tentar atualizar tarefa que não existe."""
    resposta = client.put('/tasks/999', json={'title': 'Não existe'})
    assert resposta.status_code == 404

# ── Testes de DELETE ─────────────────────────────────────

def test_deletar_tarefa(client):
    """Deve remover uma tarefa e confirmar com mensagem."""
    client.post('/tasks', json={'title': 'Tarefa para deletar'})
    resposta = client.delete('/tasks/1')
    assert resposta.status_code == 200
    assert 'removida' in resposta.get_json()['message']

def test_deletar_tarefa_inexistente(client):
    """Deve retornar 404 ao tentar deletar tarefa que não existe."""
    resposta = client.delete('/tasks/999')
    assert resposta.status_code == 404
