

   
# def create_search_prompt(user_query: str) -> str:
#     prompt = f"""
#     "{user_query}" 
#     (site:walmart.com OR site:bestbuy.com OR site:amazon.com)
#     (inurl:product OR inurl:dp OR inurl:ip OR inurl:item)
#     ("current price" OR "price" OR "buy now")
#     in stock
#     -("discontinued" OR "out of stock" OR "not available")
#     """
#     return prompt




def create_summary_prompt(results) -> str:  # Renamed to match usage
    system_prompt = """You are a smart shopping assistant helping users make quick decisions.
            Analyze the product comparison data and create a concise summary that:
            1. Identifies the absolute best deal (considering price, retailer reliability)
            2. Highlights any significant price differences worth noting
            3. Mentions immediate availability
            4. Adds any time-sensitive information (like sales/deals)

            Keep the tone conversational and direct. Format should be brief but informative."""
            
    user_prompt = f"""Based on this comparison data:
        {results}

        Create a quick summary focusing on:
        - Best deal: [Price + Retailer]
        - Price range: [Lowest to Highest]
        - Quick recommendation
        - Any special notes (deals/availability)

        Keep it under 3-4 sentences total."""
        
    return system_prompt, user_prompt


def create_compare_prompt(search_results:list[str]) -> str:
    system_prompt = """You are a product comparison expert. Act as a precise product data extractor that returns clean JSON data.
    DO NOT add any explanation or markdown formatting."""

    user_prompt = f"""Based on these product search results with images:
    {search_results}
    
    Return ONLY a JSON object exactly matching this structure:
    {{
        "products": [
            {{
                "title": "Full Product Name",
                "image": "Use actual product image URL from search_results, NO placeholder",
                "rating": 5,
                "retailers": [
                    {{
                        "name": "Walmart",
                        "price": "price in XX.XX format",
                        "availability": true if found in results
                    }},
                    {{
                        "name": "Best Buy",
                        "price": "price in XX.XX format",
                        "availability": true if found in results
                    }},
                    {{
                        "name": "Amazon",
                        "price": "price in XX.XX format",
                        "availability": true if found in results
                    }}
                ]
            }}
        ]
    }}

    IMPORTANT:
    - Extract and use actual product images from the search_results
    - NO placeholder images unless absolutely no image found
    - Return raw JSON only, no code blocks or markdown
    - Always include all three retailers
    - Use consistent price format XX,XX
    """
    return system_prompt, user_prompt
  