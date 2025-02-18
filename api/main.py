from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from .rag import get_response

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    # Redirect to the chat interface
    return HTMLResponse('<html><body><a href="/static/index.html">Go to Chat</a></body></html>')

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    query = data.get("query", "")
    if not query:
        return JSONResponse({"error": "Empty query"}, status_code=400)
    answer = get_response(query)
    return JSONResponse({"answer": answer})
