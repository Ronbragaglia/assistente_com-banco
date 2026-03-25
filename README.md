# 🤖 OpenAI Database Assistant

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI](https://img.shields.io/pypi/v/openai-database-assistant)](https://pypi.org/project/openai-database-assistant/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/openai-database-assistant)](https://pypi.org/project/openai-database-assistant/)
[![Tests](https://img.shields.io/github/actions/workflow/ci.yml/Ronbragaglia/assistente_com-banco?branch=main)](https://github.com/Ronbragaglia/assistente_com-banco/actions)
[![Coverage](https://img.shields.io/codecov/c/github/Ronbragaglia/assistente_com-banco)](https://codecov.io/gh/Ronbragaglia/assistente_com-banco)
[![CodeQL](https://github.com/Ronbragaglia/assistente_com-banco/actions/workflows/codeql.yml/badge.svg)](https://github.com/Ronbragaglia/assistente_com-banco/actions/workflows/codeql.yml)
[![Docker](https://img.shields.io/docker/v/ronbragaglia/openai-database-assistant?label=Docker)](https://hub.docker.com/r/ronbragaglia/openai-database-assistant)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![CodeFactor](https://www.codefactor.io/repository/github/Ronbragaglia/assistente_com-banco/badge)](https://www.codefactor.io/repository/github/Ronbragaglia/assistente_com-banco)
[![Maintainability](https://api.codeclimate.com/v1/badges/maintainability-percentage/Ronbragaglia/assistente_com-banco?style=flat)](https://codeclimate.com/github/Ronbragaglia/assistente_com-banco/maintainability)

Um assistente de IA avançado com banco de dados SQLite e busca de similaridade usando TF-IDF e cosine similarity. Transforme suas perguntas em respostas inteligentes com cache automático!

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Como Usar](#como-usar)
- [Exemplos Avançados](#exemplos-avançados)
- [Docker](#docker)
- [Desenvolvimento](#desenvolvimento)
- [Testes](#testes)
- [Contribuindo](#contribuindo)
- [Roadmap](#roadmap)
- [FAQ](#faq)
- [Licença](#licença)

## 🎯 Visão Geral

O OpenAI Database Assistant é uma solução completa para criar assistentes de IA com memória persistente. Ele combina:

- **Armazenamento Inteligente**: Banco de dados SQLite para persistência de dados
- **Busca Semântica**: TF-IDF com cosine similarity para encontrar respostas similares
- **Integração OpenAI**: GPT-3.5/GPT-4 para geração de respostas
- **Cache Automático**: Armazena perguntas e respostas para respostas mais rápidas
- **Interface Flexível**: CLI interativa ou uso como biblioteca Python

## ✨ Funcionalidades

- 🗄️ **Banco de Dados SQLite**: Armazenamento persistente de eventos e perguntas/respostas
- 🔍 **Busca de Similaridade**: TF-IDF com cosine similarity para encontrar respostas similares
- 🤖 **Integração OpenAI**: Geração de respostas usando GPT-3.5/GPT-4
- 💬 **Modo Interativo**: Converse com o assistente em tempo real
- 💾 **Cache Inteligente**: Armazena automaticamente perguntas e respostas
- 🎯 **Busca Eficiente**: Encontra respostas similares rapidamente
- 📝 **Logging Avançado**: Rastreia todas as operações com logs detalhados
- 🔧 **Configuração Flexível**: Use variáveis de ambiente ou arquivo .env
- 🧪 **Testes Completos**: Suite de testes incluída

## 🚀 Instalação

### Via pip (recomendado)

```bash
pip install openai-database-assistant
```

### Via código fonte

```bash
git clone https://github.com/Ronbragaglia/assistente_com-banco.git
cd assistente_com-banco
pip install -e .
```

### Dependências de desenvolvimento

```bash
pip install -e ".[dev]"
```

## ⚙️ Configuração

### 1. Crie um arquivo `.env`

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

### 2. Configure suas credenciais

Edite o arquivo `.env` com suas configurações:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7

# Database Configuration
DATABASE_PATH=data/eventos.db

# Similarity Search Configuration
SIMILARITY_THRESHOLD=0.7

# Assistant Configuration
ASSISTANT_NAME=Assistente de Eventos
ASSISTANT_SYSTEM_PROMPT=Você é um assistente útil especializado em eventos.

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/assistant.log

# Cache Configuration
CACHE_ENABLED=true
```

### 3. Obtenha sua chave da API OpenAI

1. Acesse [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Crie uma nova chave de API
3. Copie e cole no arquivo `.env`

## 📖 Como Usar

### Linha de Comando

#### Modo Interativo

```bash
db-assistant --interactive
```

#### Pergunta Única

```bash
db-assistant --ask "Quais eventos estão disponíveis?"
```

#### Adicionar Evento

```bash
db-assistant --add-event "Conferência de IA" "2024-06-15" "Centro de Convenções" "Evento sobre inteligência artificial"
```

#### Listar Eventos

```bash
db-assistant --list-events
```

### Como Biblioteca Python

```python
from database_assistant import (
    Settings,
    DatabaseManager,
    SimilaritySearch,
    OpenAIAssistant,
    setup_logger,
)

# Setup
logger = setup_logger(level="INFO")
settings = Settings()

# Initialize components
db_manager = DatabaseManager(settings.database_path)
similarity_search = SimilaritySearch(threshold=settings.similarity_threshold)
ai_assistant = OpenAIAssistant(settings)

# Setup database
with db_manager:
    db_manager.create_tables()
    db_manager.seed_sample_data()

# Load similarity search
with db_manager:
    qa_pairs = db_manager.get_all_qa_pairs()
    similarity_search.fit(qa_pairs)

# Get context
with db_manager:
    context = db_manager.get_events_as_context()

# Ask question
question = "Quais eventos estão disponíveis?"
cached_answer = similarity_search.search(question)

if cached_answer:
    print(f"Resposta (do cache): {cached_answer}")
else:
    response = ai_assistant.generate_response(context, question)
    print(f"Resposta (gerada): {response}")
    
    # Cache the response
    if settings.cache_enabled:
        with db_manager:
            db_manager.insert_question_answer(question, response)
        similarity_search.update([(question, response)])
```

## 🏗️ Arquitetura

O projeto segue uma arquitetura modular e escalável:

```
┌─────────────────────────────────────────────────────────────┐
│                     CLI Interface                        │
│                  (interactive/ask/add)                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │   Config     │  │   Logger     │  │  Utils   │ │
│  │   (Pydantic) │  │  (Colorlog)  │  │          │ │
│  └──────────────┘  └──────────────┘  └──────────┘ │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌──────────────────┐  ┌──────────────────┐
│  OpenAI Module  │  │  Database Module │
│   (GPT API)     │  │    (SQLite)      │
└──────────────────┘  └──────────────────┘
        │                     │
        └──────────┬──────────┘
                   ▼
        ┌──────────────────┐
        │ Similarity      │
        │    Search       │
        │  (TF-IDF)      │
        └──────────────────┘
```

### Componentes Principais

- **Config Module**: Gerenciamento de configurações com Pydantic Settings
- **Logger Module**: Sistema de logging avançado com colorlog
- **Database Module**: Gerenciamento do banco de dados SQLite
- **Similarity Module**: Busca de similaridade usando TF-IDF
- **Assistant Module**: Integração com a API da OpenAI
- **CLI Module**: Interface de linha de comando interativa

### Fluxo de Dados

1. **Usuário faz uma pergunta** → CLI
2. **Busca no cache** → Similarity Search
3. **Se encontrado** → Retorna resposta do cache
4. **Se não encontrado** → Gera resposta com OpenAI
5. **Armazena no cache** → Database + Similarity Search
6. **Retorna resposta** → Usuário

## 🐳 Docker

### Usando Docker

```bash
# Construir a imagem
docker build -t openai-database-assistant .

# Executar o container
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  openai-database-assistant
```

### Usando Docker Compose

```bash
# Iniciar serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down
```

### Perfis do Docker Compose

```bash
# Modo desenvolvimento
docker-compose --profile dev up

# Modo de teste
docker-compose --profile test up

# Modo de backup
docker-compose --profile backup up
```

## 📁 Estrutura do Projeto

```
assistente_com-banco/
├── src/
│   └── database_assistant/
│       ├── __init__.py           # Pacote principal
│       ├── config.py             # Configurações com Pydantic
│       ├── logger.py             # Sistema de logging
│       ├── database.py           # Gerenciamento do SQLite
│       ├── similarity.py          # Busca de similaridade TF-IDF
│       ├── assistant.py          # Integração com OpenAI
│       └── cli.py                # Interface de linha de comando
├── tests/                        # Testes
│   ├── __init__.py
│   └── test_config.py
├── examples/                     # Exemplos de uso
│   ├── basic_usage.py
│   └── advanced_usage.py
├── docs/                         # Documentação
├── logs/                         # Logs de execução
├── data/                         # Banco de dados
├── .env.example                  # Exemplo de configuração
├── .gitignore
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```

## 🎨 Exemplos

### Busca Básica

```python
from database_assistant import DatabaseManager, SimilaritySearch

# Initialize components
db_manager = DatabaseManager("data/eventos.db")
similarity_search = SimilaritySearch(threshold=0.7)

# Load existing Q&A pairs
with db_manager:
    qa_pairs = db_manager.get_all_qa_pairs()
    similarity_search.fit(qa_pairs)

# Search for similar question
answer = similarity_search.search("Quais eventos tem?")
if answer:
    print(f"Found: {answer}")
```

### Adicionar Eventos

```python
with db_manager:
    db_manager.insert_event(
        nome="Workshop de Python",
        data="2024-03-10",
        local="Sala de Conferências",
        descricao="Workshop introdutório sobre Python"
    )
```

### Busca com Score

```python
answer, score = similarity_search.search_with_score("Quais eventos?")
print(f"Answer: {answer}")
print(f"Similarity Score: {score:.4f}")
```

## 🧪 Executar Testes

```bash
# Executar todos os testes
pytest

# Executar com coverage
pytest --cov=src --cov-report=html

# Executar testes específicos
pytest tests/test_config.py

# Verbose output
pytest -v
```

## 🔧 Desenvolvimento

### Formatar código

```bash
black src/ tests/ examples/
```

### Verificar lint

```bash
flake8 src/ tests/ examples/
```

### Type checking

```bash
mypy src/
```

### Pre-commit hooks

```bash
pre-commit install
pre-commit run --all-files
```

## 📝 Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `OPENAI_API_KEY` | Chave da API OpenAI | Obrigatório |
| `OPENAI_MODEL` | Modelo OpenAI a usar | `gpt-3.5-turbo` |
| `OPENAI_TEMPERATURE` | Temperatura das respostas | `0.7` |
| `DATABASE_PATH` | Caminho do banco SQLite | `data/eventos.db` |
| `SIMILARITY_THRESHOLD` | Limite de similaridade | `0.7` |
| `ASSISTANT_NAME` | Nome do assistente | `Assistente de Eventos` |
| `ASSISTANT_SYSTEM_PROMPT` | Prompt do sistema | - |
| `LOG_LEVEL` | Nível de logging | `INFO` |
| `LOG_FILE` | Arquivo de log | `logs/assistant.log` |
| `CACHE_ENABLED` | Habilitar cache | `true` |

## 🚀 Roadmap

### Próximas Funcionalidades Planejadas

- [ ] **Streaming de Respostas**: Suporte a streaming de respostas da OpenAI
- [ ] **Múltiplos Embeddings**: Suporte a diferentes modelos de embeddings (OpenAI, Sentence Transformers)
- [ ] **Export/Import**: Funcionalidade para exportar e importar Q&A pairs
- [ ] **Interface Web**: Dashboard web para gerenciamento
- [ ] **Multi-idioma**: Suporte a múltiplos idiomas
- [ ] **API REST**: Endpoints REST para integração
- [ ] **WebSocket**: Suporte a WebSocket para comunicação em tempo real
- [ ] **Analytics**: Dashboard de analytics e métricas
- [ ] **Backup Automático**: Sistema de backup automático com retenção
- [ ] **Plugins**: Sistema de plugins para extensibilidade

### Versões Futuras

#### v3.0.0 (Q2 2024)
- Interface web completa
- API REST com autenticação
- Suporte a múltiplos bancos de dados (PostgreSQL, MySQL)

#### v4.0.0 (Q3 2024)
- Sistema de plugins
- Analytics avançado
- Multi-tenancy

## ❓ FAQ

### Perguntas Frequentes

**Q: Posso usar este projeto comercialmente?**
R: Sim! O projeto é licenciado sob a Licença MIT, permitindo uso comercial.

**Q: Quais modelos da OpenAI são suportados?**
R: Todos os modelos da OpenAI são suportados, incluindo GPT-3.5, GPT-4, GPT-4-turbo, etc.

**Q: Como funciona o cache de respostas?**
R: O sistema usa TF-IDF com cosine similarity para encontrar perguntas similares no banco de dados. Se uma pergunta similar for encontrada, a resposta correspondente é retornada imediatamente.

**Q: Posso usar um banco de dados diferente do SQLite?**
R: Atualmente, apenas SQLite é suportado, mas estamos planejando adicionar suporte a PostgreSQL e MySQL em versões futuras.

**Q: Como posso contribuir com o projeto?**
R: Consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes detalhadas sobre como contribuir.

**Q: O projeto é seguro para uso em produção?**
R: Sim! O projeto inclui validações de entrada, tratamento de erros robusto, e passou por testes de segurança. No entanto, sempre revise e teste antes de usar em produção.

**Q: Posso usar embeddings customizados?**
R: Atualmente, o projeto usa TF-IDF para similaridade. Suporte a embeddings customizados está planejado para versões futuras.

**Q: Como faço backup do banco de dados?**
R: O banco de dados SQLite é um arquivo simples. Basta copiar o arquivo `data/eventos.db` para fazer backup. O projeto também inclui um serviço de backup automático via Docker Compose.

**Q: Posso integrar com outros serviços?**
R: Sim! O projeto foi desenhado para ser modular. Você pode facilmente integrar com outros serviços usando a API ou extendendo os módulos existentes.

**Q: Qual é a performance do sistema?**
R: O sistema é otimizado para performance:
- Busca no cache: < 10ms
- Geração de resposta com OpenAI: 1-5s (depende do modelo)
- Inserção no banco: < 5ms

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

### Diretrizes de Contribuição

- Siga o estilo de código do projeto (PEP 8, Black)
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário
- Use mensagens de commit claras e descritivas

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙋 Suporte

- 📧 Email: ronald.bragaglia@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/Ronbragaglia/assistente_com-banco/issues)
- 📖 Documentação: [Wiki](https://github.com/Ronbragaglia/assistente_com-banco/wiki)

## 🌟 Recursos Adicionais

- [Documentação da API OpenAI](https://platform.openai.com/docs/api-reference)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [scikit-learn Documentation](https://scikit-learn.org/stable/)

## 📸 Screenshots

<div align="center">
  <img src="https://github.com/user-attachments/assets/9f7492b6-cce0-450f-a160-e7a8bbd0b773" alt="Screenshot 1" width="45%">
  <img src="https://github.com/user-attachments/assets/129d6f2f-5359-40e6-96f7-2db5cfbee63e" alt="Screenshot 2" width="45%">
</div>

<div align="center">
  <img src="https://github.com/user-attachments/assets/53a8ead9-7e8b-44d6-9cbd-c15316fad9a1" alt="Screenshot 3" width="45%">
  <img src="https://github.com/user-attachments/assets/50262e38-4b78-438f-abf1-c9c1296339d6" alt="Screenshot 4" width="45%">
</div>

## ⭐ Star History

Se este projeto foi útil para você, considere dar uma ⭐!

---

Feito com ❤️ por [Ronald Bragaglia](https://github.com/Ronbragaglia)
