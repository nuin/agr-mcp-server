# Alliance of Genome Resources MCP Server

🧬 **Organized Alliance of Genome Resources MCP Server Implementation**

A comprehensive Model Context Protocol (MCP) server providing programmatic access to the Alliance of Genome Resources genomic data, bioinformatics tools, and comparative genomics research capabilities.

## 📁 Project Structure

```
agr-mcp-server/
├── 🚀 src/                     # Core source code
│   ├── agr_server_enhanced.py  # Enhanced MCP server (30+ tools)
│   ├── agr_server_basic.py     # Basic MCP server (10 tools)
│   └── utils.py               # Utilities and configuration
│
├── 📚 examples/               # Usage examples and tutorials
│   ├── basic_examples.py      # Basic usage patterns
│   └── advanced_examples.py   # Advanced genomics workflows
│
├── 🧪 tests/                  # Test suite
│   └── test_agr_server.py     # Comprehensive tests
│
├── ⚙️ config/                # Configuration files
│   ├── development.yaml       # Development environment
│   ├── staging.yaml          # Staging environment
│   ├── production.yaml       # Production environment
│   └── mcp_client_config.json # MCP client configuration
│
├── 🛠️ scripts/               # Utility scripts
│   ├── agr_cli.py            # Command line interface
│   ├── health_check.py       # System health checker
│   ├── quick_start_demo.py   # Interactive demonstration
│   └── deploy.sh             # Deployment automation
│
├── 🐳 docker/               # Docker and deployment files
│   ├── Dockerfile            # Container configuration
│   └── docker-compose.yml    # Multi-service deployment
│
├── 📄 Documentation & Setup
│   ├── README.md             # Comprehensive documentation
│   ├── PROJECT_OVERVIEW.md   # Project summary
│   ├── requirements.txt      # Production dependencies
│   ├── requirements-dev.txt  # Development dependencies
│   ├── setup.py             # Package configuration
│   ├── Makefile             # Development automation
│   ├── .env.example         # Environment template
│   ├── .gitignore           # Git ignore patterns
│   └── LICENSE              # MIT License
│
└── 🔧 .github/              # CI/CD and automation
    └── workflows/
        └── ci.yml           # GitHub Actions pipeline
```

## 🚀 Quick Start

### Navigate to the Project
```bash
cd /Users/nuin/Projects/alliance/agr-mcp-server
```

### Basic Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run interactive demo
python scripts/quick_start_demo.py
```

### Try the Enhanced Server
```bash
# Start enhanced server (30+ tools)
python src/agr_server_enhanced.py

# Or use the CLI
python scripts/agr_cli.py search BRCA1
python scripts/agr_cli.py gene-info HGNC:1100
```

### Health Check
```bash
python scripts/health_check.py
```

### Development with Makefile
```bash
# Show all available commands
make help

# Complete development setup
make dev-setup

# Run tests
make test

# Run examples
make examples

# Deploy to development
make deploy-dev
```

## ⭐ Key Features

### 🔬 Core Genomics Functionality (30+ Tools)
- **Gene Search & Discovery** across 8+ model organisms
- **Cross-Species Orthology** and comparative analysis  
- **Disease Associations** and clinical relevance data
- **Expression Analysis** with visualization-ready data
- **Molecular & Genetic Interactions**
- **Allele & Variant Information**
- **Functional Annotations** (GO terms, pathways)
- **Literature Search** with Textpresso integration
- **BLAST Sequence Analysis**
- **JBrowse Genome Browser** integration

### 🌍 Model Organisms Supported
- **Homo sapiens** (Human) - HGNC identifiers
- **Mus musculus** (Mouse) - MGI identifiers  
- **Rattus norvegicus** (Rat) - RGD identifiers
- **Danio rerio** (Zebrafish) - ZFIN identifiers
- **Drosophila melanogaster** (Fruit fly) - FlyBase identifiers
- **Caenorhabditis elegans** (Roundworm) - WormBase identifiers
- **Saccharomyces cerevisiae** (Baker's yeast) - SGD identifiers
- **Xenopus** (Frog species) - Xenbase identifiers

### 🔧 Advanced Capabilities
- **AllianceMine** data mining and complex queries
- **Expression Ribbons** for visualization
- **Transgenic Models** and construct data
- **Experimental Conditions** and treatments
- **Pathway Analysis** and biological networks
- **Literature Mining** and citation management

## 💻 Usage Examples

### Command Line Interface
```bash
# Search for genes
python scripts/agr_cli.py search BRCA1 --limit 10

