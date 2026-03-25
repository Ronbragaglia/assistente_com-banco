# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete test suite for all modules
- Docker support with Dockerfile and docker-compose.yml
- CI/CD pipeline with GitHub Actions
- Pre-commit hooks configuration
- Makefile for common development tasks
- Advanced examples and use cases
- Export/import functionality for Q&A pairs
- Streaming response support
- Multiple embedding models support
- API documentation
- Performance optimizations
- Enhanced error handling and validation

### Changed
- Improved type hints throughout the codebase
- Better logging and debugging capabilities
- Enhanced configuration management
- Improved similarity search performance

### Fixed
- Fixed database connection issues
- Fixed similarity search edge cases
- Fixed CLI argument parsing

## [2.0.0] - 2024-01-15

### Added
- Initial release of OpenAI Database Assistant
- SQLite database integration
- TF-IDF based similarity search
- OpenAI GPT integration
- Interactive CLI mode
- Caching system for Q&A pairs
- Comprehensive logging system
- Configuration management with Pydantic
- Basic test suite
- Documentation and examples

### Features
- 🗄️ SQLite database for persistent storage
- 🔍 TF-IDF with cosine similarity for finding similar questions
- 🤖 OpenAI GPT-3.5/GPT-4 integration
- 💬 Interactive mode for real-time conversations
- 💾 Automatic caching of questions and answers
- 🎯 Efficient similarity search
- 📝 Advanced logging with colored output
- 🔧 Flexible configuration via environment variables
- 🧪 Complete test suite

## [1.0.0] - 2023-12-01

### Added
- Initial proof of concept
- Basic OpenAI integration
- Simple database storage
- Basic similarity search

---

[Unreleased]: https://github.com/Ronbragaglia/assistente_com-banco/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/Ronbragaglia/assistente_com-banco/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/Ronbragaglia/assistente_com-banco/releases/tag/v1.0.0
