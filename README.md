# TechFlow Task Manager 🗂️

Sistema de gerenciamento de tarefas desenvolvido para a startup de logística LogiRun,
utilizando metodologia ágil Kanban. Projeto acadêmico da disciplina de Engenharia de Software — UniFECAF.

## 📋 Objetivo

Desenvolver um sistema web que permita acompanhar o fluxo de trabalho em tempo real,
priorizar tarefas críticas e monitorar o desempenho da equipe.

## 🎯 Escopo Inicial

- Cadastro, listagem, edição e exclusão de tarefas (CRUD completo)
- Definição de prioridade (Alta, Média, Baixa)
- Status das tarefas (A Fazer, Em Progresso, Concluído)
- Interface web simples e funcional

## ⚙️ Tecnologias

- **Linguagem:** Python 3.11
- **Framework:** Flask
- **Banco de dados:** SQLite
- **Testes:** Pytest
- **CI/CD:** GitHub Actions

## 🚀 Como executar

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/techflow-task-manager.git
cd techflow-task-manager

# Instale as dependências
pip install -r requirements.txt

# Execute o sistema
python src/app.py
```

Acesse em: http://localhost:5000

## 📁 Estrutura do projeto
techflow-task-manager/
├── src/          # Código fonte principal
├── tests/        # Testes automatizados
├── docs/         # Documentação e diagramas UML
└── README.md
## 🔄 Metodologia

Este projeto adota a metodologia **Kanban**, com o quadro de tarefas gerenciado
via GitHub Projects, organizado nas colunas: **A Fazer**, **Em Progresso** e **Concluído**.
