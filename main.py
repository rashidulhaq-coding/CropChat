# import os
# import uuid
# from dotenv import load_dotenv
# from fastapi import FastAPI, HTTPException,Request,Depends
# from fastapi.responses import JSONResponse
# from models import get_db,ConversationHistory
# from sqlalchemy.orm import Session

# from langchain.chains import ConversationChain
# from langchain.memory import ConversationBufferMemory
# from langchain.chat_models import ChatOpenAI
# from langchain.chat_models import AzureChatOpenAI

# from pydantic import BaseModel


# load_dotenv()

# app = FastAPI()



# memory = ConversationBufferMemory()

# class ChatRequest(BaseModel):
#     user_id: str
#     memory: str
#    # Initialize the conversational model (e.g., OpenAI GPT)
# model_name = "gpt-4o" 

# os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("API_TOKEN")
# os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
# os.environ["OPENAI_API_VERSION"] = "2023-05-15"  # Set the API version here


# llm = AzureChatOpenAI(
#     model=model_name,
#     temperature=0.7
# )
#    # Create the conversational chain
# conversation = ConversationChain(
#        llm=llm,
#        memory=memory
# )

# def save_memory(user_id, memory_data,session: Session = Depends(get_db)):

#     conversation = session.query(ConversationHistory).filter_by(user_id=user_id).first()
#     if conversation:
#         conversation.memory = memory_data
#     else:
#         conversation = ConversationHistory(user_id=user_id, memory=memory_data)
#         session.add(conversation)
#     session.commit()

# def load_memory(user_id,session: Session = Depends(get_db)):

#     conversation = session.query(ConversationHistory).filter_by(user_id=user_id).first()

#     return conversation.memory if conversation else None




# @app.post("/chat")
# async def chat_with_bot(user_id:str):
#        # Load memory for the user
#     previous_memory = load_memory(user_id)
#     if previous_memory:
#         memory.load_memory(previous_memory)

#        # Process the user's message
#     response = conversation.predict()

#        # Save the updated memory
#     save_memory(user_id, memory.buffer)

#     return {"response": response}

# @app.post("/new_chat")
# async def new_chat(request: Request,session: Session = Depends(get_db)):
#     user_id = uuid.uuid4()
#     memory = ConversationBufferMemory()
#     save_memory(str(user_id), memory.buffer,session)

#     return {"user_id": str(user_id), "memory": memory.buffer}


import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from models import get_db, ConversationHistory, SessionLocal
from sqlalchemy.orm import Session

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import AzureChatOpenAI

from pydantic import BaseModel

load_dotenv()

app = FastAPI()

memory = ConversationBufferMemory()

class ChatRequest(BaseModel):
    user_id: str
    message: str  # Changed 'memory' to 'message'

# Initialize the conversational model (e.g., OpenAI GPT)
model_name = "gpt-4o"

os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("API_TOKEN")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["OPENAI_API_VERSION"] = "2023-05-15"  # Set the API version here

llm = AzureChatOpenAI(
    model=model_name,
    temperature=0.7
)
# Create the conversational chain
conversation = ConversationChain(
    llm=llm,
    memory=memory
)

def save_memory(user_id, memory_data, session: Session = Depends(get_db)):
    conversation = session.query(ConversationHistory).filter_by(user_id=user_id).first()
    if conversation:
        conversation.memory = memory_data
    else:
        conversation = ConversationHistory(user_id=user_id, memory=memory_data)
        session.add(conversation)
    session.commit()
    # session.close() # Removed this line

def load_memory(user_id, session: Session = Depends(get_db)):
    conversation = session.query(ConversationHistory).filter_by(user_id=user_id).first()
    # session.close() # Removed this line
    return conversation.memory if conversation else None

@app.post("/chat")
async def chat_with_bot(request: ChatRequest, session: Session = Depends(get_db)):
    # Load memory for the user
    previous_memory = load_memory(request.user_id, session)
    if previous_memory:
        memory.chat_memory(previous_memory)

    # Process the user's message
    response = conversation.predict(input=request.message) # Changed invoke to predict

    # Save the updated memory
    save_memory(request.user_id, memory.buffer, session)

    return {"response": response}

@app.post("/new_chat")
async def new_chat(request: Request, session: Session = Depends(get_db)):
    user_id = uuid.uuid4()
    memory = ConversationBufferMemory()
    save_memory(str(user_id), memory.buffer, session)

    return {"user_id": str(user_id), "memory": memory.buffer}
