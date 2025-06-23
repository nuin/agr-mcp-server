#!/usr/bin/env python3
"""
Enhanced Alliance of Genome Resources (AGR) MCP Server

This server provides comprehensive programmatic access to AGR's genomic data, gene searches,
identifier lookups, bioinformatics tools, literature search, data mining, and genome browsing
through the Model Context Protocol.

Based on Alliance capabilities including:
- Core gene/allele/disease data
- JBrowse genome browser integration  
- AllianceMine data mining
- Textpresso literature search
- SequenceServer BLAST
- Expression ribbon summaries
- Orthology and comparative genomics
- Pathway analysis
- Phenotype and experimental conditions
"""

import asyncio
import json
import logging
import os
import re
import urllib.parse
from typing import Any, Dict, List, Optional, Union

import httpx
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    TextContent,
    Tool,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedAGRClient:
    """Enhanced client for interacting with Alliance of Genome Resources APIs and services."""
    
    def __init__(self):
        self.base_url = "https://www.alliancegenome.org/api"
        self.blast_url = "https://blast.alliancegenome.org"
        self.fms_url = "https://fms.alliancegenome.org/api"
        self.jbrowse_url = "https://jbrowse.alliancegenome.org"
        self.textpresso_url = "https://textpresso.alliancegenome.org"
        self.alliancemine_url = "https://www.alliancegenome.org/alliancemine"
        self.timeout = 30.0
        
    async def _make_request(self, endpoint: str, params: Optional[Dict] = None, 
                           base_url: Optional[str] = None, method: str = "GET") -> Dict[str, Any]:
        """Make HTTP request to AGR API."""
        url = f"{base_url or self.base_url}/{endpoint.lstrip('/')}"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, params=params or {})
                elif method.upper() == "POST":
                    response = await client.post(url, json=params or {})
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"API request failed: {e}")
                raise Exception(f"API request failed: {str(e)}")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                raise Exception(f"Invalid JSON response: {str(e)}")

    # Core Gene and Search Functions
    async def search_genes(self, query: str, category: str = "gene", 
                          limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Search for genes using AGR search API."""
        params = {
            "q": query,
            "category": category,
            "limit": limit,
            "offset": offset
        }
        return await self._make_request("/search", params)

    async def get_gene_info(self, gene_id: str) -> Dict[str, Any]:
        """Get detailed gene information."""
        return await self._make_request(f"/gene/{gene_id}")

    async def get_gene_summary(self, gene_id: str) -> Dict[str, Any]:
        """Get gene summary information."""
        return await self._make_request(f"/gene/{gene_id}/summary")

    # Allele and Variant Functions
    async def get_gene_alleles(self, gene_id: str) -> Dict[str, Any]:
        """Get allele information for a gene."""
        return await self._make_request(f"/gene/{gene_id}/alleles")

    async def get_allele_info(self, allele_id: str) -> Dict[str, Any]:
        """Get detailed allele information."""
        return await self._make_request(f"/allele/{allele_id}")

    async def get_gene_variants(self, gene_id: str) -> Dict[str, Any]:
        """Get variant information for a gene."""
        return await self._make_request(f"/gene/{gene_id}/variants")

    # Disease and Phenotype Functions
    async def get_gene_diseases(self, gene_id: str) -> Dict[str, Any]:
        """Get disease associations for a gene."""
        return await self._make_request(f"/gene/{gene_id}/diseases")

    async def get_disease_info(self, disease_id: str) -> Dict[str, Any]:
        """Get detailed disease information."""
        return await self._make_request(f"/disease/{disease_id}")

    async def get_gene_phenotypes(self, gene_id: str) -> Dict[str, Any]:
        """Get phenotype associations for a gene."""
        return await self._make_request(f"/gene/{gene_id}/phenotypes")

    async def search_diseases(self, query: str, limit: int = 20) -> Dict[str, Any]:
        """Search for diseases."""
        params = {
            "q": query,
            "category": "disease",
            "limit": limit
        }
        return await self._make_request("/search", params)

    async def search_phenotypes(self, query: str, limit: int = 20) -> Dict[str, Any]:
        """Search for phenotypes."""
        params = {
            "q": query,
            "category": "phenotype", 
            "limit": limit
        }
        return await self._make_request("/search", params)

    # Expression and Interaction Functions
    async def get_gene_expression(self, gene_id: str) -> Dict[str, Any]:
        """Get expression data for a gene."""
        return await self._make_request(f"/gene/{gene_id}/expression")

    async def get_expression_ribbon_summary(self, gene_id: str) -> Dict[str, Any]:
        """Get expression ribbon summary for a gene."""
        return await self._make_request(f"/gene/{gene_id}/expression-ribbon-summary")

    async def get_gene_interactions(self, gene_id: str) -> Dict[str, Any]:
        """Get interaction data for a gene."""
        return await self._make_request(f"/gene/{gene_id}/interactions")

    async def get_molecular_interactions(self, gene_id: str) -> Dict[str, Any]:
        """Get molecular interaction data for a gene."""
        return await self._make_request(f"/gene/{gene_id}/molecular-interactions")

    async def get_genetic_interactions(self, gene_id: str) -> Dict[str, Any]:
        """Get genetic interaction data for a gene."""
        return await self._make_request(f"/gene/{gene_id}/genetic-interactions")

    # Orthology and Comparative Functions
    async def find_orthologs(self, gene_id: str) -> Dict[str, Any]:
        """Find orthologous genes across species."""
        return await self._make_request(f"/gene/{gene_id}/orthologs")

    async def get_homologs_by_species(self, gene_id: str, species: str) -> Dict[str, Any]:
        """Get homologs for a specific species."""
        params = {"species": species}
        return await self._make_request(f"/gene/{gene_id}/orthologs", params)

    async def get_paralogs(self, gene_id: str) -> Dict[str, Any]:
        """Get paralogous genes within the same species."""
        return await self._make_request(f"/gene/{gene_id}/paralogs")

    # Gene Ontology and Function
    async def get_gene_function(self, gene_id: str) -> Dict[str, Any]:
        """Get gene function annotations (GO terms)."""
        return await self._make_request(f"/gene/{gene_id}/function")

    async def get_go_annotations(self, gene_id: str) -> Dict[str, Any]:
        """Get Gene Ontology annotations for a gene."""
        return await self._make_request(f"/gene/{gene_id}/go-annotations")

    async def search_go_terms(self, query: str, limit: int = 20) -> Dict[str, Any]:
        """Search for Gene Ontology terms."""
        params = {
            "q": query,
            "category": "go",
            "limit": limit
        }
        return await self._make_request("/search", params)

    # Pathway Functions
    async def get_gene_pathways(self, gene_id: str) -> Dict[str, Any]:
        """Get pathway associations for a gene."""
        return await self._make_request(f"/gene/{gene_id}/pathways")

    async def search_pathways(self, query: str, limit: int = 20) -> Dict[str, Any]:
        """Search for biological pathways."""
        params = {
            "q": query,
            "category": "pathway",
            "limit": limit
        }
        return await self._make_request("/search", params)

    # Literature and References
    async def get_gene_literature(self, gene_id: str) -> Dict[str, Any]:
        """Get literature references for a gene."""
        return await self._make_request(f"/gene/{gene_id}/literature")

    async def search_literature_textpresso(self, query: str, species: str = "all",
                                         category: str = "gene", limit: int = 20) -> Dict[str, Any]:
        """Search literature using Textpresso."""
        params = {
            "query": query,
            "species": species,
            "category": category,
            "limit": limit
        }
        return await self._make_request("/search", params, self.textpresso_url)

    # Sequence and BLAST Functions
    async def blast_sequence(self, sequence: str, database: str = "all", 
                           program: str = "blastn", max_target_seqs: int = 50) -> Dict[str, Any]:
        """Perform BLAST sequence search."""
        params = {
            "sequence": sequence,
            "database": database,
            "program": program,
            "max_target_seqs": max_target_seqs
        }
        return await self._make_request("/blast", params, self.blast_url)

    async def get_gene_sequence(self, gene_id: str, sequence_type: str = "genomic") -> Dict[str, Any]:
        """Get gene sequence data."""
        params = {"type": sequence_type}
        return await self._make_request(f"/gene/{gene_id}/sequence", params)

    # Species and Model Organism Functions
    async def get_species_list(self) -> Dict[str, Any]:
        """Get list of supported species."""
        return await self._make_request("/species")

    async def get_species_info(self, species_id: str) -> Dict[str, Any]:
        """Get detailed species information."""
        return await self._make_request(f"/species/{species_id}")

    async def get_model_organisms(self) -> Dict[str, Any]:
        """Get list of model organisms."""
        return await self._make_request("/model-organisms")

    # Data Mining and Complex Queries
    async def alliancemine_query(self, query_xml: str) -> Dict[str, Any]:
        """Execute AllianceMine query."""
        params = {"query": query_xml}
        return await self._make_request("/query", params, self.alliancemine_url, "POST")

    async def get_download_links(self, data_type: str = "all") -> Dict[str, Any]:
        """Get data download links."""
        params = {"type": data_type}
        return await self._make_request("/downloads", params)

    # JBrowse Integration
    async def get_jbrowse_data(self, species: str, chromosome: str, 
                              start: int, end: int) -> Dict[str, Any]:
        """Get JBrowse genome browser data."""
        params = {
            "species": species,
            "chr": chromosome,
            "start": start,
            "end": end
        }
        return await self._make_request("/tracks", params, self.jbrowse_url)

    # Experimental Conditions
    async def get_experimental_conditions(self, entity_id: str) -> Dict[str, Any]:
        """Get experimental conditions for phenotype/disease annotations."""
        return await self._make_request(f"/experimental-conditions/{entity_id}")

    # Transgenic and Construct Data
    async def get_transgenic_alleles(self, gene_id: str) -> Dict[str, Any]:
        """Get transgenic alleles for a gene."""
        return await self._make_request(f"/gene/{gene_id}/transgenic-alleles")

    async def get_construct_info(self, construct_id: str) -> Dict[str, Any]:
        """Get construct information."""
        return await self._make_request(f"/construct/{construct_id}")

# Initialize the enhanced AGR client
agr_client = EnhancedAGRClient()

# Create the MCP server
server = Server("agr-genomics-enhanced")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools for the enhanced AGR MCP server."""
    return [
        # Core Gene Search and Information
        Tool(
            name="search_genes",
            description="Search for genes by symbol, name, or identifier across model organisms",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Gene symbol, name, or identifier"},
                    "limit": {"type": "integer", "description": "Maximum results (default: 20)", "default": 20},
                    "offset": {"type": "integer", "description": "Results to skip (default: 0)", "default": 0}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_gene_info",
            description="Retrieve comprehensive gene information including summary, function, and annotations",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier (e.g., HGNC:5, MGI:95892)"}
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="get_gene_summary",
            description="Get concise gene summary with key functional information",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),

        # Allele and Variant Tools
        Tool(
            name="get_gene_alleles",
            description="Get all alleles associated with a gene including phenotypic effects",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="get_allele_info", 
            description="Get detailed information about a specific allele",
            inputSchema={
                "type": "object",
                "properties": {
                    "allele_id": {"type": "string", "description": "Allele identifier"}
                },
                "required": ["allele_id"]
            }
        ),
        Tool(
            name="get_gene_variants",
            description="Get sequence variants for a gene",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),

        # Disease and Phenotype Tools
        Tool(
            name="get_gene_diseases",
            description="Get disease associations and models for a gene",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="get_disease_info",
            description="Get comprehensive information about a disease",
            inputSchema={
                "type": "object",
                "properties": {
                    "disease_id": {"type": "string", "description": "Disease identifier (DO term)"}
                },
                "required": ["disease_id"]
            }
        ),
        Tool(
            name="get_gene_phenotypes",
            description="Get phenotype annotations and experimental conditions for a gene",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="search_diseases",
            description="Search for diseases and conditions",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Disease name or term"},
                    "limit": {"type": "integer", "description": "Maximum results (default: 20)", "default": 20}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="search_phenotypes",
            description="Search for phenotypes and their associations",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Phenotype term"},
                    "limit": {"type": "integer", "description": "Maximum results (default: 20)", "default": 20}
                },
                "required": ["query"]
            }
        ),

        # Expression and Interaction Tools
        Tool(
            name="get_gene_expression",
            description="Get comprehensive gene expression data across tissues and conditions",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="get_expression_ribbon_summary",
            description="Get expression ribbon summary for visualization across anatomy and life stages",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="get_molecular_interactions",
            description="Get protein-protein and molecular interactions for a gene",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="get_genetic_interactions",
            description="Get genetic interactions and epistasis data for a gene",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),

        # Orthology and Comparative Genomics
        Tool(
            name="find_orthologs",
            description="Find orthologous genes across all species in the Alliance",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="get_homologs_by_species",
            description="Get homologs for a specific target species",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"},
                    "species": {"type": "string", "description": "Target species (e.g., 'Homo sapiens', 'Mus musculus')"}
                },
                "required": ["gene_id", "species"]
            }
        ),
        Tool(
            name="get_paralogs",
            description="Get paralogous genes within the same species",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),

        # Gene Ontology and Function
        Tool(
            name="get_gene_function",
            description="Get functional annotations and Gene Ontology terms for a gene",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="get_go_annotations",
            description="Get detailed Gene Ontology annotations with evidence codes",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="search_go_terms",
            description="Search for Gene Ontology terms and definitions",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "GO term name or ID"},
                    "limit": {"type": "integer", "description": "Maximum results (default: 20)", "default": 20}
                },
                "required": ["query"]
            }
        ),

        # Pathway Analysis
        Tool(
            name="get_gene_pathways",
            description="Get biological pathways associated with a gene",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="search_pathways",
            description="Search for biological pathways and networks",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Pathway name or description"},
                    "limit": {"type": "integer", "description": "Maximum results (default: 20)", "default": 20}
                },
                "required": ["query"]
            }
        ),

        # Literature and References
        Tool(
            name="get_gene_literature",
            description="Get literature references and citations for a gene",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="search_literature_textpresso",
            description="Search literature using Textpresso full-text search system",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search terms for literature"},
                    "species": {"type": "string", "description": "Species filter (default: 'all')", "default": "all"},
                    "category": {"type": "string", "description": "Category filter (default: 'gene')", "default": "gene"},
                    "limit": {"type": "integer", "description": "Maximum results (default: 20)", "default": 20}
                },
                "required": ["query"]
            }
        ),

        # Sequence Analysis
        Tool(
            name="blast_sequence",
            description="Perform BLAST sequence similarity search against Alliance databases",
            inputSchema={
                "type": "object",
                "properties": {
                    "sequence": {"type": "string", "description": "DNA, RNA, or protein sequence"},
                    "database": {"type": "string", "description": "Target database (default: 'all')", "default": "all"},
                    "program": {"type": "string", "description": "BLAST program (default: 'blastn')", "default": "blastn"},
                    "max_target_seqs": {"type": "integer", "description": "Maximum targets (default: 50)", "default": 50}
                },
                "required": ["sequence"]
            }
        ),
        Tool(
            name="get_gene_sequence",
            description="Get gene sequence data (genomic, transcript, protein)",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"},
                    "sequence_type": {"type": "string", "description": "Sequence type (genomic, transcript, protein)", "default": "genomic"}
                },
                "required": ["gene_id"]
            }
        ),

        # Species and Model Organisms
        Tool(
            name="get_species_list",
            description="Get list of all supported model organisms and species",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_species_info",
            description="Get detailed information about a specific species",
            inputSchema={
                "type": "object",
                "properties": {
                    "species_id": {"type": "string", "description": "Species identifier or name"}
                },
                "required": ["species_id"]
            }
        ),

        # JBrowse Genome Browser Integration
        Tool(
            name="get_jbrowse_data",
            description="Get genome browser data for visualization of genomic regions",
            inputSchema={
                "type": "object",
                "properties": {
                    "species": {"type": "string", "description": "Species name"},
                    "chromosome": {"type": "string", "description": "Chromosome identifier"},
                    "start": {"type": "integer", "description": "Start position"},
                    "end": {"type": "integer", "description": "End position"}
                },
                "required": ["species", "chromosome", "start", "end"]
            }
        ),

        # Transgenic and Construct Data
        Tool(
            name="get_transgenic_alleles",
            description="Get transgenic alleles and model systems for a gene",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="get_construct_info",
            description="Get information about transgenic constructs",
            inputSchema={
                "type": "object",
                "properties": {
                    "construct_id": {"type": "string", "description": "Construct identifier"}
                },
                "required": ["construct_id"]
            }
        ),

        # Data Downloads and Mining
        Tool(
            name="get_download_links",
            description="Get links to download Alliance data files",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_type": {"type": "string", "description": "Data type to download (default: 'all')", "default": "all"}
                },
                "required": []
            }
        ),
        Tool(
            name="alliancemine_query",
            description="Execute complex data mining queries using AllianceMine",
            inputSchema={
                "type": "object",
                "properties": {
                    "query_xml": {"type": "string", "description": "AllianceMine XML query"}
                },
                "required": ["query_xml"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls for the enhanced AGR MCP server."""
    try:
        # Core Gene Functions
        if name == "search_genes":
            query = arguments["query"]
            limit = arguments.get("limit", 20)
            offset = arguments.get("offset", 0)
            result = await agr_client.search_genes(query, limit=limit, offset=offset)
            return CallToolResult(content=[TextContent(type="text", 
                text=f"Gene search results for '{query}':\n\n{json.dumps(result, indent=2)}")])

        elif name == "get_gene_info":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_gene_info(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Gene information for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "get_gene_summary":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_gene_summary(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Gene summary for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        # Allele and Variant Functions
        elif name == "get_gene_alleles":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_gene_alleles(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Alleles for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "get_allele_info":
            allele_id = arguments["allele_id"]
            result = await agr_client.get_allele_info(allele_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Allele information for {allele_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "get_gene_variants":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_gene_variants(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Variants for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        # Disease and Phenotype Functions
        elif name == "get_gene_diseases":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_gene_diseases(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Disease associations for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "get_disease_info":
            disease_id = arguments["disease_id"]
            result = await agr_client.get_disease_info(disease_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Disease information for {disease_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "get_gene_phenotypes":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_gene_phenotypes(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Phenotypes for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "search_diseases":
            query = arguments["query"]
            limit = arguments.get("limit", 20)
            result = await agr_client.search_diseases(query, limit=limit)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Disease search results for '{query}':\n\n{json.dumps(result, indent=2)}")])

        elif name == "search_phenotypes":
            query = arguments["query"]
            limit = arguments.get("limit", 20)
            result = await agr_client.search_phenotypes(query, limit=limit)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Phenotype search results for '{query}':\n\n{json.dumps(result, indent=2)}")])

        # Expression and Interaction Functions
        elif name == "get_gene_expression":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_gene_expression(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Expression data for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "get_expression_ribbon_summary":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_expression_ribbon_summary(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Expression ribbon summary for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "get_molecular_interactions":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_molecular_interactions(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Molecular interactions for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "get_genetic_interactions":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_genetic_interactions(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Genetic interactions for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        # Orthology Functions
        elif name == "find_orthologs":
            gene_id = arguments["gene_id"]
            result = await agr_client.find_orthologs(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Orthologs for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "get_homologs_by_species":
            gene_id = arguments["gene_id"]
            species = arguments["species"]
            result = await agr_client.get_homologs_by_species(gene_id, species)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Homologs in {species} for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "get_paralogs":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_paralogs(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Paralogs for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        # Gene Ontology Functions
        elif name == "get_gene_function":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_gene_function(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Functional annotations for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "get_go_annotations":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_go_annotations(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"GO annotations for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "search_go_terms":
            query = arguments["query"]
            limit = arguments.get("limit", 20)
            result = await agr_client.search_go_terms(query, limit=limit)
            return CallToolResult(content=[TextContent(type="text",
                text=f"GO term search results for '{query}':\n\n{json.dumps(result, indent=2)}")])

        # Pathway Functions
        elif name == "get_gene_pathways":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_gene_pathways(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Pathways for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "search_pathways":
            query = arguments["query"]
            limit = arguments.get("limit", 20)
            result = await agr_client.search_pathways(query, limit=limit)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Pathway search results for '{query}':\n\n{json.dumps(result, indent=2)}")])

        # Literature Functions
        elif name == "get_gene_literature":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_gene_literature(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Literature for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "search_literature_textpresso":
            query = arguments["query"]
            species = arguments.get("species", "all")
            category = arguments.get("category", "gene")
            limit = arguments.get("limit", 20)
            result = await agr_client.search_literature_textpresso(query, species, category, limit)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Textpresso literature search for '{query}':\n\n{json.dumps(result, indent=2)}")])

        # Sequence Functions
        elif name == "blast_sequence":
            sequence = arguments["sequence"]
            database = arguments.get("database", "all")
            program = arguments.get("program", "blastn")
            max_target_seqs = arguments.get("max_target_seqs", 50)
            result = await agr_client.blast_sequence(sequence, database, program, max_target_seqs)
            return CallToolResult(content=[TextContent(type="text",
                text=f"BLAST results:\n\n{json.dumps(result, indent=2)}")])

        elif name == "get_gene_sequence":
            gene_id = arguments["gene_id"]
            sequence_type = arguments.get("sequence_type", "genomic")
            result = await agr_client.get_gene_sequence(gene_id, sequence_type)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Sequence data for {gene_id} ({sequence_type}):\n\n{json.dumps(result, indent=2)}")])

        # Species Functions
        elif name == "get_species_list":
            result = await agr_client.get_species_list()
            return CallToolResult(content=[TextContent(type="text",
                text=f"Supported species:\n\n{json.dumps(result, indent=2)}")])

        elif name == "get_species_info":
            species_id = arguments["species_id"]
            result = await agr_client.get_species_info(species_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Species information for {species_id}:\n\n{json.dumps(result, indent=2)}")])

        # JBrowse Functions
        elif name == "get_jbrowse_data":
            species = arguments["species"]
            chromosome = arguments["chromosome"]
            start = arguments["start"]
            end = arguments["end"]
            result = await agr_client.get_jbrowse_data(species, chromosome, start, end)
            return CallToolResult(content=[TextContent(type="text",
                text=f"JBrowse data for {species} {chromosome}:{start}-{end}:\n\n{json.dumps(result, indent=2)}")])

        # Transgenic Functions
        elif name == "get_transgenic_alleles":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_transgenic_alleles(gene_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Transgenic alleles for {gene_id}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "get_construct_info":
            construct_id = arguments["construct_id"]
            result = await agr_client.get_construct_info(construct_id)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Construct information for {construct_id}:\n\n{json.dumps(result, indent=2)}")])

        # Data Mining Functions
        elif name == "get_download_links":
            data_type = arguments.get("data_type", "all")
            result = await agr_client.get_download_links(data_type)
            return CallToolResult(content=[TextContent(type="text",
                text=f"Download links for {data_type}:\n\n{json.dumps(result, indent=2)}")])

        elif name == "alliancemine_query":
            query_xml = arguments["query_xml"]
            result = await agr_client.alliancemine_query(query_xml)
            return CallToolResult(content=[TextContent(type="text",
                text=f"AllianceMine query results:\n\n{json.dumps(result, indent=2)}")])

        else:
            return CallToolResult(content=[TextContent(type="text", text=f"Unknown tool: {name}")])

    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}")
        return CallToolResult(content=[TextContent(type="text", text=f"Error calling tool {name}: {str(e)}")])

async def main():
    """Main function to run the enhanced AGR MCP server."""
    from mcp.server.stdio import stdio_server 
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="agr-genomics-enhanced",
                server_version="2.0.0"
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
