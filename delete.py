import os
import spacy
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_community.tools import DuckDuckGoSearchRun
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from typing_extensions import TypedDict

# Load environment variables
load_dotenv()

def Address_print_agent(place):
    """Finds the full address of a given place using DuckDuckGo and spaCy."""

    # Load spaCy NLP model
    nlp = spacy.load("en_core_web_lg")

    # IBM WatsonX credentials
    credentials = Credentials(
        url=os.getenv('Pay_url_Watsonx'),  
        api_key=os.getenv('Pay_API_KEY_Watsonx')
    )

    # Model configuration
    model_id = "ibm/granite-3-8b-instruct"
    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 100,
        "repetition_penalty": 1
    }

    # Initialize WatsonX ModelInference
    llm = ModelInference(
        model_id=model_id,
        params=parameters,
        credentials=credentials,
        project_id=os.getenv('Pay_PROJECT_ID_Watsonx'),  
        space_id=os.getenv('space_id')  
    )

    # Define the state schema
    class State(TypedDict):
        query: str  # User's query
        retrieved_context: str  # Address
        answer: str  # Final answer

    def extract_address(response):
        """Extracts address using spaCy NLP."""
        print("🛠 Processing Response:", response)  # Debugging output

        doc = nlp(response)

        # Extract address-related entities
        possible_addresses = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "FACILITY", "ORG"]]

        if possible_addresses:
            address = possible_addresses[0]  # Take the first found
        else:
            address = "Address Not Found"

        return {
            "retrieved_context": f"Address: {address}",
            "answer": f"Address: {address}"
        }

    def search_duckduckgo(state):
        """Fetches address using DuckDuckGo search."""
        # print(f"🔍 Searching DuckDuckGo for: {state['query']}")  
        
        search = DuckDuckGoSearchRun()
        query = f"{state['query']} full address"
        response = search.invoke(query)

        # print("🛠 RAW RESPONSE:", response)  # Debugging output

        # Handle different response types
        if isinstance(response, list) and response:
            return extract_address(response[0])
        elif isinstance(response, str) and response.strip():
            return extract_address(response)
        else:
            return {"retrieved_context": "Address: Not Found"}

    def generate_answer(state):
        """Generates a final answer based on extracted address."""
        return {"answer": state.get("retrieved_context", "Address: Not Found")}

    # Build LangGraph
    builder = StateGraph(State)

    # Add nodes
    builder.add_node("search_duckduckgo", search_duckduckgo)
    builder.add_node("generate_answer", generate_answer)

    # Define workflow connections
    builder.set_entry_point("search_duckduckgo")
    builder.add_edge("search_duckduckgo", "generate_answer")
    builder.add_edge("generate_answer", END)

    # Compile the graph
    graph = builder.compile()

    # Example input execution
    result = graph.invoke({"query": place})
    print("🔍 Final Output:", result)

# Example Run
Address_print_agent("Centauria City Hotel")
