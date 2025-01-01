
from langgraph.graph import StateGraph, END
from .graph_state import AgentState
from .nodes import (start_node, compare_node, summarize_node,coordinate_node)
from .retailers.amazon import amazon_node
from .retailers.bestbuy import bestbuy_node
from .retailers.walmart import walmart_node
from IPython.display import Image, display
from typing import Annotated, List, TypedDict


def route_to_retailers(state: AgentState) -> List[str]:
        # Only route to retailers that haven't processed yet
        next_steps = []
        if not state["amazon_results"]:
            next_steps.append("amazon")
        if not state["bestbuy_results"]:
            next_steps.append("bestbuy")
        if not state["walmart_results"]:
            next_steps.append("walmart")
        return next_steps
    
    
    
def build_graph() -> StateGraph:
    """
    Builds and compiles the state graph for the AI agent.

    Returns:
        StateGraph: The compiled state graph.
    """
    builder = StateGraph(AgentState)
    builder.add_node("start", start_node)
    
    builder.add_node("amazon",  amazon_node)
    builder.add_node("bestbuy", bestbuy_node)
    builder.add_node("walmart", walmart_node)
    builder.add_node("coordinator", coordinate_node)
    builder.add_node("compare", compare_node)
    builder.add_node("summarize", summarize_node)
    
    builder.set_entry_point("start")
    
    # Define parallel execution paths
   # Add conditional edges from start to retailers
    # builder.add_conditional_edges(
    #     "start",
    #     route_to_retailers
    # )
    
    
    builder.add_edge("start", "amazon")
    builder.add_edge("start", "bestbuy")
    builder.add_edge("start", "walmart")
    
    # Connect to coordinator
    builder.add_edge("amazon", "coordinator")
    builder.add_edge("bestbuy", "coordinator")
    builder.add_edge("walmart", "coordinator")
    
    # builder.add_conditional_edges(
    #     "coordinator",
    #     lambda x: x["next_steps"][0],
    #     {
    #         "compare": "compare",
    #         "wait": "coordinator"
    #     }
    # )
    
    builder.add_edge("coordinator", "compare")

    builder.add_edge("compare", "summarize")
    #builder.add_edge("summarize", END)
    # builder.add_node("end", lambda x: x)
    
    # Add edge to end
    builder.add_edge("summarize", END)
    return builder.compile()



compiled_graph = build_graph()
# display(Image(compiled_graph.get_graph().draw_mermaid_png()))


    
def run_graph(user_input: str) -> AgentState:
    initial_state = AgentState(
       # comparison_results=[],
        # top_results=[],          # Initialize as empty list
        # amazon_results=[],      # Initialize as empty lists
        # bestbuy_results=[],
        # walmart_results=[],
        # tasks=[user_input],     # Initialize 'tasks' as a list with the user input
        # summary=[],
        # next_steps=["start"]
        aggregator=[]
    )
    # ... your graph invocation logic ...
    final_state = compiled_graph.invoke(initial_state)
    return final_state