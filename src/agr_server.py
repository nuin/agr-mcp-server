#!/usr/bin/env python3
"""
Alliance of Genome Resources (AGR) MCP Server

A Model Context Protocol server providing elegant access to AGR's comprehensive
genomic database, supporting gene searches, disease associations, and detailed
gene information across 8 model organisms.

This implementation bypasses MCP framework serialization issues by handling
JSON-RPC protocol directly while maintaining full MCP compliance.
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional

import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AGRClient:
    """Elegant client for Alliance of Genome Resources APIs."""
    
    def __init__(self):
        self.base_url = "https://www.alliancegenome.org/api"
        self.timeout = 30.0
        
    async def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make robust HTTP request with comprehensive error handling."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.debug(f"Requesting: {url} with params: {params}")
                response = await client.get(url, params=params or {})
                
                if response.status_code == 200:
                    data = response.json()
                    logger.debug(f"Successfully retrieved {len(str(data))} characters")
                    return data
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text[:200]}"
                    logger.warning(error_msg)
                    return {"error": error_msg}
                    
        except httpx.TimeoutException:
            error_msg = "Request timeout - AGR API may be slow"
            logger.error(error_msg)
            return {"error": error_msg}
        except httpx.RequestError as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON response: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}

    async def search_genes(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search for genes by symbol, name, or identifier."""
        params = {"q": query, "category": "gene", "limit": limit}
        return await self._make_request("/search", params)

    async def search_diseases(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search for diseases and conditions."""
        params = {"q": query, "category": "disease", "limit": limit}
        return await self._make_request("/search", params)

    async def get_gene_info(self, gene_id: str) -> Dict[str, Any]:
        """Get detailed gene information by identifier."""
        return await self._make_request(f"/gene/{gene_id}")


class MCPServer:
    """Elegant MCP server implementation with direct JSON-RPC handling."""
    
    def __init__(self):
        self.agr_client = AGRClient()
        self.tools = self._define_tools()
        
    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define available tools with comprehensive schemas."""
        return [
            {
                "name": "search_genes",
                "description": "Search for genes by symbol, name, or identifier across 8 model organisms",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Gene symbol (e.g., BRCA1), name, or identifier"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return",
                            "default": 10,
                            "minimum": 1,
                            "maximum": 50
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "search_diseases",
                "description": "Search for diseases and medical conditions with gene associations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Disease name or medical term (e.g., diabetes, cancer)"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return",
                            "default": 10,
                            "minimum": 1,
                            "maximum": 50
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_gene_info",
                "description": "Get comprehensive information about a specific gene",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "gene_id": {
                            "type": "string",
                            "description": "Gene identifier (e.g., HGNC:1100, MGI:88276, FB:FBgn0000008)"
                        }
                    },
                    "required": ["gene_id"]
                }
            }
        ]

    def _format_gene_results(self, results: List[Dict], query: str, limit: int) -> str:
        """Format gene search results elegantly."""
        if not results:
            return f"No genes found for '{query}'"
            
        formatted_genes = []
        for gene in results[:limit]:
            gene_info = {
                "symbol": gene.get("symbol", "Unknown"),
                "name": gene.get("name", ""),
                "species": gene.get("species", {}).get("name", ""),
                "id": gene.get("id", ""),
                "biotype": gene.get("soTermName", "")
            }
            formatted_genes.append(gene_info)
        
        header = f"Found {len(formatted_genes)} genes for '{query}':\n\n"
        return header + json.dumps(formatted_genes, indent=2)

    def _format_disease_results(self, data: Dict, query: str) -> str:
        """Format disease search results elegantly."""
        if "results" in data and data["results"]:
            diseases = data["results"]
            formatted_diseases = []
            
            for disease in diseases:
                disease_info = {
                    "name": disease.get("name", "Unknown"),
                    "id": disease.get("id", ""),
                    "definition": disease.get("definition", "")[:200] + "..." if disease.get("definition", "") else "",
                    "associated_genes": len(disease.get("associatedGenes", []))
                }
                formatted_diseases.append(disease_info)
            
            header = f"Found {len(formatted_diseases)} diseases for '{query}':\n\n"
            return header + json.dumps(formatted_diseases, indent=2)
        else:
            return f"No diseases found for '{query}'"

    async def _handle_search_genes(self, arguments: Dict[str, Any]) -> str:
        """Handle gene search with elegant formatting."""
        query = arguments.get("query", "").strip()
        limit = min(arguments.get("limit", 10), 50)
        
        if not query:
            return "Error: Gene query is required (e.g., 'BRCA1', 'insulin')"
        
        result = await self.agr_client.search_genes(query, limit)
        
        if "error" in result:
            return f"Gene search failed: {result['error']}"
        
        if "results" in result and isinstance(result["results"], list):
            return self._format_gene_results(result["results"], query, limit)
        else:
            return f"Unexpected response format for gene search '{query}'"

    async def _handle_search_diseases(self, arguments: Dict[str, Any]) -> str:
        """Handle disease search with elegant formatting."""
        query = arguments.get("query", "").strip()
        limit = min(arguments.get("limit", 10), 50)
        
        if not query:
            return "Error: Disease query is required (e.g., 'diabetes', 'cancer')"
        
        result = await self.agr_client.search_diseases(query, limit)
        
        if "error" in result:
            return f"Disease search failed: {result['error']}"
        
        return self._format_disease_results(result, query)

    async def _handle_get_gene_info(self, arguments: Dict[str, Any]) -> str:
        """Handle gene information retrieval with elegant formatting."""
        gene_id = arguments.get("gene_id", "").strip()
        
        if not gene_id:
            return "Error: Gene identifier is required (e.g., 'HGNC:1100', 'MGI:88276')"
        
        result = await self.agr_client.get_gene_info(gene_id)
        
        if "error" in result:
            return f"Gene information retrieval failed: {result['error']}"
        
        # Format key gene information elegantly
        if "symbol" in result:
            gene_summary = {
                "symbol": result.get("symbol"),
                "name": result.get("name"),
                "species": result.get("species", {}).get("name"),
                "biotype": result.get("soTermName"),
                "description": result.get("description", "")[:300] + "..." if result.get("description") else "",
                "synonyms": result.get("synonyms", [])[:5],  # First 5 synonyms
                "chromosome": result.get("genomeLocations", [{}])[0].get("chromosome") if result.get("genomeLocations") else None
            }
            
            header = f"Gene Information for {gene_id}:\n\n"
            return header + json.dumps(gene_summary, indent=2)
        else:
            return f"Gene information for {gene_id}:\n\n{json.dumps(result, indent=2)}"

    async def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle incoming JSON-RPC requests elegantly."""
        method = request.get("method")
        request_id = request.get("id")
        params = request.get("params", {})
        
        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "serverInfo": {
                            "name": "agr-genomics",
                            "version": "2.0.0"
                        }
                    }
                }
            
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"tools": self.tools}
                }
            
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                logger.info(f"Tool call: {tool_name} with arguments: {arguments}")
                
                if tool_name == "search_genes":
                    result_text = await self._handle_search_genes(arguments)
                elif tool_name == "search_diseases":
                    result_text = await self._handle_search_diseases(arguments)
                elif tool_name == "get_gene_info":
                    result_text = await self._handle_get_gene_info(arguments)
                else:
                    result_text = f"Unknown tool: {tool_name}"
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": result_text}],
                        "isError": False
                    }
                }
            
            elif method == "notifications/initialized":
                return None  # No response needed for notifications
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": "Method not found"
                    }
                }
        
        except Exception as e:
            logger.error(f"Error handling {method}: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }

    async def run(self):
        """Run the MCP server with elegant error handling."""
        logger.info("Starting Alliance of Genome Resources MCP Server v2.0.0")
        logger.info("Supporting 8 model organisms with comprehensive genomic data")
        
        try:
            while True:
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    logger.info("EOF received, shutting down")
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request = json.loads(line)
                    response = await self.handle_request(request)
                    
                    if response is not None:
                        output = json.dumps(response)
                        print(output, flush=True)
                        logger.debug(f"Sent response: {output[:100]}...")
                        
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}")
            sys.exit(1)


async def main():
    """Main entry point."""
    server = MCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())