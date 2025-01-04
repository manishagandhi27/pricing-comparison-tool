from typing import TypedDict
from typing import Annotated, List, TypedDict, Dict
import operator

class Retailer(TypedDict):
    name: str 
    price: str 
    availability: bool

class ComparedProducts(TypedDict):
    title: str
    image: str
    rating : str 
    retailers: list[Retailer]

class Product(TypedDict):
    title : str
    url : str
    image: str
    content: str
    

class AgentState(TypedDict):
    # comparison_results: Annotated[List[dict], "merge"]
    # top_results: Annotated[list, operator.add]
    # amazon_results : Annotated[list, operator.add]
    # bestbuy_results : Annotated[list, operator.add]
    # walmart_results : Annotated[list, operator.add]
    # tasks:  Annotated[list, operator.add]  # Changed from 'task: str' to 'tasks: List[str]'
    # summary :  Annotated[list, operator.add]
    # next_steps=[]
    # aggregator: Annotated[list[tuple[str, list]], operator.add]
    aggregator: Annotated[List[Dict[str, List]], operator.add]
    query: str
    
    
    
