# Contribuindo para o OpenAI Database Assistant

Obrigado por considerar contribuir com o OpenAI Database Assistant! Este documento fornece diretrizes e informações sobre como contribuir para o projeto.

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Começar](#como-começar)
- [Processo de Desenvolvimento](#processo-de-desenvolvimento)
- [Diretrizes de Código](#diretrizes-de-código)
- [Testes](#testes)
- [Documentação](#documentação)
- [Reportando Bugs](#reportando-bugs)
- [Sugerindo Melhorias](#sugerindo-melhorias)
- [Pull Requests](#pull-requests)

## 🤝 Código de Conduta

Este projeto adota o [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/). Ao participar, você deve manter este código. Por favor, reporte comportamento inaceitável para [ronald.bragaglia@example.com](mailto:ronald.bragaglia@example.com).

## 🚀 Como Começar

### Pré-requisitos

- Python 3.9 ou superior
- pip ou poetry
- Git

### Configuração do Ambiente de Desenvolvimento

1. **Fork o repositório**

   ```bash
   # Clique no botão "Fork" no GitHub
   # Clone seu fork
   git clone https://github.com/SEU_USUARIO/assistente_com-banco.git
   cd assistente_com-banco
   ```

2. **Crie um ambiente virtual**

   ```bash
   # Usando venv
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows

   # Usando poetry
   poetry install
   ```

3. **Instale as dependências de desenvolvimento**

   ```bash
   # Usando pip
   pip install -e ".[dev]"

   # Usando poetry
   poetry install --with dev
   ```

4. **Configure o pre-commit**

   ```bash
   pre-commit install
   ```

5. **Configure suas variáveis de ambiente**

   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

## 🔄 Processo de Desenvolvimento

### 1. Escolha uma Issue

- Verifique as [issues abertas](https://github.com/Ronbragaglia/assistente_com-banco/issues)
- Comente na issue que você gostaria de trabalhar nela
- Aguarde aprovação dos mantenedores

### 2. Crie uma Branch

```bash
git checkout -b feature/sua-feature
# ou
git checkout -b fix/seu-bugfix
```

Use prefixos descritivos:
- `feature/` para novas funcionalidades
- `fix/` para correções de bugs
- `docs/` para alterações na documentação
- `test/` para adicionar ou melhorar testes
- `refactor/` para refatorações
- `chore/` para tarefas de manutenção

### 3. Faça suas Alterações

- Siga as [Diretrizes de Código](#diretrizes-de-código)
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário
- Execute os testes localmente

### 4. Commit suas Alterações

```bash
git add .
git commit -m "feat: adicionar nova funcionalidade X"
```

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` alterações na documentação
- `style:` formatação, ponto e vírgula, etc.
- `refactor:` refatoração de código
- `test:` adicionar ou atualizar testes
- `chore:` alterações em ferramentas de build, configurações, etc.

### 5. Push e Crie um Pull Request

```bash
git push origin feature/sua-feature
```

Crie um Pull Request no GitHub seguindo o [template de PR](#pull-requests).

## 📝 Diretrizes de Código

### Estilo de Código

- Siga o [PEP 8](https://pep8.org/)
- Use [Black](https://github.com/psf/black) para formatação automática
- Limite de linha: 100 caracteres
- Use type hints em todas as funções

### Exemplo de Código

```python
from typing import Optional
from database_assistant import DatabaseManager


def process_event(
    db_manager: DatabaseManager,
    event_name: str,
    event_date: str,
) -> Optional[int]:
    """Processa um evento e o insere no banco de dados.

    Args:
        db_manager: Gerenciador do banco de dados
        event_name: Nome do evento
        event_date: Data do evento

    Returns:
        ID do evento inserido ou None se falhar
    """
    try:
        with db_manager:
            event_id = db_manager.insert_event(
                nome=event_name,
                data=event_date,
                local="Local padrão",
                descricao="Descrição padrão"
            )
        return event_id
    except Exception as e:
        logger.error(f"Erro ao processar evento: {e}")
        return None
```

### Boas Práticas

1. **Documentação**
   - Adicione docstrings em todas as funções e classes
   - Use o formato Google ou NumPy
   - Inclua exemplos de uso quando apropriado

2. **Tratamento de Erros**
   - Capture exceções específicas
   - Logue erros com contexto suficiente
   - Forneça mensagens de erro claras

3. **Performance**
   - Evite operações desnecessárias em loops
   - Use context managers para recursos
   - Considere o uso de cache quando apropriado

4. **Segurança**
   - Nunca faça commit de credenciais
   - Valide inputs de usuários
   - Sanitize dados antes de inserir no banco

## 🧪 Testes

### Executando Testes

```bash
# Executar todos os testes
pytest

# Executar com coverage
pytest --cov=src --cov-report=html

# Executar testes específicos
pytest tests/test_database.py

# Executar com verbose
pytest -v

# Executar testes marcados
pytest -m "not slow"
```

### Escrevendo Testes

- Use [pytest](https://docs.pytest.org/)
- Siga o padrão `test_*.py` para nomes de arquivos
- Use fixtures para configuração compartilhada
- Teste casos normais e casos de borda

### Exemplo de Teste

```python
import pytest
from database_assistant import DatabaseManager


class TestDatabaseManager:
    """Testes para DatabaseManager."""

    @pytest.fixture
    def db_manager(self, tmp_path):
        """Fixture que cria um gerenciador de banco de dados temporário."""
        db_path = tmp_path / "test.db"
        return DatabaseManager(db_path)

    def test_insert_event(self, db_manager):
        """Testa inserção de evento."""
        with db_manager:
            event_id = db_manager.insert_event(
                nome="Test Event",
                data="2024-01-01",
                local="Test Location",
                descricao="Test Description"
            )
        
        assert event_id > 0
```

### Cobertura de Testes

- Mantenha pelo menos 80% de cobertura de código
- Foque em testar lógica complexa e casos de borda
- Use mocks para dependências externas

## 📚 Documentação

### Tipos de Documentação

1. **README.md**
   - Visão geral do projeto
   - Instruções de instalação
   - Exemplos de uso

2. **Docstrings**
   - Documentação de código inline
   - Use formato Google ou NumPy

3. **Docs/**
   - Tutoriais detalhados
   - Guias de API
   - Arquitetura do sistema

4. **CHANGELOG.md**
   - Mantenha atualizado com cada release
   - Siga o formato [Keep a Changelog](https://keepachangelog.com/)

### Atualizando a Documentação

- Atualize o README se a funcionalidade afeta o uso público
- Adicione docstrings para novas funções/classes
- Atualize o CHANGELOG com mudanças significativas

## 🐛 Reportando Bugs

### Antes de Reportar

1. Verifique se o bug já foi reportado
2. Certifique-se de que está usando a versão mais recente
3. Tente reproduzir o bug em um ambiente limpo

### Como Reportar

Use o [template de bug](.github/ISSUE_TEMPLATE/bug_report.md):

```markdown
**Descrição do Bug**
Uma descrição clara e concisa do que o bug é.

**Passos para Reproduzir**
1. Vá para '...'
2. Clique em '....'
3. Role até '....'
4. Veja o erro

**Comportamento Esperado**
Uma descrição clara do que você esperava acontecer.

**Screenshots**
Se aplicável, adicione screenshots para ajudar a explicar o problema.

**Ambiente**
- OS: [e.g. Windows 10]
- Python Version: [e.g. 3.9]
- Versão do Projeto: [e.g. 2.0.0]

**Logs Adicionais**
Adicione quaisquer logs ou saídas relevantes.
```

## 💡 Sugerindo Melhorias

### Antes de Sugerir

1. Verifique se a sugestão já foi feita
2. Pense em como a funcionalidade beneficiaria outros usuários
3. Considere se você pode implementá-la

### Como Sugerir

Use o [template de feature request](.github/ISSUE_TEMPLATE/feature_request.md):

```markdown
**Descrição da Funcionalidade**
Uma descrição clara e concisa da funcionalidade.

**Problema que Resolve**
Qual problema essa funcionalidade resolve? Que valor ela adiciona?

**Solução Proposta**
Como você imagina que essa funcionalidade deva ser implementada?

**Alternativas Consideradas**
Quais alternativas você considerou? Por que não foram escolhidas?

**Contexto Adicional**
Adicione qualquer outro contexto ou capturas de tela sobre a funcionalidade.
```

## 🔀 Pull Requests

### Checklist Antes de Submeter

- [ ] Meu código segue as diretrizes de estilo do projeto
- [ ] Eu realizei uma auto-revisão do meu código
- [ ] Eu comentei meu código, particularmente em áreas difíceis de entender
- [ ] Eu fiz as alterações correspondentes na documentação
- [ ] Meus cambios geram nenhum novo aviso
- [ ] Eu adicionei testes que provam que minha correção é efetiva ou que minha funcionalidade funciona
- [ ] Testes novos e unitários passaram localmente com meus cambios
- [ ] Quaisquer testes dependentes passaram

### Processo de Revisão

1. **Revisão Automática**
   - CI/CD checks (lint, testes, coverage)
   - Pre-commit hooks

2. **Revisão Manual**
   - Pelo menos um mantenedor deve aprovar
   - Feedback será fornecido se necessário
   - Faça as alterações solicitadas

3. **Merge**
   - Após aprovação, o PR será mergeado
   - Mantenedores podem fazer squash/merge
   - A branch será deletada após o merge

### Template de PR

```markdown
## Descrição
Breve descrição das mudanças feitas.

## Tipo de Mudança
- [ ] Bug fix (correção não quebrando mudança)
- [ ] Nova feature (funcionalidade que adiciona comportamento)
- [ ] Breaking change (correção ou funcionalidade que causa comportamento existente a não funcionar)
- [ ] Documentação (atualização de docs)

## Como Foi Testado
Descreva os testes que você executou para verificar suas mudanças.

## Checklist
- [ ] Meu código segue as diretrizes de estilo deste projeto
- [ ] Eu realizei uma auto-revisão do meu código
- [ ] Eu comentei meu código
- [ ] Eu fiz as alterações correspondentes na documentação
- [ ] Meus cambios geram nenhum novo aviso
- [ ] Eu adicionei testes que provam que minha correção é efetiva
- [ ] Testes novos e unitários passaram localmente
- [ ] Quaisquer testes dependentes passaram

## Issues Relacionadas
Closes #123, #456
```

## 📞 Contato

Se você tiver dúvidas sobre como contribuir, sinta-se à vontade para:

- Abrir uma issue com a tag "question"
- Entrar em contato: [ronald.bragaglia@example.com](mailto:ronald.bragaglia@example.com)
- Participar das discussões no GitHub

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a Licença MIT.

---

Obrigado por contribuir! 🎉
