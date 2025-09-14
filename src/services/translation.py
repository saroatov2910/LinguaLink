from typing import Dict, Optional, Tuple
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# --- Model and Tokenizer Loading ---
MODEL_NAME = "facebook/nllb-200-distilled-600M"

def load_model() -> Tuple[AutoModelForSeq2SeqLM, AutoTokenizer, str]:
    """Load the NLLB model and tokenizer and return (model, tokenizer, device)."""
    print("Loading NLLB model and tokenizer...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(device)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    print("Model and tokenizer loaded successfully.")
    # This is the critical line that was missing
    return model, tokenizer, device

# --- Language Code Mapping ---
NLLB_LANGUAGE_CODES: Dict[str, str] = {
    "en": "eng_Latn",
    "es": "spa_Latn",
    "he": "heb_Hebr",
    "ru": "rus_Cyrl",
    # Align with config.language_codes: Arabic uses arb_Arab (Modern Standard Arabic)
    "ar": "arb_Arab",
    # Add common languages present in config
    "fr": "fra_Latn",
    "de": "deu_Latn",
}

# --- Helpers ---
def _normalize_lang_input(code: Optional[str]) -> Optional[str]:
    """Normalize user-provided language code to a short ISO-like form or full NLLB tag.

    - Trims whitespace, lowercases short codes, folds subtags (e.g., en-US -> en) unless full NLLB tag already.
    - Applies common aliases (iw -> he).
    """
    if not code:
        return None
    raw = code.strip()
    if not raw:
        return None
    if "_" in raw:
        # Assume full NLLB tag like 'eng_Latn'
        return raw
    short = raw.split("-", 1)[0].lower()
    aliases = {
        "iw": "he",  # legacy Hebrew
    }
    return aliases.get(short, short)


def _resolve_nllb_code(norm: Optional[str]) -> Optional[str]:
    """Return a valid NLLB tag for a normalized input or None if unsupported."""
    if not norm:
        return None
    if "_" in norm:
        return norm
    return NLLB_LANGUAGE_CODES.get(norm)


def _get_target_lang_token_id(tokenizer: AutoTokenizer, nllb_target: str) -> Optional[int]:
    """Resolve the forced_bos_token_id for a target NLLB language across tokenizer variants."""
    if hasattr(tokenizer, "lang_code_to_id") and isinstance(getattr(tokenizer, "lang_code_to_id"), dict):
        tid = tokenizer.lang_code_to_id.get(nllb_target)
        if tid is not None:
            return tid
    if hasattr(tokenizer, "convert_tokens_to_ids"):
        tid = tokenizer.convert_tokens_to_ids(nllb_target)
        if isinstance(tid, int) and tid > 0:
            return tid
    if hasattr(tokenizer, "vocab") and isinstance(getattr(tokenizer, "vocab"), dict):
        tid = tokenizer.vocab.get(nllb_target)
        if isinstance(tid, int) and tid > 0:
            return tid
    return None

# --- Translation Function ---
def translate_text_nllb(
    text: str,
    source_lang: str,
    target_lang: str,
    model: AutoModelForSeq2SeqLM,
    tokenizer: AutoTokenizer,
    device: str,
    max_length: int = 100,
) -> str:
    """Translate text using the provided NLLB model and tokenizer.

    Raises ValueError for unsupported language codes; unexpected errors are returned as a
    user-friendly bracketed message.
    """
    try:
        # Quick exit for empty/whitespace input
        if not text or not text.strip():
            return ""

        # Normalize language inputs and resolve to NLLB tags
        raw_source = source_lang or ""
        raw_target = target_lang or ""
        norm_source = _normalize_lang_input(raw_source)
        norm_target = _normalize_lang_input(raw_target)

        nllb_source = _resolve_nllb_code(norm_source)
        nllb_target = _resolve_nllb_code(norm_target)

        if not nllb_source or not nllb_target:
            # Let caller map this to HTTP 400; include diagnostics
            print(
                f"Unsupported language(s): src='{raw_source}' -> '{nllb_source}', "
                f"tgt='{raw_target}' -> '{nllb_target}'"
            )
            raise ValueError(f"Language code '{raw_source}' or '{raw_target}' not supported")

        tokenizer.src_lang = nllb_source
        inputs = tokenizer(text, return_tensors="pt").to(device)

        # Compute target language token id robustly across tokenizer variants
        target_lang_id = _get_target_lang_token_id(tokenizer, nllb_target)
        if target_lang_id is None:
            raise ValueError(f"Target language token not found for '{nllb_target}'")

        # Run generation under no-grad for speed/memory
        with torch.inference_mode():
            translated_tokens = model.generate(
                **inputs,
                forced_bos_token_id=target_lang_id,
                max_length=max_length,
            )

        translated_text = tokenizer.batch_decode(
            translated_tokens, skip_special_tokens=True
        )[0]
        return translated_text

    except ValueError:
        # Re-raise to allow the FastAPI layer to return 400
        raise
    except Exception as e:
        print(f"An error occurred during NLLB translation: {e}")
        return f"[Translation Error: {e}]"