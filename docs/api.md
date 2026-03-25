# API Documentation

Complete API reference for the OpenAI Database Assistant.

## Table of Contents

- [Settings](#settings)
- [DatabaseManager](#databasemanager)
- [SimilaritySearch](#similaritysearch)
- [OpenAIAssistant](#openaiassistant)
- [Logger Functions](#logger-functions)
- [CLI Functions](#cli-functions)

---

## Settings

Configuration management using Pydantic Settings.

### Class: `Settings`

```python
from database_assistant import Settings

settings = Settings()
```

#### Attributes

| Attribute | Type | Default | Description |
|-----------|--------|----------|-------------|
| `openai_api_key` | `str` | Required | OpenAI API key |
| `openai_model` | `str` | `"gpt-3.5-turbo"` | OpenAI model to use |
| `openai_temperature` | `float` | `0.7` | Temperature for responses (0.0-2.0) |
| `database_path` | `Path` | `Path("data/eventos.db")` | Path to SQLite database |
| `similarity_threshold` | `float` | `0.7` | Similarity threshold (0.0-1.0) |
| `assistant_name` | `str` | `"Assistente de Eventos"` | Name of the assistant |
| `assistant_system_prompt` | `str` | `"Você é um assistente útil..."` | System prompt |
| `log_level` | `str` | `"INFO"` | Logging level |
| `log_file` | `str` | `"logs/assistant.log"` | Path to log file |
| `cache_enabled` | `bool` | `True` | Enable caching |

#### Methods

##### `ensure_directories()`

Creates all required directories.

```python
settings.ensure_directories()
```

---

## DatabaseManager

Manages SQLite database operations.

### Class: `DatabaseManager`

```python
from database_assistant import DatabaseManager
from pathlib import Path

db_manager = DatabaseManager(Path("data/eventos.db"))
```

#### Constructor

```python
DatabaseManager(db_path: Path)
```

**Parameters:**
- `db_path` (`Path`): Path to the SQLite database file

#### Context Manager

```python
with db_manager:
    # Database operations here
    pass
```

#### Methods

##### `connect()`

Establishes connection to the database.

```python
db_manager.connect()
```

##### `disconnect()`

Closes the database connection.

```python
db_manager.disconnect()
```

##### `create_tables()`

Creates all necessary tables in the database.

```python
with db_manager:
    db_manager.create_tables()
```

##### `insert_event()`

Inserts a new event into the database.

```python
event_id = db_manager.insert_event(
    nome="Event Name",
    data="2024-01-01",
    local="Event Location",
    descricao="Event Description"
)
```

**Parameters:**
- `nome` (`str`): Event name
- `data` (`str`): Event date (YYYY-MM-DD format)
- `local` (`str`): Event location
- `descricao` (`str`): Event description

**Returns:**
- `int`: ID of the inserted event

##### `get_all_events()`

Retrieves all events from the database.

```python
events = db_manager.get_all_events()
```

**Returns:**
- `List[Tuple[str, str, str, str]]`: List of (nome, data, local, descricao) tuples

##### `get_events_as_context()`

Gets all events formatted as context string.

```python
context = db_manager.get_events_as_context()
```

**Returns:**
- `str`: Formatted context string with all events

##### `insert_question_answer()`

Inserts a new question and answer pair.

```python
qa_id = db_manager.insert_question_answer(
    pergunta="Question text",
    resposta="Answer text"
)
```

**Parameters:**
- `pergunta` (`str`): The question
- `resposta` (`str`): The answer

**Returns:**
- `int`: ID of the inserted record

##### `get_all_qa_pairs()`

Retrieves all question and answer pairs.

```python
qa_pairs = db_manager.get_all_qa_pairs()
```

**Returns:**
- `List[Tuple[str, str]]`: List of (pergunta, resposta) tuples

##### `get_qa_count()`

Gets the count of question and answer pairs.

```python
count = db_manager.get_qa_count()
```

**Returns:**
- `int`: Number of Q&A pairs in the database

##### `seed_sample_data()`

Seeds the database with sample events if empty.

```python
with db_manager:
    db_manager.seed_sample_data()
```

---

## SimilaritySearch

Search for similar questions using TF-IDF and cosine similarity.

### Class: `SimilaritySearch`

```python
from database_assistant import SimilaritySearch

similarity_search = SimilaritySearch(threshold=0.7)
```

#### Constructor

```python
SimilaritySearch(threshold: float = 0.7)
```

**Parameters:**
- `threshold` (`float`): Similarity threshold for considering a match (0.0 to 1.0)

#### Methods

##### `fit()`

Fits the vectorizer with existing Q&A pairs.

```python
qa_pairs = [
    ("Question 1", "Answer 1"),
    ("Question 2", "Answer 2"),
]

similarity_search.fit(qa_pairs)
```

**Parameters:**
- `qa_pairs` (`List[Tuple[str, str]]`): List of (question, answer) tuples

##### `search()`

Search for the most similar question and return its answer.

```python
answer = similarity_search.search("What events are available?")
```

**Parameters:**
- `query` (`str`): The query question to search for

**Returns:**
- `Optional[str]`: The answer to the most similar question, or None if no match found

##### `search_with_score()`

Search for the most similar question and return answer with similarity score.

```python
answer, score = similarity_search.search_with_score("What events?")
```

**Parameters:**
- `query` (`str`): The query question to search for

**Returns:**
- `Tuple[Optional[str], float]`: Tuple of (answer, similarity_score). Returns (None, 0.0) if no match found.

##### `update()`

Updates the similarity search with new Q&A pairs.

```python
new_pairs = [
    ("New Question", "New Answer"),
]

similarity_search.update(new_pairs)
```

**Parameters:**
- `qa_pairs` (`List[Tuple[str, str]]`): List of (question, answer) tuples to add

##### `clear()`

Clears all indexed questions and answers.

```python
similarity_search.clear()
```

---

## OpenAIAssistant

Manager for OpenAI API interactions.

### Class: `OpenAIAssistant`

```python
from database_assistant import OpenAIAssistant, Settings

settings = Settings()
assistant = OpenAIAssistant(settings)
```

#### Constructor

```python
OpenAIAssistant(settings: Optional[Settings] = None)
```

**Parameters:**
- `settings` (`Optional[Settings]`): Configuration settings (uses default if not provided)

#### Methods

##### `generate_response()`

Generates a response for a question based on context.

```python
response = assistant.generate_response(
    context="Context information",
    question="What events are available?",
    system_prompt="You are a helpful assistant"
)
```

**Parameters:**
- `context` (`str`): The context or background information
- `question` (`str`): The question to answer
- `system_prompt` (`Optional[str]`): Optional system prompt (uses settings default if not provided)

**Returns:**
- `str`: The generated response

**Raises:**
- `Exception`: If the API call fails

##### `generate_response_with_history()`

Generates a response with conversation history.

```python
conversation_history = [
    {"role": "user", "content": "Previous question"},
    {"role": "assistant", "content": "Previous answer"},
]

response = assistant.generate_response_with_history(
    context="Context information",
    conversation_history=conversation_history
)
```

**Parameters:**
- `context` (`str`): The context or background information
- `conversation_history` (`list`): List of message dictionaries with 'role' and 'content'
- `system_prompt` (`Optional[str]`): Optional system prompt (uses settings default if not provided)

**Returns:**
- `str`: The generated response

**Raises:**
- `Exception`: If the API call fails

##### `set_model()`

Changes the OpenAI model.

```python
assistant.set_model("gpt-4")
```

**Parameters:**
- `model` (`str`): The model name (e.g., "gpt-3.5-turbo", "gpt-4")

##### `set_temperature()`

Changes the temperature for responses.

```python
assistant.set_temperature(0.5)
```

**Parameters:**
- `temperature` (`float`): Temperature value (0.0 to 2.0)

**Raises:**
- `ValueError`: If temperature is not between 0.0 and 2.0

---

## Logger Functions

Setup and configure logging.

### `setup_logger()`

Sets up and configures a logger with console and file handlers.

```python
from database_assistant import setup_logger

logger = setup_logger(
    name="my_app",
    level="INFO",
    log_file="logs/my_app.log",
    use_colors=True
)
```

**Parameters:**
- `name` (`str`): Logger name (default: "database_assistant")
- `level` (`str`): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `log_file` (`Optional[str]`): Optional path to log file
- `use_colors` (`bool`): Whether to use colored output in console

**Returns:**
- `logging.Logger`: Configured logger instance

### `get_logger()`

Gets an existing logger or creates a new one.

```python
from database_assistant import get_logger

logger = get_logger("my_app")
```

**Parameters:**
- `name` (`str`): Logger name

**Returns:**
- `logging.Logger`: Logger instance

---

## CLI Functions

Command-line interface functions.

### `main()`

Main entry point for the CLI.

```python
from database_assistant.cli import main

import sys
sys.exit(main())
```

**Return:**
- `int`: Exit code (0 for success, 1 for error)

**Command-line Arguments:**

| Argument | Type | Description |
|----------|--------|-------------|
| `--interactive` | flag | Run in interactive mode |
| `--ask QUESTION` | string | Ask a single question and exit |
| `--add-event NOME DATA LOCAL DESCRICAO` | strings | Add a new event to the database |
| `--list-events` | flag | List all events in the database |
| `--api-key` | string | OpenAI API key |
| `--model` | string | OpenAI model to use |
| `--database` | Path | Path to SQLite database file |
| `--config` | Path | Path to .env configuration file |
| `--log-level` | string | Logging level |
| `--log-file` | string | Path to log file |
| `--no-color` | flag | Disable colored output |
| `--no-cache` | flag | Disable caching of responses |
| `--version` | flag | Show version and exit |

### `run_interactive_mode()`

Runs the assistant in interactive mode.

```python
from database_assistant.cli import run_interactive_mode

run_interactive_mode(
    db_manager=db_manager,
    similarity_search=similarity_search,
    ai_assistant=ai_assistant,
    settings=settings
)
```

### `run_single_question()`

Asks a single question and exits.

```python
from database_assistant.cli import run_single_question

run_single_question(
    db_manager=db_manager,
    similarity_search=similarity_search,
    ai_assistant=ai_assistant,
    question="What events are available?",
    settings=settings
)
```

### `add_event()`

Adds a new event to the database.

```python
from database_assistant.cli import add_event

add_event(
    db_manager=db_manager,
    event_data=("Event Name", "2024-01-01", "Location", "Description")
)
```

### `list_events()`

Lists all events in the database.

```python
from database_assistant.cli import list_events

list_events(db_manager=db_manager)
```

---

## Examples

### Basic Usage

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

### Advanced Usage with Custom Settings

```python
from database_assistant import Settings, OpenAIAssistant

# Custom settings
settings = Settings(
    openai_api_key="your-api-key",
    openai_model="gpt-4",
    openai_temperature=0.5,
    similarity_threshold=0.8,
    cache_enabled=True
)

# Initialize assistant with custom settings
assistant = OpenAIAssistant(settings)

# Change model dynamically
assistant.set_model("gpt-3.5-turbo")

# Change temperature dynamically
assistant.set_temperature(0.8)
```

---

## Error Handling

### Database Errors

```python
import sqlite3

try:
    with db_manager:
        db_manager.insert_event("Event", "2024-01-01", "Location", "Description")
except sqlite3.Error as e:
    print(f"Database error: {e}")
```

### API Errors

```python
try:
    response = assistant.generate_response(context, question)
except Exception as e:
    print(f"API error: {e}")
```

### Similarity Search Errors

```python
try:
    answer = similarity_search.search(question)
except Exception as e:
    print(f"Similarity search error: {e}")
```

---

## Best Practices

1. **Always use context managers** for database operations
2. **Handle exceptions** appropriately for API calls
3. **Cache responses** to improve performance
4. **Use appropriate similarity thresholds** for your use case
5. **Log operations** for debugging and monitoring
6. **Validate inputs** before processing
7. **Use streaming** for long responses
8. **Optimize batch operations** for better performance

---

## Performance Tips

1. **Use similarity search** to avoid unnecessary API calls
2. **Batch operations** when possible
3. **Cache frequently accessed data**
4. **Use appropriate logging levels** in production
5. **Optimize database queries** with indexes
6. **Use streaming** for better user experience

---

## Security Considerations

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Validate all inputs** before processing
4. **Sanitize database inputs** to prevent SQL injection
5. **Use HTTPS** for API calls
6. **Implement rate limiting** for API usage
7. **Regularly update dependencies** for security patches

---

## Support

For more information, visit:
- [GitHub Repository](https://github.com/Ronbragaglia/assistente_com-banco)
- [Documentation](https://github.com/Ronbragaglia/assistente_com-banco#readme)
- [Issues](https://github.com/Ronbragaglia/assistente_com-banco/issues)
