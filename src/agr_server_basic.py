#!/usr/bin/env python3
"""
Alliance of Genome Resources (AGR) MCP Server

This server provides programmatic access to AGR's genomic data, gene searches,
identifier lookups, and bioinformatics tools through the Model Context Protocol.
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

class AGRClient:
    """Client for interacting with Alliance of Genome Resources APIs."""
    
    def __init__(self):
        self.base_url = "https://www.alliancegenome.org/api"
        self.blast_url = "https://blast.alliancegenome.org"
        self.fms_url = "https://fms.alliancegenome.org/api"
        self.timeout = 30.0
        
    async def _make_request(self, endpoint: str, params: Optional[Dict] = None, base_url: Optional[str] = None) -> Dict[str, Any]:
        """Make HTTP request to AGR API."""
        url = f"{base_url or self.base_url}/{endpoint.lstrip('/')}"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, params=params or {})
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"API request failed: {e}")
                raise Exception(f"API request failed: {str(e)}")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                raise Exception(f"Invalid JSON response: {str(e)}")

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

    async def get_gene_alleles(self, gene_id: str) -> Dict[str, Any]:
        """Get allele information for a gene."""
        return await self._make_request(f"/gene/{gene_id}/alleles")

    async def get_gene_diseases(self, gene_id: str) -> Dict[str, Any]:
        """Get disease associations for a gene."""
        return await self._make_request(f"/gene/{gene_id}/diseases")

    async def get_gene_interactions(self, gene_id: str) -> Dict[str, Any]:
        """Get interaction data for a gene."""
        return await self._make_request(f"/gene/{gene_id}/interactions")

    async def get_gene_expression(self, gene_id: str) -> Dict[str, Any]:
        """Get expression data for a gene."""
        return await self._make_request(f"/gene/{gene_id}/expression")

    async def find_orthologs(self, gene_id: str) -> Dict[str, Any]:
        """Find orthologous genes across species."""
        return await self._make_request(f"/gene/{gene_id}/orthologs")

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

    async def blast_sequence(self, sequence: str, database: str = "all", 
                           program: str = "blastn", max_target_seqs: int = 50) -> Dict[str, Any]:
        """Perform BLAST sequence search."""
        # Note: This is a simplified implementation. The actual BLAST API may require
        # different endpoints and parameters. Check AGR BLAST documentation for details.
        params = {
            "sequence": sequence,
            "database": database,
            "program": program,
            "max_target_seqs": max_target_seqs
        }
        return await self._make_request("/blast", params, self.blast_url)

    async def get_species_list(self) -> Dict[str, Any]:
        """Get list of supported species."""
        return await self._make_request("/species")

# Initialize the AGR client
agr_client = AGRClient()

# Create the MCP server
server = Server("agr-genomics")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools for the AGR MCP server."""
    return [
        Tool(
            name="search_genes",
            description="Search for genes by symbol, name, or identifier across model organisms",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Gene symbol, name, or identifier to search for"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 20)",
                        "default": 20
                    },
                    "offset": {
                        "type": "integer", 
                        "description": "Number of results to skip (default: 0)",
                        "default": 0
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_gene_info",
            description="Retrieve detailed information about a specific gene",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {
                        "type": "string",
                        "description": "Gene identifier (e.g., HGNC:5, MGI:95892, ZFIN:ZDB-GENE-030131-1)"
                    }
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="get_gene_diseases",
            description="Get disease associations for a gene",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {
                        "type": "string",
                        "description": "Gene identifier"
                    }
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="find_orthologs",
            description="Find orthologous genes across different species",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {
                        "type": "string",
                        "description": "Gene identifier to find orthologs for"
                    }
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="get_gene_interactions",
            description="Retrieve gene and protein interaction data",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {
                        "type": "string",
                        "description": "Gene identifier"
                    }
                },
                "required": ["gene_id"]
            }
        ),
        Tool(
            name="get_gene_expression",
            description="Get gene expression data and tissue-specific information",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {
                        "type": "string",
                        "description": "Gene identifier"
                    }
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
                    "query": {
                        "type": "string",
                        "description": "Disease name or term to search for"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 20)",
                        "default": 20
                    }
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
                    "query": {
                        "type": "string",
                        "description": "Phenotype term to search for"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 20)",
                        "default": 20
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="blast_sequence",
            description="Perform BLAST sequence similarity search against AGR databases",
            inputSchema={
                "type": "object",
                "properties": {
                    "sequence": {
                        "type": "string",
                        "description": "DNA, RNA, or protein sequence to search"
                    },
                    "database": {
                        "type": "string",
                        "description": "Target database (default: 'all')",
                        "default": "all"
                    },
                    "program": {
                        "type": "string",
                        "description": "BLAST program (blastn, blastp, blastx, etc.)",
                        "default": "blastn"
                    },
                    "max_target_seqs": {
                        "type": "integer",
                        "description": "Maximum number of target sequences (default: 50)",
                        "default": 50
                    }
                },
                "required": ["sequence"]
            }
        ),
        Tool(
            name="get_species_list",
            description="Get list of all supported model organisms",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls for the AGR MCP server."""
    try:
        if name == "search_genes":
            query = arguments["query"]
            limit = arguments.get("limit", 20)
            offset = arguments.get("offset", 0)
            
            result = await agr_client.search_genes(query, limit=limit, offset=offset)
            
            # Format the response
            if "results" in result:
                genes = result["results"]
                formatted_results = []
                
                for gene in genes[:limit]:
                    gene_info = {
                        "id": gene.get("id", ""),
                        "symbol": gene.get("symbol", ""),
                        "name": gene.get("name", ""),
                        "species": gene.get("species", {}).get("name", ""),
                        "description": gene.get("automatedGeneSynopsis", "")
                    }
                    formatted_results.append(gene_info)
                
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Found {len(formatted_results)} genes matching '{query}':\n\n" +
                             json.dumps(formatted_results, indent=2)
                    )]
                )
            else:
                return CallToolResult(
                    content=[TextContent(
                        type="text", 
                        text=f"No genes found matching '{query}'"
                    )]
                )

        elif name == "get_gene_info":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_gene_info(gene_id)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Gene Information for {gene_id}:\n\n" +
                         json.dumps(result, indent=2)
                )]
            )

        elif name == "get_gene_diseases":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_gene_diseases(gene_id)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Disease associations for {gene_id}:\n\n" +
                         json.dumps(result, indent=2)
                )]
            )

        elif name == "find_orthologs":
            gene_id = arguments["gene_id"]
            result = await agr_client.find_orthologs(gene_id)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Orthologs for {gene_id}:\n\n" +
                         json.dumps(result, indent=2)
                )]
            )

        elif name == "get_gene_interactions":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_gene_interactions(gene_id)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Interactions for {gene_id}:\n\n" +
                         json.dumps(result, indent=2)
                )]
            )

        elif name == "get_gene_expression":
            gene_id = arguments["gene_id"]
            result = await agr_client.get_gene_expression(gene_id)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Expression data for {gene_id}:\n\n" +
                         json.dumps(result, indent=2)
                )]
            )

        elif name == "search_diseases":
            query = arguments["query"]
            limit = arguments.get("limit", 20)
            result = await agr_client.search_diseases(query, limit=limit)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Disease search results for '{query}':\n\n" +
                         json.dumps(result, indent=2)
                )]
            )

        elif name == "search_phenotypes":
            query = arguments["query"]
            limit = arguments.get("limit", 20)
            result = await agr_client.search_phenotypes(query, limit=limit)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Phenotype search results for '{query}':\n\n" +
                         json.dumps(result, indent=2)
                )]
            )

        elif name == "blast_sequence":
            sequence = arguments["sequence"]
            database = arguments.get("database", "all")
            program = arguments.get("program", "blastn")
            max_target_seqs = arguments.get("max_target_seqs", 50)
            
            result = await agr_client.blast_sequence(
                sequence, database, program, max_target_seqs
            )
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"BLAST results for sequence (program: {program}, database: {database}):\n\n" +
                         json.dumps(result, indent=2)
                )]
            )

        elif name == "get_species_list":
            result = await agr_client.get_species_list()
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text="Supported model organisms:\n\n" +
                         json.dumps(result, indent=2)
                )]
            )

        else:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )]
            )

    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}")
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=f"Error calling tool {name}: {str(e)}"
            )]
        )

async def main():
    """Main function to run the AGR MCP server."""
    # Import here to avoid issues with circular imports
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="agr-genomics",
                server_version="1.0.0",
                capabilities={}
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
