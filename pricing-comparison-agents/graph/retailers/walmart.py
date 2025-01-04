from utils.helper import get_english_product_name

from langchain_core.messages import (SystemMessage, HumanMessage)
from config.settings import model, tavily, logger
from graph.graph_state import AgentState



def create_search_prompt(user_query: str,domain:str) -> str:
    # prompt = f"""
    # "{user_query}" 
    # (site:WALMART.com)
    # (inurl:product OR inurl:dp OR inurl:ip OR inurl:item)
    # ("current price" OR "price" OR "buy now")
    # in stock
    # -("discontinued" OR "out of stock" OR "not available")
    # """
    prompt =  f"""
      Search for the product "{user_query}" exclusively on the website "{domain}". Provide a comprehensive summary that includes the following details sourced only from "{domain}":

    
    Ensure that all information is accurate and solely derived from "{domain}". Do not include data or references from any other websites or sources.

    """
    return prompt

def walmart_node(state: AgentState):
    print(f"walmart node")
    # query = state["tasks"][0]
    try:
        search_prompt = create_search_prompt(state["query"], "walmart.com")
        print(f"serch prmopot: {search_prompt}")
        # Add image search capability
        search_results =  tavily.search(
            query=search_prompt, 
            search_depth="basic", 
            max_results=3,
            include_domains=["walmart.com"],
            include_images=True # Enable image search
        )
        #logger.info(f"search_results : {search_results}")
        results = search_results.get('results', [])
        images = search_results.get('images', [])
        
        processed_results = []
        print(f"search_results: {search_results}")
        # Process each result and try to match with an image
        for idx, result in enumerate(results):
            # Try to get corresponding image if available
            image_url = images[idx] if idx < len(images) else "https://via.placeholder.com/300"
            
            processed_results.append({
                "title": get_english_product_name(result["title"]),
                "url": result["url"],
                "content": result["content"],
                "image": image_url
            })
            
       # logger.info("Processed results with images:", processed_results)
        #state["walmart_results"] = processed_results
        #state["aggregator"] = [{"walmart_results": processed_results}]
    except IndexError:
        # Handle case when idx is out of range for images list
        logger.error("No corresponding image found for a search result.")
        state["walmart_results"] = []
    except Exception as e:
        #print(f"search error {e}")
        logger.error(f"Error {e}")
        state["walmart_results"] = []
    # return {
    #     **state,
    #     "walmart_results": processed_results,
    #     "next_steps": ["check_coordinator"]
    # }
    return {"aggregator": [{"walmart_results": processed_results}]}
    #return state
