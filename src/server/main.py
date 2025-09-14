from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Import the new translation function and the model loader
from ..services.translation import translate_text_nllb, load_model

# This is the lifespan manager that FastAPI will use.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup, load the model and store it in the app's state
    print("Server is starting up...")
    model, tokenizer, device = load_model()
    app.state.model = model
    app.state.tokenizer = tokenizer
    app.state.device = device
    yield
    # On shutdown, clear the state
    print("Server is shutting down.")
    app.state.model = None
    app.state.tokenizer = None
    app.state.device = None

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

@app.get("/", include_in_schema=False)
async def root():
    """Redirect base path to interactive API docs."""
    return RedirectResponse(url="/docs")

@app.post("/translate", summary="Translate Text")
async def translate(request: TranslationRequest):
    """
    Receives text and language codes, and returns the translated text
    using the model stored in the application state.
    """
    try:
        translated_text = translate_text_nllb(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            model=app.state.model,
            tokenizer=app.state.tokenizer,
            device=app.state.device
        )
        return {"translated_text": translated_text}
    except ValueError as e:
        # This will catch the error for unsupported languages
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Generic error for other issues
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")
