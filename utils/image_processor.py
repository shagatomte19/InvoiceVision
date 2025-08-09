"""
Image processing utilities for invoice OCR
"""
import streamlit as st
import base64
import io
from PIL import Image
from typing import Optional, Dict, Any
from api.openrouter_client import OpenRouterClient, create_extraction_prompt
from utils.data_parser import parse_extraction_result

def encode_image_to_base64(image: Image.Image) -> str:
    """
    Convert PIL Image to base64 string
    
    Args:
        image: PIL Image object
        
    Returns:
        Base64 encoded string
    """
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def process_uploaded_file(uploaded_file, config: Dict[str, Any]) -> None:
    """
    Process uploaded file and extract invoice data
    
    Args:
        uploaded_file: Streamlit uploaded file object
        config: Configuration dictionary
    """
    st.markdown("### 🖼️ Uploaded Invoice")
    
    if uploaded_file.type.startswith('image'):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Invoice", use_container_width=True)
        
        # Process button
        if st.button("🚀 Extract Data", type="primary"):
            if not config.get('api_key'):
                st.error("Please provide your OpenRouter API key in the sidebar")
                return
            
            # Convert image to base64
            image_base64 = encode_image_to_base64(image)
            
            # Create extraction options
            extraction_options = {
                key: config.get(key, False) 
                for key in ['extract_vendor', 'extract_dates', 'extract_totals', 'extract_items']
            }
            
            # Create extraction prompt
            prompt = create_extraction_prompt(extraction_options)
            
            # Initialize API client
            client = OpenRouterClient(
                api_key=config['api_key'],
                endpoint=config['api_endpoint'],
                site_url=config.get('site_url', ''),
                site_name=config.get('site_name', '')
            )
            
            # Call API
            api_response = client.extract_invoice_data(
                image_base64=image_base64,
                prompt=prompt,
                model=config['model_name'],
                temperature=config['temperature'],
                max_tokens=config['max_tokens']
            )
            
            if api_response:
                # Parse results
                extracted_data = parse_extraction_result(api_response)
                
                if extracted_data:
                    # Store in session state
                    st.session_state.extracted_data = extracted_data
                    st.session_state.processing_complete = True
                    
                    st.markdown("""
                    <div class="success-container">
                        ✅ Invoice processed successfully!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Trigger rerun to show results
                    st.rerun()
                    
    elif uploaded_file.type == 'application/pdf':
        st.info("📝 PDF processing requires additional setup. Please use image files for now.")
        st.markdown("""
        **To process PDF files:**
        1. Convert PDF to images first
        2. Or implement PDF-to-image conversion using libraries like `pdf2image`
        """)
    else:
        st.error("Unsupported file type. Please upload PNG, JPG, or JPEG files.")