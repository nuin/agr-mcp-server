#!/usr/bin/env python3
"""
AGR MCP Server - Minimal Version

This version uses a completely different approach to avoid the Pydantic tuple issue.
We return plain dictionaries instead of Pydantic models.
"""

import asyncio
import json
import logging
import sys
import traceback
from typing import Any, Dict, List, Optional

import httpx

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AGRClient:
    """Simplified client for Alliance of Genome Resources APIs."""
    
    def __init__(self):
        self.base_url = "https://www.alliancegenome.org/api"
        self.timeout = 15.0
        
    async def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to AGR API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"Making request to: {url}")
                response = await client.get(url, params=params or {})
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"HTTP {response.status_code}: {response.text[:200]}"}
                    
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}

    async def search_genes(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search for genes."""
        params = {"q": query, "category": "gene", "limit": limit}
        return await self._make_request("/search", params)

    async def search_diseases(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search for diseases."""
        params = {"q": query, "category": "disease", "limit": limit}
        return await self._make_request("/search", params)

    async def get_gene_info(self, gene_id: str) -> Dict[str, Any]:
        """Get gene information."""
        return await self._make_request(f"/gene/{gene_id}")

# Global client
agr_client = AGRClient()

async def handle_jsonrpc_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle JSON-RPC requests directly."""
    try:
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        logger.info(f"Handling method: {method}")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "serverInfo": {
                        "name": "agr-genomics-minimal",
                        "version": "1.0.0"
                    }
                }
            }
            
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "search_genes",
                            "description": "Search for genes by symbol, name, or identifier",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string", "description": "Gene symbol or name"},
                                    "limit": {"type": "integer", "description": "Max results (default: 10)", "default": 10}
                                },
                                "required": ["query"]
                            }
                        },
                        {
                            "name": "search_diseases",
                            "description": "Search for diseases and conditions",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string", "description": "Disease name or term"},
                                    "limit": {"type": "integer", "description": "Max results (default: 10)", "default": 10}
                                },
                                "required": ["query"]
                            }
                        },
                        {
                            "name": "get_gene_info",
                            "description": "Get detailed information about a gene",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "gene_id": {"type": "string", "description": "Gene identifier"}
                                },
                                "required": ["gene_id"]
                            }
                        }
                    ]
                }
            }
            
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            logger.info(f"Tool call: {tool_name} with args: {arguments}")
            
            result_text = ""
            
            if tool_name == "search_genes":
                query = arguments.get("query", "")
                limit = arguments.get("limit", 10)
                
                if not query:
                    result_text = "Error: query parameter is required"
                else:
                    result = await agr_client.search_genes(query, limit)
                    
                    if "error" in result:
                        result_text = f"Error searching genes: {result['error']}"
                    else:
                        if "results" in result and isinstance(result["results"], list):
                            genes = result["results"][:limit]
                            if genes:
                                formatted_genes = []
                                for gene in genes:
                                    gene_info = {
                                        "symbol": gene.get("symbol", "Unknown"),
                                        "name": gene.get("name", ""),
                                        "species": gene.get("species", {}).get("name", ""),
                                        "id": gene.get("id", "")
                                    }
                                    formatted_genes.append(gene_info)
                                
                                result_text = f"Found {len(formatted_genes)} genes for '{query}':\n\n"
                                result_text += json.dumps(formatted_genes, indent=2)
                            else:
                                result_text = f"No genes found for '{query}'"
                        else:
                            result_text = f"Gene search results for '{query}':\n\n{json.dumps(result, indent=2)}"
                            
            elif tool_name == "search_diseases":
                query = arguments.get("query", "")
                limit = arguments.get("limit", 10)
                
                if not query:
                    result_text = "Error: query parameter is required"
                else:
                    result = await agr_client.search_diseases(query, limit)
                    
                    if "error" in result:
                        result_text = f"Error searching diseases: {result['error']}"
                    else:
                        result_text = f"Disease search results for '{query}':\n\n{json.dumps(result, indent=2)}"
                        
            elif tool_name == "get_gene_info":
                gene_id = arguments.get("gene_id", "")
                
                if not gene_id:
                    result_text = "Error: gene_id parameter is required"
                else:
                    result = await agr_client.get_gene_info(gene_id)
                    
                    if "error" in result:
                        result_text = f"Error getting gene info: {result['error']}"
                    else:
                        result_text = f"Gene information for {gene_id}:\n\n{json.dumps(result, indent=2)}"
            else:
                result_text = f"Unknown tool: {tool_name}"
            
            # Return the response as a plain dict - no Pydantic models
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result_text
                        }
                    ],
                    "isError": False
                }
            }
            
        elif method == "notifications/initialized":
            # No response needed for notifications
            return None
            
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
        logger.error(f"Error handling request: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }

async def main():
    """Main function - handle stdio JSON-RPC directly."""
    try:
        logger.info("Starting AGR MCP Server (Minimal Version)...")
        
        while True:
            try:
                # Read from stdin
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                    
                line = line.strip()
                if not line:
                    continue
                
                logger.info(f"Received: {line}")
                
                # Parse JSON-RPC request
                request = json.loads(line)
                
                # Handle the request
                response = await handle_jsonrpc_request(request)
                
                # Send response if not None
                if response is not None:
                    response_line = json.dumps(response)
                    print(response_line, flush=True)
                    logger.info(f"Sent: {response_line}")
                    
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
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                
    except KeyboardInterrupt:
        logger.info("Server stopped")
    except Exception as e:
        logger.error(f"Server error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())