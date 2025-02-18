import re
from transformers import pipeline
from .database import cocktail_db, memory_db

# Load the generative model (using a free Hugging Face model)
generator = pipeline("text-generation", model="distilgpt2")


def detect_memory_update(query: str):
    """
    Check if the query contains user preference updates.
    Example: "My favorite ingredients: rum, lime, mint"
    """
    pattern = re.compile(r"my favorite (ingredients|cocktails):\s*(.+)", re.IGNORECASE)
    match = pattern.search(query)
    if match:
        pref_type = match.group(1).lower()
        items = [item.strip() for item in match.group(2).split(",")]
        return pref_type, items
    return None, None


def build_prompt(query: str, cocktails: list, memories: list = None):
    prompt = (
        "You are a friendly cocktail advisor. Provide a concise, natural, and clear answer without listing raw details. "
        f"Query: {query}\n"
    )
    if cocktails:
        # Extract the names from the cocktail dictionaries
        names = ", ".join([c.get("name", "Unknown") for c in cocktails])
        prompt += f"Matching Cocktails: {names}.\n"
    prompt += "Based on the above, offer a friendly recommendation or answer."
    return prompt




def get_response(query: str) -> str:
    """
    Main function to obtain a response.
    If the query includes user preference updates, save them.
    Then perform a search in the cocktail database and generate a response.
    """
    # Check for preference update in the query
    pref_type, items = detect_memory_update(query)
    memory_response = ""
    if items:
        for item in items:
            memory_db.add_memory(item)
        memory_response = f"Thanks, I've updated your favorite {pref_type}.\n\n"

    # Search for relevant cocktails in the database
    cocktail_results = cocktail_db.search(query, k=5)
    # Optionally, include user memories if relevant
    memory_results = memory_db.search("ingredients")

    # Build the prompt for the LLM
    prompt = build_prompt(query, cocktail_results, memory_results)

    # Generate a response using max_new_tokens to control the output length
    generated = generator(prompt, max_new_tokens=50, temperature=0.7, num_return_sequences=1)
    answer = generated[0]['generated_text']

    # Combine the memory update message (if any) with the generated answer
    full_response = memory_response + answer.strip()
    return full_response
