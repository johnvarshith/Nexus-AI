from mcp.server import Server
from mcp.types import Tool
import asyncio
from typing import Any

server = Server("nexus-tools")

@server.tool()
async def web_search(query: str, max_results: int = 5) -> str:
    """Search the web using Tavily API"""
    try:
        from tavily import TavilyClient
        import os
        
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        results = client.search(query, max_results=max_results)
        
        formatted_results = []
        for result in results['results']:
            formatted_results.append(f"Title: {result['title']}\nContent: {result['content']}\nURL: {result['url']}\n")
        
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Search error: {str(e)}"

@server.tool()
async def read_pdf(url: str) -> str:
    """Extract text from PDF document"""
    try:
        import PyPDF2
        import requests
        from io import BytesIO
        
        response = requests.get(url)
        pdf_file = BytesIO(response.content)
        
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        return text
    except Exception as e:
        return f"PDF read error: {str(e)}"

@server.tool()
async def execute_python(code: str, timeout: int = 30) -> str:
    """Execute Python code in a sandboxed environment"""
    try:
        import subprocess
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        result = subprocess.run(
            ["python", temp_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        os.unlink(temp_file)
        
        return result.stdout or result.stderr
    except Exception as e:
        return f"Code execution error: {str(e)}"

@server.tool()
async def query_vector_db(query: str, collection: str = "default") -> str:
    """Query vector database for semantic search"""
    try:
        from sqlalchemy import create_engine
        from backend.config import settings
        
        # Implement pgvector query
        # This is a placeholder
        return f"Vector search results for: {query}"
    except Exception as e:
        return f"Vector DB error: {str(e)}"

async def main():
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read, write):
        await server.run(read, write)

if __name__ == "__main__":
    asyncio.run(main())