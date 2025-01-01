from  graph.graph_builder import run_graph

def main():
    
    user_input = input("Enter the product you are looking for: ").strip()
    if not user_input:
        print("Please enter valid product name")
        return
    
    try:
        result = run_graph(user_input)
        
        # Display Top Results
        # if result["top_results"]:
        #     print("\nTop Results:")
        #     for idx, product in enumerate(result["top_results"], start=1):
        #         print(f"\nResult {idx}:")
        #         print(f"Title   : {product['title']}")
        #         print(f"URL     : {product['url']}")
        #         print(f"Image   : {product['image']}")
        #         print(f"Content : {product['content']}")
        
        # else:
        #     print("No top results found.")
        
        # Display Summary
        # if result["summary"]:
        #     print("\nSummary:")
        #     print(result["summary"])
        # else:
        #     print("No summary available.")
    
    except Exception as e:
    
        print("An error occurred while processing your request.")



if __name__ == "__main__":
    main()
    