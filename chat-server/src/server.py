import logging
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import markdown

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ollama-client-session")

app = FastAPI()
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class OllamaClient:
    def __init__(self):
        # Get Ollama model from environment variable or use default
        ollama_model = os.environ.get("OLLAMA_MODEL", "gpt-oss:20b")
        logger.info(f"Using Ollama model: {ollama_model}")

        # Configure Ollama with optimized parameters
        self.llm = ChatOllama(
            model=ollama_model,
            validate_model_on_init=True,
            temperature=0.8,
            num_ctx=32000,  # Large context window for complex tasks
            base_url="http://localhost:11434",
        )

        
        # Cache for storing frequently accessed data
        self.cache = {}
    async def sendMessage(self,message:str)->str:
        # Initialize conversation history for continuous context
        messages:list[SystemMessage|HumanMessage|AIMessage] = [
            SystemMessage(content="""You are a helpful assistant.""")
        ]
        messages.append(HumanMessage(content=f"Task: {message}"))
        try:
            response = await self.llm.ainvoke(messages)
            print(f"\nOllama's output:\n{response.content}")
            return response.content
        except KeyboardInterrupt:
                logger.info("\nTask execution interrupted by user.")
                print("\n\n👋 Goodbye!")
                return "\nTask execution interrupted by user.\n\n👋 Goodbye!"
        except EOFError:
                return ""
        except Exception as e:
                logger.error(f"Error during execution: {str(e)}", exc_info=True)
                return f"Error during execution: {str(e)}"

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.clients:dict[int,OllamaClient]={}

    async def connect(self, clientId:int, websocket: WebSocket):
        if len(self.active_connections) > 2:
             print("Maximum 3 connections allowed")
             return
        await websocket.accept()
        self.active_connections.append(websocket)
        self.clients[clientId] = OllamaClient()

    def disconnect(self, clientId:int, websocket: WebSocket):
        self.active_connections.remove(websocket)
        self.clients.pop(clientId)

    async def send_personal_message(self, clientId:int, message: str, websocket: WebSocket):
        try:
            if clientId not in self.clients:
                 await websocket.send_text('Unknown Error in processing query')
            answer = await self.clients[clientId].sendMessage(message)
            html_content = markdown.markdown(answer)
            await websocket.send_text(html_content)
        except Exception as e:
             await websocket.send_text('Unknown Error in processing query')
             

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)



manager = ConnectionManager()

@app.get("/")
async def main():
    return {"Health": "OK"}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(client_id, data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(client_id,websocket)
