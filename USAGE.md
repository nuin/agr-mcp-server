# AGR MCP Server Usage Guide

## Overview

The Alliance of Genome Resources (AGR) MCP Server provides Claude Code with access to comprehensive genomics data through 30+ specialized tools. This integration transforms Claude into a powerful genomics research assistant with real-time access to the world's largest comparative genomics database.

## Quick Start

### Prerequisites
- Claude Code installed and configured
- AGR MCP Server added to Claude configuration (see installation guide)
- Active internet connection for API access

### Getting Started
1. **Restart Claude Code** to load the MCP server
2. **Ask genomics questions** in natural language
3. **Explore the examples** below to understand capabilities

## Core Capabilities

### 🧬 Gene Research
- **Gene Search**: Find genes by symbol, name, or identifier across 8 model organisms
- **Gene Information**: Retrieve detailed annotations, locations, and functional data
- **Cross-Species Analysis**: Compare genes across human, mouse, fly, worm, and more

### 🏥 Disease & Phenotype Analysis
- **Disease Associations**: Link genes to human diseases and conditions
- **Phenotype Data**: Access experimental phenotype information
- **Clinical Relevance**: Connect research findings to medical applications

### 📊 Expression & Interaction Analysis
- **Expression Patterns**: Tissue-specific and developmental expression data
- **Molecular Interactions**: Protein-protein interaction networks
- **Genetic Interactions**: Epistasis and genetic modifier relationships

### 🔬 Sequence & Structural Analysis
- **BLAST Search**: Sequence similarity analysis across Alliance species
- **Genome Browser**: Integration with JBrowse for genomic visualization
- **Sequence Retrieval**: Access genomic, transcript, and protein sequences

## Supported Model Organisms

| Organism | Common Name | Database | Example ID |
|----------|-------------|----------|------------|
| *Homo sapiens* | Human | HGNC | HGNC:1100 |
| *Mus musculus* | Mouse | MGI | MGI:104537 |
| *Rattus norvegicus* | Rat | RGD | RGD:2018 |
| *Danio rerio* | Zebrafish | ZFIN | ZFIN:ZDB-GENE-990415-8 |
| *Drosophila melanogaster* | Fruit fly | FlyBase | FB:FBgn0000043 |
| *Caenorhabditis elegans* | Roundworm | WormBase | WB:WBGene00000912 |
| *Saccharomyces cerevisiae* | Baker's yeast | SGD | SGD:S000001855 |
| *Xenopus* | Frogs | Xenbase | XENBASE:XB-GENE-865049 |

## Usage Examples

### Basic Gene Research

#### Example 1: Gene Information Lookup
```
User: "Tell me about the BRCA1 gene"

Claude Response:
- Searches for BRCA1 across species
- Retrieves detailed gene information
- Shows gene symbol, name, location, and function
- Provides cross-references and external links
```

#### Example 2: Cross-Species Gene Comparison
```
User: "Find mouse and zebrafish orthologs of human BRCA1"

Claude Response:
- Identifies human BRCA1 (HGNC:1100)
- Finds orthologous genes in mouse and zebrafish
- Compares gene structures and functions
- Shows evolutionary conservation
```

### Disease Research

#### Example 3: Disease Association Analysis
```
User: "What diseases are associated with the TP53 gene?"

Claude Response:
- Retrieves TP53 gene information
- Lists associated diseases and conditions
- Shows evidence codes and experimental support
- Provides literature references
```

#### Example 4: Phenotype Investigation
```
User: "Get phenotype data for Alzheimer's disease genes"

Claude Response:
- Searches for Alzheimer's-related genes (APOE, APP, PSEN1)
- Retrieves experimental phenotype data
- Shows model organism studies
- Connects to human disease relevance
```

### Expression Analysis

#### Example 5: Tissue Expression Patterns
```
User: "Show expression patterns for the FOXP2 gene"

Claude Response:
- Retrieves expression data across tissues
- Shows developmental stage information
- Provides visualization-ready data
- Links to expression atlases
```

