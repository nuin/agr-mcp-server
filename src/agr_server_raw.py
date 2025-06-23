#!/usr/bin/env python3
"""
AGR MCP Server - Raw JSON-RPC Implementation

This completely bypasses the MCP Python library to avoid all Pydantic issues.
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, Optional

import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AGRClient:
    def __init__(self):
        self.base_url = "https://www.alliancegenome.org/api"
        self.timeout = 15.0
        
    async def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params or {})
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    async def search_genes(self, query: str, limit: int = 10) -> Dict[str, Any]:
        params = {"q": query, "category": "gene", "limit": limit}
        return await self._make_request("/search", params)

    async def search_diseases(self, query: str, limit: int = 10) -> Dict[str, Any]:
        params = {"q": query, "category": "disease", "limit": limit}
        return await self._make_request("/search", params)

    async def get_gene_info(self, gene_id: str) -> Dict[str, Any]:
        return await self._make_request(f"/gene/{gene_id}")

agr_client = AGRClient()

async def handle_request(request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    method = request.get("method")
    request_id = request.get("id")
    params = request.get("params", {})
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "serverInfo": {"name": "agr-genomics-raw", "version": "1.0.0"}
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
                        "description": "Search for genes",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string"},
                                "limit": {"type": "integer", "default": 10}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "search_diseases", 
                        "description": "Search for diseases",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string"},
                                "limit": {"type": "integer", "default": 10}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "get_gene_info",
                        "description": "Get gene information",
                        "inputSchema": {
                            "type": "object", 
                            "properties": {
                                "gene_id": {"type": "string"}
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
        
        result_text = ""
        
        if tool_name == "search_genes":
            query = arguments.get("query", "")
            limit = arguments.get("limit", 10)
            
            if not query:
                result_text = "Error: query required"
            else:
                result = await agr_client.search_genes(query, limit)
                if "error" in result:
                    result_text = f"Error: {result['error']}"
                else:
                    result_text = f"Gene search results:\n{json.dumps(result, indent=2)}"
        
        elif tool_name == "search_diseases":
            query = arguments.get("query", "")
            limit = arguments.get("limit", 10)
            
            if not query:
                result_text = "Error: query required"
            else:
                result = await agr_client.search_diseases(query, limit)
                if "error" in result:
                    result_text = f"Error: {result['error']}"
                else:
                    result_text = f"Disease search results:\n{json.dumps(result, indent=2)}"
        
        elif tool_name == "get_gene_info":
            gene_id = arguments.get("gene_id", "")
            
            if not gene_id:
                result_text = "Error: gene_id required"
            else:
                result = await agr_client.get_gene_info(gene_id)
                if "error" in result:
                    result_text = f"Error: {result['error']}"
                else:
                    result_text = f"Gene info:\n{json.dumps(result, indent=2)}"
        
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
        return None
    
    else:
        return {
            "jsonrpc": "2.0", 
            "id": request_id,
            "error": {"code": -32601, "message": "Method not found"}
        }

async def main():
    logger.info("Starting AGR Raw MCP Server...")
    
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            request = json.loads(line)
            response = await handle_request(request)
            
            if response:
                print(json.dumps(response), flush=True)
                
        except json.JSONDecodeError:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"}
            }
            print(json.dumps(error_response), flush=True)
        except Exception as e:
            logger.error(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())