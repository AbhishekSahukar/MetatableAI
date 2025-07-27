from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda

from tools.pdf_loader import extract_text_from_pdf
from tools.llm_extractor import extract_parameters_from_text

class GraphState(dict):
    pdf_path: str
    extracted_text: str
    extracted_params: list

# Step 1: Extract text from PDF
def step_extract_text(state: GraphState) -> GraphState:
    text = extract_text_from_pdf(state["pdf_path"])
    return {**state, "extracted_text": text}

# Step 2: Extract parameter-value pairs using LLM
def step_extract_parameters(state: GraphState) -> GraphState:
    extracted = extract_parameters_from_text(state["extracted_text"])
    return {**state, "extracted_params": extracted}

def build_metatable_graph():
    builder = StateGraph(GraphState)
    builder.add_node("extract_text", RunnableLambda(step_extract_text))
    builder.add_node("llm_extract", RunnableLambda(step_extract_parameters))

    builder.set_entry_point("extract_text")
    builder.add_edge("extract_text", "llm_extract")
    builder.set_finish_point("llm_extract")

    # ✅ No checkpointer used for simplicity
    return builder.compile()