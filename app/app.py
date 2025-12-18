"""
E-commerce Product Search with Streamlit.
Browse and search products using Azure AI Search.
"""

import sys
from pathlib import Path
import math
import streamlit as st
from typing import List, Dict, Any

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from services.azure_search_service import get_search_service
from config import Config

# Page configuration
st.set_page_config(
    page_title="이커머스 상품 검색",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services
@st.cache_resource
def get_services():
    return get_search_service()

search_service = get_services()

# Constants
PRODUCTS_PER_PAGE = 9  # 3 rows x 3 products
ALL_SEARCH_FIELDS = ["name", "brand", "description", "imageCaption", "imageDescription", "imageTags"]


# ============================================================================
# Initialization
# ============================================================================

def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'products' not in st.session_state:
        st.session_state.products = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1
    if 'is_search_mode' not in st.session_state:
        st.session_state.is_search_mode = False
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'sidebar_menu' not in st.session_state:
        st.session_state.sidebar_menu = "검색"


# ============================================================================
# Product Display Functions
# ============================================================================

def display_product_card(product: Dict[str, Any], show_score: bool = False):
    """Display a single product card"""
    with st.container(height=690, border=True):
        # Display image with fixed height
        if product.get('imageUrl'):
            st.image(product['imageUrl'], use_container_width=True)
            st.markdown(
                """
                <style>
                img {
                    height: 280px !important;
                    object-fit: cover !important;
                }
                hr {
                    margin-top: 0.5rem !important;
                    margin-bottom: 0.5rem !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
        else:
            st.image("https://via.placeholder.com/300x300?text=No+Image", use_container_width=True)
        
        # Product name
        st.markdown(f"**{product.get('name', 'N/A')}**")
        
        # Brand and price
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<span style='color: #666; font-size: 0.9rem;'>🏷️ {product.get('brand', 'N/A')}</span>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<span style='color: #666; font-size: 0.9rem;'>💰 {product.get('price', 0):,}원</span>", unsafe_allow_html=True)
        
        # Score if in search mode
        if show_score and product.get('score'):
            st.caption(f"⭐ 관련도: {product['score']:.4f}")
        
        # Description (fixed height container)
        desc_container = st.container()
        with desc_container:
            if product.get('description'):
                desc = product['description']
                if len(desc) > 80:
                    desc = desc[:80] + "..."
                st.markdown(f'<div style="height: 70px; overflow: hidden; margin-top: 8px;"><small>📝 {desc}</small></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="height: 70px; margin-top: 8px;"></div>', unsafe_allow_html=True)
        
        # Image Caption (fixed height container)
        caption_container = st.container()
        with caption_container:
            if product.get('imageCaption'):
                caption = product['imageCaption']
                if len(caption) > 50:
                    caption = caption[:50] + "..."
                st.markdown(f'<div style="height: 55px; overflow: hidden; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e0e0e0;"><small>💬 {caption}</small></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="height: 55px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e0e0e0;"></div>', unsafe_allow_html=True)
        
        # Image Tags (fixed height container)
        tags_container = st.container()
        with tags_container:
            if product.get('imageTags'):
                tags = product['imageTags']
                if isinstance(tags, list) and tags:
                    tags_str = " • ".join([f"#{tag}" for tag in tags])  # Show all tags
                    st.markdown(f'<div style="height: 70px; overflow: hidden; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e0e0e0;"><small>🏷️ {tags_str}</small></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="height: 70px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e0e0e0;"></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="height: 70px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #e0e0e0;"></div>', unsafe_allow_html=True)
        
        # Image Description (expander for detailed info)
        if product.get('imageDescription'):
            with st.expander("🔍 상세보기"):
                st.write(product['imageDescription'])


def display_products_grid(products: List[Dict[str, Any]], page: int, show_scores: bool = False):
    """Display products in a grid layout with pagination"""
    if not products:
        st.info("😔 표시할 상품이 없습니다.")
        return
    
    total_products = len(products)
    total_pages = math.ceil(total_products / PRODUCTS_PER_PAGE)
    
    # Ensure page is within bounds
    page = max(1, min(page, total_pages))
    
    # Get products for current page
    start_idx = (page - 1) * PRODUCTS_PER_PAGE
    end_idx = min(start_idx + PRODUCTS_PER_PAGE, total_products)
    page_products = products[start_idx:end_idx]
    
    # Display product count and page info
    st.markdown(f"### 📦 전체 {total_products}개 상품 | 📄 {page}/{total_pages} 페이지")
    st.divider()
    
    # Display products in 3 columns with equal spacing
    for i in range(0, len(page_products), 3):
        cols = st.columns(3, gap="medium")
        for j, col in enumerate(cols):
            if i + j < len(page_products):
                with col:
                    display_product_card(page_products[i + j], show_scores)
    
    # Pagination controls
    st.divider()
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    with col1:
        if st.button("◀️ 이전", disabled=(page <= 1), use_container_width=True):
            st.session_state.current_page = page - 1
            st.rerun()
    
    with col3:
        st.markdown(f"<h4 style='text-align: center;'>페이지 {page} / {total_pages}</h4>", unsafe_allow_html=True)
    
    with col5:
        if st.button("다음 ▶️", disabled=(page >= total_pages), use_container_width=True):
            st.session_state.current_page = page + 1
            st.rerun()


# ============================================================================
# Search Functions
# ============================================================================

def search_products(query: str, strategy: str, search_fields: List[str]) -> List[Dict[str, Any]]:
    """Search for products based on query and strategy"""
    try:
        # Prepare search_fields (None means all fields)
        fields_to_search = search_fields if search_fields else None
        
        # Perform search based on strategy
        if strategy == "keyword":
            results = search_service.keyword_search(query, search_fields=fields_to_search)
        elif strategy == "vector":
            results = search_service.vector_search(query, search_fields=fields_to_search)
        else:  # hybrid
            results = search_service.hybrid_search(query, search_fields=fields_to_search)
        
        return results
    except Exception as e:
        st.error(f"❌ 검색 중 오류가 발생했습니다: {str(e)}")
        return []


def load_all_products() -> List[Dict[str, Any]]:
    """Load all products from Azure AI Search"""
    try:
        return search_service.get_all_products(top_k=100)
    except Exception as e:
        st.error(f"❌ 상품을 불러오는 중 오류가 발생했습니다: {str(e)}")
        return []


# ============================================================================
# Main Application
# ============================================================================

def main():
    """Main application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar - Search Settings
    with st.sidebar:
        st.title("🛍️ 검색 설정")
        st.divider()
        
        # Search strategy
        strategy = st.selectbox(
            "검색 방식",
            ["keyword", "vector", "hybrid"],
            index=2,
            format_func=lambda x: {
                "keyword": "키워드 (전문 검색)",
                "vector": "벡터 (의미 기반)",
                "hybrid": "하이브리드 (키워드 + 벡터)"
            }[x]
        )
        
        # Search fields
        search_fields = st.multiselect(
            "검색 범위",
            ALL_SEARCH_FIELDS,
            default=ALL_SEARCH_FIELDS,
            format_func=lambda x: {
                "name": "상품명",
                "brand": "브랜드",
                "description": "설명",
                "imageCaption": "이미지 캡션",
                "imageDescription": "이미지 설명",
                "imageTags": "이미지 태그"
            }.get(x, x)
        )
        
        st.divider()
        
        # Search input
        search_query = st.text_input("🔍 검색어를 입력하세요", value=st.session_state.search_query)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("검색", type="primary", use_container_width=True):
                if search_query:
                    st.session_state.search_query = search_query
                    with st.spinner("검색 중..."):
                        results = search_products(search_query, strategy, search_fields)
                        if results:
                            st.session_state.products = results
                            st.session_state.is_search_mode = True
                            st.session_state.current_page = 1
                            st.success(f"✅ {len(results)}개 상품을 찾았습니다!")
                        else:
                            st.warning("😔 검색 결과가 없습니다.")
                else:
                    st.warning("검색어를 입력하세요.")
        
        with col2:
            if st.button("전체보기", use_container_width=True):
                st.session_state.search_query = ""
                with st.spinner("상품 불러오는 중..."):
                    all_products = load_all_products()
                    st.session_state.products = all_products
                    st.session_state.is_search_mode = False
                    st.session_state.current_page = 1
                    st.success(f"✅ {len(all_products)}개 상품을 불러왔습니다!")
        
        st.divider()
        st.caption("💡 Tips")
        st.caption("• 자연어로 검색 가능")
        st.caption("• 검색 방식 변경 가능")
        st.caption("• 검색 범위 선택 가능")
    
    # Main content
    st.title("🛍️ 이커머스 상품 검색")
    
    # Menu selection in main area with clear button
    menu = st.radio(
        "메뉴 선택",
        ["📦 상품 목록", "💬 챗봇"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # if menu == "💬 챗봇":
    #     if st.button("🗑️", key="clear_chat_top"):
    #         st.session_state.chat_messages = []
    #         st.rerun()
    
    # st.divider()
    
    # Product List View
    if menu == "📦 상품 목록":
        # Load products on first run
        if not st.session_state.products:
            with st.spinner("전체 상품을 불러오는 중..."):
                all_products = load_all_products()
                st.session_state.products = all_products
        
        # Display products
        if st.session_state.products:
            title_text = f"🔍 '{st.session_state.search_query}' 검색 결과" if st.session_state.is_search_mode else "전체 상품 목록"
            st.subheader(title_text)
            
            display_products_grid(
                st.session_state.products,
                st.session_state.current_page,
                show_scores=st.session_state.is_search_mode
            )
        else:
            st.info("상품이 없습니다. 전체보기를 클릭하여 상품을 불러오세요.")
    
    # Chatbot View
    else:
        # Display chat messages
        if not st.session_state.chat_messages:
            st.info("👋 안녕하세요! 상품에 대해 무엇이든 물어보세요.")
        else:
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    # Display product name at the top if available
                    if message["role"] == "assistant" and message.get("product"):
                        product = message["product"]
                        st.markdown(f"#### 추천 상품: {product.get('name', 'N/A')}")
                        st.divider()
                    
                    # Display message content
                    st.write(message["content"])
                    
                    # Add product detail expander if product info exists
                    if message["role"] == "assistant" and message.get("product"):
                        product = message["product"]
                        with st.expander("📦 상품 상세 정보 보기"):
                            # Display product image
                            if product.get('imageUrl'):
                                st.image(product['imageUrl'], use_container_width=True)
                            
                            # Product details
                            st.markdown(f"**상품명:** {product.get('name', 'N/A')}")
                            st.markdown(f"**브랜드:** {product.get('brand', 'N/A')}")
                            
                            price = product.get('price', 0)
                            price_str = f"{price:,}원" if price is not None else "가격 정보 없음"
                            st.markdown(f"**가격:** {price_str}")
                            
                            st.divider()
                            
                            st.markdown("**📝 상품 설명**")
                            st.write(product.get('description', 'N/A'))
                            
                            st.divider()
                            
                            if product.get('imageCaption'):
                                st.markdown("**💬 이미지 캡션**")
                                st.write(product.get('imageCaption'))
                            
                            if product.get('imageDescription'):
                                st.markdown("**🖼️ 이미지 상세 설명**")
                                st.write(product.get('imageDescription'))
                            
                            if product.get('imageTags'):
                                tags = product.get('imageTags', [])
                                if isinstance(tags, list) and tags:
                                    st.markdown("**🏷️ 태그**")
                                    tags_str = " • ".join([f"#{tag}" for tag in tags])
                                    st.write(tags_str)
                            
                            if product.get('score'):
                                st.divider()
                                st.caption(f"⭐ 검색 관련도: {product['score']:.4f}")
        
        # Placeholder for loading indicator
        loading_placeholder = st.empty()
        
        # Chat input area with clear button
        # col1, col2 = st.columns([11, 1])
        # with col2:
        #     if st.button("🗑️", help="대화 초기화", key="clear_chat"):
        #         st.session_state.chat_messages = []
        #         st.rerun()
        
        # with col1:
        prompt = st.chat_input("메시지를 입력하세요...")
        
        if prompt:
            # Add user message
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            
            # Generate assistant response with loading indicator above input
            with loading_placeholder:
                with st.spinner("상품 검색 중..."):
                    try:
                        from services.openai_service import get_openai_service
                        openai_service = get_openai_service()
                        
                        # Step 1: Search for products using user's message
                        search_results = search_products(prompt, "hybrid", ALL_SEARCH_FIELDS)
                        
                        if search_results and len(search_results) > 0:
                            # Get the top 1 product (highest score)
                            top_product = search_results[0]
                            
                            # Step 2: Create context with product information (handle None values)
                            price = top_product.get('price', 0)
                            price_str = f"{price:,}원" if price is not None else "가격 정보 없음"
                            
                            tags = top_product.get('imageTags', [])
                            tags_str = ', '.join(tags) if isinstance(tags, list) and tags else 'N/A'
                            
                            score = top_product.get('score', 0)
                            score_str = f"{score:.4f}" if score is not None else "N/A"
                            
                            product_context = f"""
[추천 상품 정보]
- 상품명: {top_product.get('name') or 'N/A'}
- 브랜드: {top_product.get('brand') or 'N/A'}
- 가격: {price_str}
- 설명: {top_product.get('description') or 'N/A'}
- 이미지 캡션: {top_product.get('imageCaption') or 'N/A'}
- 이미지 설명: {top_product.get('imageDescription') or 'N/A'}
- 태그: {tags_str}
- 관련도 점수: {score_str}
"""
                            
                            # Step 3: Create messages for LLM with RAG context
                            system_prompt = """당신은 친절한 이커머스 상품 추천 챗봇입니다. 
사용자의 질문에 따라 검색된 상품 정보를 바탕으로 자연스럽고 친절하게 상품을 추천하고 설명해주세요.
상품의 특징, 장점, 어울리는 상황 등을 포함하여 구체적으로 설명하되, 자연스러운 대화체를 유지하세요.
가격과 브랜드 정보도 함께 안내해주세요."""
                            
                            messages = [
                                {"role": "system", "content": system_prompt},
                                {"role": "system", "content": product_context}
                            ]
                            
                            # Add recent chat history (last 3 exchanges for context)
                            recent_messages = st.session_state.chat_messages[-7:] if len(st.session_state.chat_messages) > 7 else st.session_state.chat_messages
                            messages.extend(recent_messages)
                            
                            # Step 4: Get response from LLM
                            assistant_message = openai_service.chat_completion(messages)
                            
                            # Add assistant message with product info
                            st.session_state.chat_messages.append({
                                "role": "assistant", 
                                "content": assistant_message,
                                "product": top_product
                            })
                            
                        else:
                            # No products found
                            assistant_message = "죄송합니다. 요청하신 내용과 관련된 상품을 찾을 수 없습니다. 다른 키워드로 다시 질문해주시겠어요?"
                            
                            # Add assistant message without product info
                            st.session_state.chat_messages.append({
                                "role": "assistant", 
                                "content": assistant_message
                            })
                        
                    except Exception as e:
                        error_message = f"죄송합니다. 오류가 발생했습니다: {str(e)}"
                        st.session_state.chat_messages.append({
                            "role": "assistant", 
                            "content": error_message
                        })
                    
                    st.rerun()


if __name__ == "__main__":
    main()
