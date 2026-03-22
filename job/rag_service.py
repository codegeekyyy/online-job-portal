import os
import io
import json
import re
import pdfplumber
import numpy as np
from langchain_huggingface import HuggingFaceEndpointEmbeddings
import faiss

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage



GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY", "")
MODEL_NAME = "llama-3.1-8b-instant"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 400          # characters per chunk
CHUNK_OVERLAP = 80        # overlap between chunks
TOP_K_CHUNKS = 6          # number of resume chunks to retrieve



_embedding_model = None  # lazy-load so server startup stays fast

def _get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEndpointEmbeddings(
            huggingfacehub_api_token=HUGGINGFACE_API_KEY, 
            model=EMBEDDING_MODEL
        )
    return _embedding_model


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract full text from a PDF file given as raw bytes."""
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += chunk_size - overlap
    return chunks


def build_faiss_index(chunks, model):
    """Embed chunks and build a FAISS flat-L2 index."""
    # HuggingFaceInferenceAPIEmbeddings returns a list of lists
    emb_list = model.embed_documents(chunks)
    embeddings = np.array(emb_list).astype(np.float32)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index, embeddings


def retrieve_top_chunks(query: str, chunks, index, model, top_k: int = TOP_K_CHUNKS):
    """Retrieve the most semantically similar resume chunks for a given query."""
    query_emb = model.embed_query(query)
    query_embedding = np.array([query_emb]).astype(np.float32)
    distances, indices = index.search(query_embedding, min(top_k, len(chunks)))
    return [chunks[i] for i in indices[0] if i < len(chunks)]




MATCH_PROMPT = """You are an expert AI career advisor. Analyze the candidate's resume against the job description below and return a structured JSON response.

Job Description:
{job_description}

Relevant Resume Sections:
{resume_chunks}

Return ONLY a valid JSON object (no markdown, no explanation, no code block) with exactly these keys:
{{
  "match_score": <integer 0-100>,
  "matching_skills": [<list of matched skill strings>],
  "missing_skills": [<list of missing skill strings>],
  "strengths": "<short paragraph about candidate strengths>",
  "recommendation": "<one of: Good Fit | Moderate Fit | Low Fit>",
  "explanation": "<2-3 sentence explanation of the overall assessment>"
}}"""




def run_job_match(resume_bytes: bytes, job_description: str) -> dict:
    """
    Full RAG pipeline:
    1. Extract text from resume PDF
    2. Chunk resume text
    3. Build FAISS vector index
    4. Retrieve top-k chunks relevant to JD
    5. Call Groq LLM with a structured prompt
    6. Return parsed JSON result
    """
    if not GROQ_API_KEY:
        return {"error": "GROQ_API_KEY not configured"}

    # Step 1 – Extract text
    try:
        resume_text = extract_text_from_pdf(resume_bytes)
    except Exception as e:
        return {"error": f"Failed to read PDF: {str(e)}"}

    if not resume_text.strip():
        return {"error": "Could not extract text from the uploaded PDF. Please ensure it is not scanned/image-only."}

    # Step 2 & 3 – Chunk and index
    model = _get_embedding_model()
    chunks = chunk_text(resume_text)
    if not chunks:
        return {"error": "Resume appears to be empty."}

    index, _ = build_faiss_index(chunks, model)

    # Step 4 – Retrieve relevant resume sections
    top_chunks = retrieve_top_chunks(job_description, chunks, index, model)
    resume_context = "\n\n---\n\n".join(top_chunks)

    # Step 5 – LLM call
    prompt = MATCH_PROMPT.format(
        job_description=job_description,
        resume_chunks=resume_context,
    )

    try:
        llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=MODEL_NAME,
            temperature=0.2,
        )
        response = llm.invoke([HumanMessage(content=prompt)])
        raw = response.content.strip()
    except Exception as e:
        return {"error": f"Groq API call failed: {str(e)}"}

    # Step 6 – Parse JSON
    try:
        # Strip any accidental markdown fences
        raw = re.sub(r"^```[a-z]*\n?", "", raw, flags=re.MULTILINE)
        raw = re.sub(r"```$", "", raw, flags=re.MULTILINE).strip()
        result = json.loads(raw)
    except Exception:
        # Return raw text as explanation if JSON parse fails
        result = {
            "match_score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "strengths": "",
            "recommendation": "Unable to parse",
            "explanation": raw,
        }

    return result
