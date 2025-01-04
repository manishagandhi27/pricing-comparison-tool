from utils.helper import get_english_product_name
from .prompts import ( create_compare_prompt, create_summary_prompt)
from langchain_core.messages import (SystemMessage, HumanMessage)
from config.settings import model, tavily, logger
from .graph_state import AgentState
import logging


def start_node(state: AgentState):
    print(f"start node")
    state["aggregator"] = [{"start_msg": "started"}]
    return state


def get_value_comprehension(state, key):
    results = [value for k, value in state["aggregator"] if k == key]
    if not results:
        raise KeyError(f"Key '{key}' not found in aggregator.")
    print("resuklt", results[0])
    return results[0]  # Return the first occurrence

def get_results(data, key):
    for entry in data:
        if key in entry:
            return entry[key]
    return None


# Example node implementation
def coordinate_node(state: AgentState) -> AgentState:
    """Coordinate and combine results"""
    print("inside crodinaror")
    print(f"aggregator {state["aggregator"]}")
    # Only combine results if all are available
    # if all(len(state[f"{r}_results"]) > 0 for r in ["amazon", "bestbuy", "walmart"]):
    all_results = []
    # for retailer in ["amazon", "bestbuy", "walmart"]:
        # result = get_results(state, f"{retailer}_results")
    amazon_results = state["aggregator"][2]["amazon_results"]
    all_results.extend(amazon_results)
    bb_results = state["aggregator"][3]["bestbuy_results"]
    all_results.extend(bb_results)
    wal_results = state["aggregator"][4]["walmart_results"]
    all_results.extend(wal_results)
   
    return {"aggregator": [{"compare_results": all_results}]}
    
    

def compare_node(state:AgentState):
    logger.info("inside compare")
    print("inside comapre")
    # top_result = state["top_results"]
    
    system_prompt, user_prompt = create_compare_prompt(state["aggregator"][5]["compare_results"])
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    try:
        response = model.invoke(messages)
        
        # Try to parse as JSON directly first
        import json
        try:
            parsed_response = json.loads(response.content)
            logger.info(f"parsed_response {parsed_response}")
        except json.JSONDecodeError:
            # If direct parsing fails, clean up the response
            logger.info(f"error in comaprsion {e}")
            content = response.content
            content = content.strip()
            if content.startswith('```'):
                content = '\n'.join(content.split('\n')[1:-1])
            parsed_response = json.loads(content)
            
        # state["comparison_results"] = parsed_response
        
    except Exception as e:
       # print(f"comparison error {e}")
        logger.error(f"Error {e}")
        # state["comparison_results"] = {
        #     "products": [...]  # your fallback structure
        # }
    # return {
    #     **state,
    #     #"comparison_result": comparison,
    #     "next_steps": ["process_llm"]
    # }
    return {"aggregator": [{"top_result": parsed_response}]}


def summarize_node(state:AgentState):
    logger.info("inside summary")
    print("inside crodinaror")
    results = state["aggregator"][6]["top_result"]
    system_prompt, user_prompt = create_summary_prompt(results)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    try:
        response = model.invoke(messages)
        logger.info(f"summary agent reponse from llm {response}")
    except Exception as e:
        #  print(f"summary error {e}")
         logger.error(f"Error {e}")
 
    # state["summary"] = response.content
    # return {
    #     **state,
    #     #"summary": summary,
    #     "next_steps": ["end"]
    # }
    return {"aggregator": [{"summary": response.content}]}