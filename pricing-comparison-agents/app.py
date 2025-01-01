import streamlit as st
import streamlit.components.v1 as components
from graph.graph_builder import run_graph

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .search-container {
        padding: 1rem;
        text-align: center;
    }
    .product-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 1.25rem;
        padding: 1rem;
        align-items: stretch;
    }

    .product-card {
        flex: 0 1 300px;
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .retailer-section {
        margin-top: auto;
        padding-top: 0.75rem;
        border-top: 1px solid #e5e7eb;
    }
    
    
    # .retailer-row {
    #     background: #f8f9fa;
    #     padding: 0.75rem;
    #     margin: 0.5rem 0;
    #     border-radius: 0.5rem;
    # }
    

    # .product-card {
    #     background: white;
    #     border: 1px solid #e5e7eb;
    #     border-radius: 0.5rem;
    #     padding: 1rem;
    #     box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    #     transition: all 0.2s ease;
    #     height: 100%;
    #     display: flex;
    #     flex-direction: column;
    # }

    .product-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transform: translateY(-1px);
    }

    .product-image {
        width: 100%;
        height: 200px;
        object-fit: contain;
        margin-bottom: 0.75rem;
    }

    .product-title {
        font-size: 1rem;
        line-height: 1.4;
        font-weight: 500;
        margin-bottom: 0.75rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    # .retailer-section {
    #     margin-top: auto;
    #     padding: 0.75rem 0 0;
    #     border-top: 1px solid #e5e7eb;
    # }

    .retailer-row {
            display: flex;
            align-items: center;
            padding: 0.5rem;
            margin: 0.25rem 0;
            background: #f9fafb;
            border-radius: 0.25rem;
    }

    .retailer-name {
        flex: 2;
    }

    .retailer-price {
        flex: 1;
        font-weight: 500;
    }

    .retailer-availability {
        flex: 0 0 auto;
        width: 24px;
        text-align: center;
    }
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

if "show_results" not in st.session_state:
    st.session_state["show_results"] = False

if not st.session_state["show_results"]:
    st.title("Search Smarter, Shop Better")
    user_query = st.text_input("", placeholder="Search for any product...", key="search_input")
    
    if st.button("Compare Prices", type="primary", use_container_width=False):
        if user_query:
            with st.spinner("Searching across retailers..."):
                graph_results = run_graph(user_query)
                st.session_state.comparison_results = graph_results.get("comparison_results", [])
                st.session_state.show_results = True
                st.rerun()
        else:
            st.warning("Please enter a product name.")

else:
    if st.button("← New Search"):
        st.session_state.show_results = False
        st.rerun()
    
    if "comparison_results" in st.session_state:
        comparison_data = st.session_state.comparison_results
        
       # In your layout code
        num_columns = 3
        for i in range(0, len(comparison_data.get("products", [])), num_columns):
            cols = st.columns(num_columns)
            for j, col in enumerate(cols):
                if i + j < len(comparison_data.get("products", [])):
                    product = comparison_data["products"][i + j]
                    with col:
                        with st.container():
                            st.image(product["image"], width=200)
                            st.markdown(f"**{product['title'][:60]}...**" if len(product['title']) > 60 else f"**{product['title']}**")
                            st.write("⭐" * int(product["rating"]))
                            for retailer in product["retailers"]:
                                st.markdown(f"""
                                    <div class='retailer-row'>
                                        <span style='flex:2'>{retailer['name']}</span>
                                        <span style='flex:1'>${retailer['price']}</span>
                                        <span>{'✅' if retailer['availability'] else '❌'}</span>
                                    </div>
                                """, unsafe_allow_html=True)