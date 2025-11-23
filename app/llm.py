from transformers import pipeline

# --- LLM pipeline ---
llm = pipeline("text-generation", model="google/flan-t5-small")

def generate_response(info):
    """
    Generate a human-readable answer using the LLM.
    """
    prompt = f"Answer the user's question based on this info: {info}"
    return llm(prompt, max_length=50)[0]['generated_text']
