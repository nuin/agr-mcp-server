#!/usr/bin/env python3
"""
Test the working server response format
"""

import sys
import asyncio
import json
sys.path.append('/Users/nuin/Projects/alliance/agr-mcp-server/src')

from agr_server_working import create_safe_response

def test_response_format():
    """Test that our response format doesn't convert to tuples"""
    
    # Test creating a response
    response = create_safe_response("Test message")
    
    print(f"Response type: {type(response)}")
    print(f"Response: {response}")
    print(f"Response dict: {response.__dict__}")
    
    # Test content
    print(f"Content: {response.content}")
    print(f"Content type: {type(response.content)}")
    
    if response.content:
        print(f"First content item: {response.content[0]}")
        print(f"First content type: {type(response.content[0])}")
    
    # Test serialization
    try:
        # Test model_dump (Pydantic v2)
        dumped = response.model_dump()
        print(f"\nmodel_dump(): {dumped}")
        print(f"model_dump() type: {type(dumped)}")
        
        # Check if content is properly serialized
        if 'content' in dumped:
            content = dumped['content']
            print(f"Dumped content: {content}")
            print(f"Dumped content type: {type(content)}")
            if content and isinstance(content, list):
                print(f"First dumped content item: {content[0]}")
                print(f"First dumped content type: {type(content[0])}")
        
    except Exception as e:
        print(f"\nmodel_dump() error: {e}")
    
    # Test JSON serialization
    try:
        json_str = json.dumps(response.model_dump())
        print(f"\nJSON serialization successful: {len(json_str)} characters")
        print(f"JSON preview: {json_str[:200]}...")
    except Exception as e:
        print(f"\nJSON serialization error: {e}")

if __name__ == "__main__":
    test_response_format()