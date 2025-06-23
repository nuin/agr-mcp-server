#!/usr/bin/env python3
"""
Test MCP response creation to isolate the tuple issue
"""

import sys
import asyncio
from mcp.types import CallToolResult, TextContent

def test_mcp_response():
    """Test creating and serializing MCP response"""
    
    # Create a TextContent object
    text_content = TextContent(type="text", text="Test response")
    print(f"TextContent: {text_content}")
    print(f"TextContent type: {type(text_content)}")
    print(f"TextContent dict: {text_content.__dict__}")
    
    # Create CallToolResult
    result = CallToolResult(content=[text_content])
    print(f"\nCallToolResult: {result}")
    print(f"CallToolResult type: {type(result)}")
    print(f"CallToolResult dict: {result.__dict__}")
    print(f"Content: {result.content}")
    print(f"Content type: {type(result.content)}")
    
    if result.content:
        print(f"First content item: {result.content[0]}")
        print(f"First content type: {type(result.content[0])}")
    
    # Test serialization
    try:
        # Test model_dump (Pydantic v2)
        dumped = result.model_dump()
        print(f"\nmodel_dump(): {dumped}")
    except Exception as e:
        print(f"\nmodel_dump() error: {e}")
    
    try:
        # Test dict()
        dict_result = dict(result)
        print(f"\ndict(): {dict_result}")
    except Exception as e:
        print(f"\ndict() error: {e}")

if __name__ == "__main__":
    test_mcp_response()