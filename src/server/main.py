from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Import the new translation function and the model loader
from ..services.translation import translate_text_nllb, load_model

# This is the lifespan manager that FastAPI will use.
# It runs the code inside it when the server starts up.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup:
    print("Server is starting up...")
    load_model()  # <--- This is the crucial call to load the model
    yield
    # Code to run on shutdown:
    print("Server is shutting down.")

# Define the data model for the translation request body
class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

# Create the FastAPI app instance and tell it to use our lifespan manager
app = FastAPI(
    title="LinguaLink NLLB Translation Server",
    description="An API server to handle translations using a local NLLB model.",
    version="2.0.0",
    lifespan=lifespan
)

@app.post("/translate", summary="Translate Text")
async def translate(request: TranslationRequest):
    """
    Receives text and language codes, and returns the translated text
    using the loaded NLLB model.
    """
    translated_text = translate_text_nllb(
        text=request.text,
        source_lang=request.source_lang,
        target_lang=request.target_lang
    )
    return {"translation": translated_text}