# Get comprehensive gene information  
python scripts/agr_cli.py gene-info HGNC:1100

# Find orthologs across species
python scripts/agr_cli.py orthologs HGNC:1100

# Get disease associations
python scripts/agr_cli.py diseases HGNC:1100

# Search literature
python scripts/agr_cli.py literature "BRCA1 mutations"

# BLAST sequence search
python scripts/agr_cli.py blast ATCGATCGATCG --program blastn
```

### Python API Usage
```python
from src.agr_server_enhanced import EnhancedAGRClient

client = EnhancedAGRClient()

# Search for genes
results = await client.search_genes("BRCA1")

# Get gene information
gene_info = await client.get_gene_info("HGNC:1100")

# Find orthologs
orthologs = await client.find_orthologs("HGNC:1100")
```

## 🧪 Testing & Quality

```bash
# Run comprehensive tests
python -m pytest tests/test_agr_server.py -v

# Check code quality
make lint

# Run security scan
make security

# Performance test
make test-cov
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker
cd docker/
docker build -t agr-mcp-server .
docker run -p 8000:8000 agr-mcp-server

# Or use docker-compose
docker-compose up -d
```

## 📊 Monitoring & Health

```bash
# System health check
python scripts/health_check.py

# Monitor logs (if running with Docker)
docker logs agr-mcp-server

# Check system status
make health-check
```

## ⚙️ Configuration

### Environment Variables
```bash
# Copy and edit environment template
cp .env.example .env

# Key settings
AGR_BASE_URL=https://www.alliancegenome.org/api
AGR_TIMEOUT=30
LOG_LEVEL=INFO
```

### Environment-Specific Configs
- **Development**: `config/development.yaml`
- **Staging**: `config/staging.yaml`
- **Production**: `config/production.yaml`

## 🌐 Alliance Integration

This MCP server integrates with the full Alliance ecosystem:
- **Primary Portal**: https://www.alliancegenome.org/
- **API Documentation**: https://www.alliancegenome.org/swagger-ui/
- **JBrowse Genome Browser**: https://jbrowse.alliancegenome.org/
- **AllianceMine Data Mining**: https://www.alliancegenome.org/alliancemine/
- **BLAST Sequence Search**: https://blast.alliancegenome.org/

## 🎯 Use Cases

### Research Applications
- **Comparative Genomics**: Cross-species gene function analysis
- **Disease Research**: Gene-disease association studies  
- **Drug Discovery**: Target identification and validation
- **Systems Biology**: Pathway and network analysis

### AI/ML Integration
- **Training Data**: Large-scale genomics datasets
- **Feature Engineering**: Gene annotations and functional data
- **Knowledge Graphs**: Structured biological knowledge
- **Predictive Modeling**: Gene function and disease prediction

## 📞 Support & Resources

- **Project Location**: `/Users/nuin/Projects/alliance/agr-mcp-server/`
- **Documentation**: See `README.md` for comprehensive guides
- **Examples**: Check `examples/` directory for usage patterns
- **CLI Help**: Run `python scripts/agr_cli.py --help`
- **Health Check**: Run `python scripts/health_check.py`
- **AGR Support**: Contact help@alliancegenome.org

## 🏗️ Development

### Getting Started
```bash
# Clone/navigate to project
cd /Users/nuin/Projects/alliance/agr-mcp-server

# Setup development environment
make dev-setup

# Run examples
make examples

# Start development server
make server-enhanced
```

### Development Commands
```bash
make help            # Show all available commands
make test            # Run tests
make lint            # Code quality checks
make format          # Format code
make docs            # Build documentation
make clean           # Clean build artifacts
```

## 📈 Production Features

- **High Performance**: Async/await architecture, connection pooling
- **Reliability**: Comprehensive error handling, health monitoring
- **Security**: Input validation, rate limiting, security scanning
- **Scalability**: Multi-instance deployment, load balancing
- **Monitoring**: Health checks, logging, metrics

## 🎉 Status: Ready for Use!

✅ **FULLY IMPLEMENTED & ORGANIZED**
- Complete MCP server with 30+ genomics tools
- Organized project structure for maintainability
- Production-ready deployment options
- Comprehensive testing and quality assurance
- Full documentation and examples
- Multi-environment configuration
- CI/CD pipeline and automation

**Ready for immediate use in genomics research, AI/ML applications, and clinical bioinformatics workflows! 🧬**
