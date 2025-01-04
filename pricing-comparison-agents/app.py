import streamlit as st
import streamlit.components.v1 as components
from graph.graph_builder import run_graph

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .product-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 0.75rem;
        margin: 0.5rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .product-grid {
        display: grid;
        gap: 1rem;
        padding: 0.5rem;
    }

    .retailer-row {
        display: flex;
        align-items: center;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 0.375rem;
        background: #f8fafc;
        transition: background-color 0.15s ease;
    }

    .retailer-row:hover {
        background: #f1f5f9;
        cursor: pointer;
    }

    .retailer-name {
        flex: 2;
        font-size: 0.875rem;
        color: #374151;
    }

    .retailer-price {
        flex: 1;
        font-size: 0.875rem;
        font-weight: 600;
        color: #1f2937;
        text-align: right;
        padding-right: 0.5rem;
    }

    .rating {
        color: #fbbf24;
        font-size: 0.75rem;
        margin: 0.25rem 0;
    }

    .product-title {
        font-size: 0.875rem;
        font-weight: 500;
        color: #111827;
        margin: 0.5rem 0;
        line-height: 1.25;
    }

    .image-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem;
        background: #f9fafb;
        border-radius: 0.375rem;
        margin-bottom: 0.5rem;
    }

    .availability-icon {
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .search-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(to right, #4f46e5, #3b82f6);
        color: white;
        margin-bottom: 2rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

if "show_results" not in st.session_state:
    st.session_state["show_results"] = False

if not st.session_state["show_results"]:
    st.markdown("""
        <div class="search-header">
            <h1>Search Smarter, Shop Better</h1>
        </div>
    """, unsafe_allow_html=True)
    
    user_query = st.text_input("", placeholder="Search for any product...", key="search_input")
    
    if st.button("Compare Prices", type="primary", use_container_width=False):
        if user_query:
            with st.spinner("Searching across retailers..."):
                graph_results = run_graph(user_query)
                st.session_state.comparison_results = graph_results.get("aggregator", [])[6]["top_result"]
                st.session_state.show_results = True
                st.rerun()
        else:
            st.warning("Please enter a product name.")

else:
    if st.button("← New Search", type="secondary"):
        st.session_state.show_results = False
        st.rerun()
    
    if "comparison_results" in st.session_state:
        comparison_data = st.session_state.comparison_results
        
        for i in range(0, len(comparison_data.get("products", [])), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(comparison_data.get("products", [])):
                    product = comparison_data["products"][i + j]
                    
                    # Safely get rating, default to 5 if not found
                    rating = 5
                    if "rating" in product and product["rating"]:
                        try:
                            rating = int(float(product["rating"]))
                        except:
                            rating = 5

                    with col:
                        st.markdown(f'''
                            <div style="display: flex; background: white; padding: 1rem; 
                                    border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
                                    margin: 0.5rem 0; gap: 1rem;">
                                <div style="flex: 1;">
                                    <img src="{product['image']}" style="width: 100%; max-height: 150px; 
                                        object-fit: contain; border-radius: 0.375rem;">
                                    <div style="color: #fbbf24; font-size: 0.75rem; margin-top: 0.5rem;">
                                        {"⭐" * rating}
                                    </div>
                                </div>
                                <div style="flex: 1.5;">
                                    <div style="font-weight: 500; margin-bottom: 0.75rem; 
                                            font-size: 0.875rem; color: #1a202c;">
                                        {product['title'][:50]}...
                                    </div>
                                    <div>
                                        {"".join([f"""
                                            <div style="display: flex; align-items: center; padding: 0.5rem;
                                                    margin: 0.25rem 0; background: #f8fafc; 
                                                    border-radius: 0.375rem; font-size: 0.75rem;">
                                                <span style="flex: 2; color: #4a5568;">{r['name']}</span>
                                                <span style="flex: 1; font-weight: 600; color: #1a202c; 
                                                    text-align: right; padding-right: 0.5rem;">
                                                    ${r['price']}
                                                </span>
                                                <span style="width: 20px; text-align: center;">
                                                    {'✅' if r['availability'] else '❌'}
                                                </span>
                                            </div>
                                        """ for r in product["retailers"]])}
                                    </div>
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)