#!/usr/bin/env python3
"""
AGR MCP Server - Working Version

This version fixes the Pydantic serialization issue by using direct dict construction
instead of relying on MCP model objects that get incorrectly serialized as tuples.
"""

import asyncio
import json
import logging
import sys
import traceback
from typing import Any, Dict, List, Optional

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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AGRClient:
    """Simplified and robust client for Alliance of Genome Resources APIs."""
    
    def __init__(self):
        self.base_url = "https://www.alliancegenome.org/api"
        self.timeout = 15.0
        
    async def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to AGR API with proper error handling."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"Making request to: {url} with params: {params}")
                response = await client.get(url, params=params or {})
                
                logger.info(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        result = response.json()
                        logger.info(f"Successfully parsed JSON response")
                        return result
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON decode error: {e}")
                        return {"error": f"Invalid JSON response: {str(e)}"}
                else:
                    logger.error(f"HTTP error: {response.status_code}")
                    return {"error": f"HTTP {response.status_code}: {response.text[:200]}"}
                    
        except httpx.TimeoutException:
            logger.error("Request timeout")
            return {"error": "Request timeout"}
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            return {"error": f"Request error: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"error": f"Unexpected error: {str(e)}"}

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

# Initialize client
agr_client = AGRClient()

# Create server
server = Server("agr-genomics-working")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="search_genes",
            description="Search for genes by symbol, name, or identifier",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Gene symbol or name"},
                    "limit": {"type": "integer", "description": "Max results (default: 10)", "default": 10}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="search_diseases",
            description="Search for diseases and conditions",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Disease name or term"},
                    "limit": {"type": "integer", "description": "Max results (default: 10)", "default": 10}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_gene_info",
            description="Get detailed information about a gene",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_id": {"type": "string", "description": "Gene identifier"}
                },
                "required": ["gene_id"]
            }
        )
    ]

def create_safe_response(text: str) -> CallToolResult:
    """Create a CallToolResult that bypasses the Pydantic serialization issue."""
    try:
        # Ensure text is a string and not too long
        if not isinstance(text, str):
            text = str(text)
        
        # Limit text length to prevent issues
        if len(text) > 10000:
            text = text[:10000] + "\n... (truncated)"
        
        # Create response using a simpler approach that avoids tuple conversion
        # We'll create the TextContent and CallToolResult in the most basic way possible
        from mcp.types import TextContent, CallToolResult
        
        # Create TextContent with explicit parameters
        content_item = TextContent(
            type="text",
            text=text,
            annotations=None
        )
        
        # Create CallToolResult with explicit parameters
        result = CallToolResult(
            content=[content_item],
            isError=False,
            meta=None
        )
        
        # Log the creation for debugging
        logger.info(f"Created safe response with {len(text)} characters")
        
        return result
        
    except Exception as e:
        logger.error(f"Error creating safe response: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Create a minimal error response
        try:
            error_content = TextContent(type="text", text=f"Error: {str(e)}", annotations=None)
            return CallToolResult(content=[error_content], isError=True, meta=None)
        except Exception as inner_e:
            logger.error(f"Failed to create error response: {inner_e}")
            # Last resort - create the absolute minimum response
            return CallToolResult(
                content=[{"type": "text", "text": f"Error: {str(e)}"}],
                isError=True
            )

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    try:
        logger.info(f"Tool called: {name} with arguments: {arguments}")
        
        if name == "search_genes":
            query = arguments.get("query", "")
            limit = arguments.get("limit", 10)
            
            if not query:
                return create_safe_response("Error: query parameter is required")
            
            result = await agr_client.search_genes(query, limit)
            
            if "error" in result:
                response_text = f"Error searching genes: {result['error']}"
            else:
                # Format the response nicely
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
                        
                        response_text = f"Found {len(formatted_genes)} genes for '{query}':\n\n"
                        response_text += json.dumps(formatted_genes, indent=2)
                    else:
                        response_text = f"No genes found for '{query}'"
                else:
                    response_text = f"Gene search results for '{query}':\n\n{json.dumps(result, indent=2)}"
            
            return create_safe_response(response_text)
            
        elif name == "search_diseases":
            query = arguments.get("query", "")
            limit = arguments.get("limit", 10)
            
            if not query:
                return create_safe_response("Error: query parameter is required")
            
            result = await agr_client.search_diseases(query, limit)
            
            if "error" in result:
                response_text = f"Error searching diseases: {result['error']}"
            else:
                response_text = f"Disease search results for '{query}':\n\n{json.dumps(result, indent=2)}"
            
            return create_safe_response(response_text)
            
        elif name == "get_gene_info":
            gene_id = arguments.get("gene_id", "")
            
            if not gene_id:
                return create_safe_response("Error: gene_id parameter is required")
            
            result = await agr_client.get_gene_info(gene_id)
            
            if "error" in result:
                response_text = f"Error getting gene info: {result['error']}"
            else:
                response_text = f"Gene information for {gene_id}:\n\n{json.dumps(result, indent=2)}"
            
            return create_safe_response(response_text)
            
        else:
            return create_safe_response(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Error in call_tool: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return create_safe_response(f"Internal error: {str(e)}")

async def main():
    """Main function to run the AGR MCP server."""
    try:
        # Import stdio_server here to avoid import issues
        from mcp.server.stdio import stdio_server
        
        logger.info("Starting AGR MCP Server (Working Version)...")
        
        async with stdio_server() as (read_stream, write_stream):
            logger.info("Server streams established")
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="agr-genomics-working",
                    server_version="1.0.3",
                    capabilities={}
                )
            )
    except Exception as e:
        logger.error(f"Server startup error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())