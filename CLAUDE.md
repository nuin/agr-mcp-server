# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Alliance of Genome Resources (AGR) MCP Server - A comprehensive Model Context Protocol server providing programmatic access to genomic data, bioinformatics tools, and comparative genomics research capabilities across 8 model organisms.

## Build/Test/Lint Commands

### Development Setup
```bash
# Create virtual environment and install dependencies
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # for development
```

### Server Operations
```bash
# Start enhanced server (30+ genomics tools)
python src/agr_server_enhanced.py

# Start basic server (10 essential tools)
python src/agr_server_basic.py
```

### Testing & Quality
```bash
# Run tests
python -m pytest tests/ -v
pytest tests/test_agr_server.py -v  # specific test file

# Code quality checks
black src/ tests/          # format code
flake8 src/ tests/         # linting
mypy src/                  # type checking
bandit -r src/             # security scan

# Coverage analysis
pytest --cov=src tests/
```

### Development Tools
```bash
# Command-line interface usage
python scripts/agr_cli.py search BRCA1
python scripts/agr_cli.py gene-info HGNC:1100

# Health check
python scripts/health_check.py

# Quick demo
python scripts/quick_start_demo.py
```

## Architecture Overview

### Core Structure
- **EnhancedAGRClient**: Main client class handling all API interactions with Alliance ecosystem
- **MCP Server Implementation**: Standard MCP pattern with `@server.list_tools()` and `@server.call_tool()` decorators
- **Async Architecture**: Uses `httpx` with async/await for non-blocking HTTP requests
- **Tool Categories**: 30+ tools organized into gene search, allele/variant analysis, disease associations, expression data, orthology, pathways, literature search, and sequence analysis

### External Service Integration
- **Primary API**: `https://www.alliancegenome.org/api` (core genomic data)
- **BLAST**: `https://blast.alliancegenome.org` (sequence similarity)
- **JBrowse**: `https://jbrowse.alliancegenome.org` (genome browser)
- **Textpresso**: Literature mining integration
- **AllianceMine**: Complex data mining queries
- **FMS API**: `https://fms.alliancegenome.org/api` (file management)

### Model Organisms Supported (8 species)
- **Homo sapiens** (HGNC), **Mus musculus** (MGI), **Rattus norvegicus** (RGD)
- **Danio rerio** (ZFIN), **Drosophila melanogaster** (FlyBase)
- **Caenorhabditis elegans** (WormBase), **Saccharomyces cerevisiae** (SGD)
- **Xenopus** (Xenbase)

## Key Implementation Patterns

### Error Handling
- Centralized error handling in `_make_request()` method
- HTTP status code validation with detailed logging
- JSON parsing protection with graceful fallbacks
- Consistent error messaging through `CallToolResult`

### Configuration Management
- `AGRConfig` dataclass in `utils.py` for environment-based configuration
- YAML configuration support for different environments (dev/staging/production)
- Environment variables: `AGR_BASE_URL`, `AGR_TIMEOUT`, `LOG_LEVEL`, etc.

### Tool Implementation Pattern
```python
async def tool_name(self, param: str) -> Dict[str, Any]:
    """Tool description with parameter details."""
    endpoint = f"/endpoint/{param}"
    return await self._make_request(endpoint)
```

### Adding New Tools
1. Add method to `EnhancedAGRClient` class following async pattern
2. Register tool in `@server.list_tools()` with proper schema
3. Add tool call handler in `@server.call_tool()` with parameter validation
4. Follow naming convention: use underscores for method names, hyphens for tool names

## Development Guidelines

### Code Style
- Use `black` for formatting, `flake8` for linting, `mypy` for type checking
- Async/await pattern for all HTTP operations
- Type hints required for all functions
- Descriptive docstrings for all tools and methods

### Testing Approach
- pytest with `pytest-asyncio` for async test support
- Use `aioresponses` for mocking HTTP calls
- Test files should mirror source structure: `tests/test_agr_server.py`
- Include both unit tests and integration tests

### Genomics Domain Knowledge
- Gene identifiers follow standard formats (HGNC:1100, MGI:96677, etc.)
- Cross-species orthology is key functionality - genes in one species map to homologs in others
- Expression data includes tissue-specific and developmental stage information
- Disease associations include both direct gene-disease links and model organism data

### Common Genomics Use Cases
- Gene search and information retrieval across species
- Disease association analysis for clinical relevance
- Expression analysis for tissue/development studies
- Orthology mapping for comparative genomics
- Literature search for gene-specific research
- Sequence analysis with BLAST integration