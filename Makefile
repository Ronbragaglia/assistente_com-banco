.PHONY: help install install-dev update clean test test-cov lint format type-check run docs build publish docker-build docker-run pre-commit-install

# Variáveis
PYTHON := python
PIP := pip
PYTEST := pytest
BLACK := black
FLAKE8 := flake8
MYPY := mypy
PRE_COMMIT := pre-commit
DOCKER := docker
DOCKER_COMPOSE := docker-compose

# Diretórios
SRC_DIR := src
TESTS_DIR := tests
DOCS_DIR := docs
DIST_DIR := dist
BUILD_DIR := build

# Comandos de ajuda
help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Instalação
install: ## Instala o pacote em modo de desenvolvimento
	$(PIP) install -e .

install-dev: ## Instala o pacote com dependências de desenvolvimento
	$(PIP) install -e ".[dev]"
	$(PRE_COMMIT) install

update: ## Atualiza as dependências
	$(PIP) install --upgrade -e ".[dev]"

# Limpeza
clean: ## Remove arquivos de build e cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.pyd" -delete 2>/dev/null || true
	find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	rm -rf $(DIST_DIR) $(BUILD_DIR) 2>/dev/null || true
	rm -rf htmlcov/ .coverage 2>/dev/null || true
	@echo "✅ Limpeza concluída"

clean-all: clean ## Remove tudo incluindo ambiente virtual
	rm -rf venv/ .venv/ 2>/dev/null || true
	@echo "✅ Limpeza completa concluída"

# Testes
test: ## Executa todos os testes
	$(PYTEST) $(TESTS_DIR) -v

test-cov: ## Executa testes com coverage
	$(PYTEST) $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=html --cov-report=term-missing -v
	@echo "📊 Relatório de coverage gerado em htmlcov/index.html"

test-fast: ## Executa testes rápidos (ignora testes lentos)
	$(PYTEST) $(TESTS_DIR) -v -m "not slow"

test-watch: ## Executa testes em modo watch (requiere pytest-watch)
	pytest-watch $(TESTS_DIR)

# Lint e Formatação
lint: ## Executa verificação de lint com flake8
	$(FLAKE8) $(SRC_DIR) $(TESTS_DIR) examples/

format: ## Formata o código com black e isort
	$(BLACK) $(SRC_DIR) $(TESTS_DIR) examples/
	isort $(SRC_DIR) $(TESTS_DIR) examples/

format-check: ## Verifica se o código está formatado corretamente
	$(BLACK) --check $(SRC_DIR) $(TESTS_DIR) examples/
	isort --check-only $(SRC_DIR) $(TESTS_DIR) examples/

type-check: ## Executa verificação de tipos com mypy
	$(MYPY) $(SRC_DIR)

# Pre-commit
pre-commit-install: ## Instala os hooks de pre-commit
	$(PRE_COMMIT) install

pre-commit-run: ## Executa todos os hooks de pre-commit
	$(PRE_COMMIT) run --all-files

pre-commit-update: ## Atualiza os hooks de pre-commit
	$(PRE-commit) autoupdate

# Execução
run: ## Executa o assistente em modo interativo
	db-assistant --interactive

run-ask: ## Executa uma pergunta única (use: make run-ask QUESTION="sua pergunta")
	@if [ -z "$(QUESTION)" ]; then \
		echo "Por favor, forneça uma pergunta: make run-ask QUESTION='sua pergunta'"; \
		exit 1; \
	fi
	db-assistant --ask "$(QUESTION)"

# Documentação
docs: ## Gera a documentação (requiere Sphinx)
	cd $(DOCS_DIR) && make html

docs-serve: ## Serve a documentação localmente
	cd $(DOCS_DIR) && make livehtml

# Build e Publicação
build: ## Constrói o pacote para distribuição
	$(PYTHON) -m build

publish-test: ## Publica no PyPI de teste
	twine upload --repository testpypi $(DIST_DIR)/*

publish: ## Publica no PyPI
	twine upload $(DIST_DIR)/*

# Docker
docker-build: ## Constrói a imagem Docker
	$(DOCKER) build -t openai-database-assistant .

docker-run: ## Executa o container Docker
	$(DOCKER) run -it --rm \
		-v $(PWD)/data:/app/data \
		-v $(PWD)/logs:/app/logs \
		openai-database-assistant

docker-compose-up: ## Inicia os serviços com docker-compose
	$(DOCKER_COMPOSE) up -d

docker-compose-down: ## Para os serviços com docker-compose
	$(DOCKER_COMPOSE) down

docker-compose-logs: ## Mostra os logs dos serviços
	$(DOCKER_COMPOSE) logs -f

# CI/CD
ci: lint type-check test-cov ## Executa todos os checks de CI (lint, type-check, test-cov)

# Utilitários
setup: ## Configura o ambiente de desenvolvimento completo
	@echo "🚀 Configurando ambiente de desenvolvimento..."
	$(MAKE) install-dev
	$(MAKE) pre-commit-install
	@echo "✅ Ambiente configurado com sucesso!"

check-all: format-check lint type-check test ## Executa todas as verificações
	@echo "✅ Todas as verificações passaram!"

# Informações
info: ## Mostra informações sobre o ambiente
	@echo "📋 Informações do Ambiente:"
	@echo "  Python: $$($(PYTHON) --version)"
	@echo "  Pip: $$($(PIP) --version)"
	@echo "  Diretório do projeto: $$(pwd)"
	@echo "  Diretório de origem: $(SRC_DIR)"
	@echo "  Diretório de testes: $(TESTS_DIR)"

# Backup
backup-db: ## Faz backup do banco de dados
	@mkdir -p backups
	@if [ -f "data/eventos.db" ]; then \
		cp data/eventos.db backups/eventos_$$(date +%Y%m%d_%H%M%S).db; \
		echo "✅ Backup criado em backups/"; \
	else \
		echo "⚠️  Banco de dados não encontrado"; \
	fi

restore-db: ## Restaura o banco de dados mais recente
	@if [ -d "backups" ]; then \
		LATEST=$$(ls -t backups/*.db 2>/dev/null | head -1); \
		if [ -n "$$LATEST" ]; then \
			cp "$$LATEST" data/eventos.db; \
			echo "✅ Banco de dados restaurado de $$LATEST"; \
		else \
			echo "⚠️  Nenhum backup encontrado"; \
		fi \
	else \
		echo "⚠️  Diretório de backups não encontrado"; \
	fi

# Estatísticas
stats: ## Mostra estatísticas do código
	@echo "📊 Estatísticas do Código:"
	@echo "  Linhas de Python: $$(find $(SRC_DIR) -name '*.py' -exec cat {} \; | wc -l)"
	@echo "  Arquivos Python: $$(find $(SRC_DIR) -name '*.py' | wc -l)"
	@echo "  Linhas de Testes: $$(find $(TESTS_DIR) -name '*.py' -exec cat {} \; | wc -l)"
	@echo "  Arquivos de Testes: $$(find $(TESTS_DIR) -name '*.py' | wc -l)"