#### Example 6: Comparative Expression
```
User: "Compare brain expression of autism-related genes"

Claude Response:
- Identifies autism-associated genes
- Retrieves brain-specific expression data
- Compares expression levels across genes
- Shows co-expression patterns
```

### Molecular Interactions

#### Example 7: Protein Interaction Networks
```
User: "Find protein interactions for the insulin receptor"

Claude Response:
- Searches for INSR gene
- Retrieves protein-protein interactions
- Shows interaction confidence scores
- Maps interaction networks
```

#### Example 8: Genetic Interactions
```
User: "What genes interact genetically with TP53?"

Claude Response:
- Finds genetic interaction data
- Shows epistasis relationships
- Provides experimental evidence
- Links to functional pathways
```

### Pathway Analysis

#### Example 9: Biological Pathways
```
User: "What pathways involve EGFR signaling?"

Claude Response:
- Retrieves EGFR pathway information
- Shows associated biological processes
- Links to pathway databases
- Identifies pathway components
```

#### Example 10: Functional Annotation
```
User: "Get GO terms for cell cycle genes"

Claude Response:
- Searches for cell cycle-related genes
- Retrieves Gene Ontology annotations
- Shows biological processes and functions
- Provides evidence codes
```

### Literature Research

#### Example 11: Literature Mining
```
User: "Search literature for CRISPR applications in muscular dystrophy"

Claude Response:
- Performs full-text literature search
- Finds relevant publications
- Shows abstracts and key findings
- Links to PubMed articles
```

#### Example 12: Gene-Specific Literature
```
User: "Find recent papers about CFTR gene mutations"

Claude Response:
- Retrieves CFTR-specific literature
- Shows publication dates and journals
- Highlights key research findings
- Provides citation information
```

### Sequence Analysis

#### Example 13: BLAST Sequence Search
```
User: "Run BLAST on this sequence: ATGCGATCGATCGTAGC"

Claude Response:
- Performs BLAST similarity search
- Shows matching sequences across species
- Provides alignment scores and E-values
- Identifies potential gene matches
```

#### Example 14: Sequence Retrieval
```
User: "Get the protein sequence for human insulin"

Claude Response:
- Identifies insulin gene (INS)
- Retrieves protein sequence
- Shows sequence features and domains
- Provides FASTA format output
```

### Advanced Analysis

#### Example 15: Multi-Gene Analysis
```
User: "Analyze the p53 pathway genes for cancer relevance"

Claude Response:
- Identifies p53 pathway components
- Retrieves cancer association data
- Shows interaction networks
- Provides functional summaries
```

#### Example 16: Comparative Genomics
```
User: "Compare HOX gene clusters between human and fly"

Claude Response:
- Identifies HOX genes in both species
- Maps orthologous relationships
- Compares gene organization
- Shows evolutionary insights
```

## Available Tools Reference

### Gene Search & Information
- `search-genes`: Search for genes by symbol, name, or identifier
- `get-gene-info`: Retrieve comprehensive gene information
- `get-gene-summary`: Get concise gene summaries

### Allele & Variant Analysis
- `get-gene-alleles`: Find alleles with phenotypic effects
- `get-allele-info`: Detailed allele information
- `get-gene-variants`: Sequence variants for genes

### Disease & Phenotype
- `get-gene-diseases`: Disease associations and models
- `get-disease-info`: Comprehensive disease information
- `get-gene-phenotypes`: Phenotype annotations
- `search-diseases`: Search disease databases

### Expression & Interactions
- `get-gene-expression`: Comprehensive expression data
- `get-expression-ribbon-summary`: Visualization-ready expression
- `get-molecular-interactions`: Protein-protein interactions
- `get-genetic-interactions`: Epistasis data

### Orthology & Comparative Genomics
- `find-orthologs`: Cross-species orthologous genes
- `get-homologs-by-species`: Species-specific homologs
- `get-paralogs`: Within-species paralogs

### Function & Pathways
- `get-gene-function`: Functional annotations
- `get-go-annotations`: Gene Ontology terms
- `search-go-terms`: GO term search
- `get-gene-pathways`: Biological pathways
- `search-pathways`: Pathway search

### Literature & References
- `get-gene-literature`: Literature references
- `search-literature-textpresso`: Full-text literature search

### Sequence Analysis
- `blast-sequence`: BLAST sequence similarity search
- `get-gene-sequence`: Gene sequence data

### Species Information
- `get-species-list`: Supported species
- `get-species-info`: Species details

### Specialized Tools
- `get-jbrowse-data`: Genome browser integration
- `get-transgenic-alleles`: Transgenic model systems
- `get-construct-info`: Transgenic construct data
- `alliancemine-query`: Complex data mining

## Best Practices

### Effective Query Strategies

1. **Be Specific**: Use official gene symbols or identifiers when possible
   - Good: "BRCA1" or "HGNC:1100"
   - Avoid: "breast cancer gene"

2. **Specify Species**: Include organism when relevant
   - Good: "mouse Trp53 gene"
   - Good: "human TP53 orthologs"

3. **Use Standard Identifiers**: Include database prefixes
   - Human: HGNC:1100
   - Mouse: MGI:104537
   - Fly: FB:FBgn0000043

4. **Combine Multiple Approaches**: Build comprehensive analyses
   - Start with gene search
   - Get detailed information
   - Find orthologs and interactions
   - Review literature

### Query Examples by Research Area

#### Cancer Research
```
"Find tumor suppressor genes and their interaction networks"
"Compare p53 pathway between human and mouse"
"Get mutation data for oncogenes in model organisms"
```

#### Neuroscience
```
"Analyze autism-related genes across species"
"Find synaptic genes with expression in brain"
"Compare neurodevelopmental pathways"
```

#### Developmental Biology
```
"Get HOX gene expression during development"
"Find morphogenetic pathway components"
"Compare developmental gene networks"
```

#### Pharmacogenomics
```
"Identify drug metabolism genes"
"Find pharmacokinetic pathway components"
"Analyze drug target orthologs"
```

## Troubleshooting

### Common Issues

1. **Gene Not Found**
   - Try alternative gene symbols
   - Check species-specific databases
   - Use broader search terms

2. **No Ortholog Data**
   - Some genes may not have characterized orthologs
   - Try related gene family members
   - Check different species combinations

3. **Limited Expression Data**
   - Expression data varies by species
   - Try different developmental stages
   - Check alternative expression resources

4. **API Timeouts**
   - Large queries may take time
   - Break complex analyses into steps
   - Retry if connection issues occur

### Getting Help

- Check gene identifiers in source databases
- Verify species names and abbreviations
- Consult Alliance Genome Resources documentation
- Use simpler queries for complex analyses

## Data Sources & Citations

The AGR MCP Server integrates data from:

- **Alliance of Genome Resources**: Primary data aggregation
- **HGNC**: Human Gene Nomenclature Committee
- **MGI**: Mouse Genome Informatics
- **RGD**: Rat Genome Database
- **ZFIN**: Zebrafish Information Network
- **FlyBase**: Drosophila database
- **WormBase**: C. elegans database
- **SGD**: Saccharomyces Genome Database
- **Xenbase**: Xenopus database

### Citing AGR Data

When using AGR data in publications, please cite:
> Alliance of Genome Resources Consortium. (2022). Harmonizing model organism data in the Alliance of Genome Resources. Genetics, 220(4), iyac022.

## Updates & Maintenance

The AGR MCP Server is regularly updated to:
- Incorporate new Alliance data releases
- Add support for additional organisms
- Enhance tool functionality
- Improve performance and reliability

Check the CLAUDE.md file for version information and update instructions.

---

*For technical support or questions, consult the main README.md or contact the development team.*