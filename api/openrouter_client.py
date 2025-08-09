"""
OpenRouter API client for invoice OCR processing using Qwen 2.5 VL
"""
import streamlit as st
from openai import OpenAI
from typing import Dict, Optional, Any

class OpenRouterClient:
    """Client for interacting with OpenRouter API using Qwen 2.5 VL"""
    
    def __init__(self, api_key: str, endpoint: str, site_url: str = "", site_name: str = ""):
        self.api_key = api_key
        self.endpoint = endpoint
        self.site_url = site_url
        self.site_name = site_name
        
        # Initialize OpenAI client with OpenRouter configuration
        self.client = OpenAI(
            base_url=endpoint,
            api_key=api_key
        )
    
    def extract_invoice_data(
        self, 
        image_base64: str, 
        prompt: str, 
        model: str, 
        temperature: float, 
        max_tokens: int
    ) -> Optional[Dict[str, Any]]:
        """
        Extract invoice data using Qwen 2.5 VL via OpenRouter
        
        Args:
            image_base64: Base64 encoded image
            prompt: Extraction prompt
            model: Model name
            temperature: Temperature parameter
            max_tokens: Maximum tokens
            
        Returns:
            API response or None if error
        """
        # Prepare extra headers for OpenRouter
        extra_headers = {}
        if self.site_url:
            extra_headers["HTTP-Referer"] = self.site_url
        if self.site_name:
            extra_headers["X-Title"] = self.site_name
        
        try:
            with st.spinner("🤖 Processing with Qwen 2.5 VL via OpenRouter..."):
                completion = self.client.chat.completions.create(
                    extra_headers=extra_headers,
                    extra_body={},
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{image_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                # Convert to format expected by existing code
                return {
                    "choices": [
                        {
                            "message": {
                                "content": completion.choices[0].message.content
                            }
                        }
                    ]
                }
                
        except Exception as e:
            st.error(f"OpenRouter API Error: {str(e)}")
            return None

def create_extraction_prompt(extraction_options: Dict[str, bool]) -> str:
    """
    Create a detailed prompt for invoice data extraction
    
    Args:
        extraction_options: Dictionary of extraction flags
        
    Returns:
        Formatted extraction prompt
    """
    from config.settings import EXTRACTION_FIELDS
    
    fields_to_extract = []
    for field_key, extract_flag in extraction_options.items():
        if extract_flag and field_key in EXTRACTION_FIELDS:
            fields_to_extract.append(EXTRACTION_FIELDS[field_key]['description'])
    
    prompt = f"""
    Please analyze this invoice image and extract the following information in a structured JSON format:
    
    Extract: {', '.join(fields_to_extract)}
    
    Return the data in this exact JSON structure:
    {{
        "invoice_number": "",
        "invoice_date": "",
        "due_date": "",
        "vendor": {{
            "name": "",
            "address": "",
            "phone": "",
            "email": ""
        }},
        "billing_to": {{
            "name": "",
            "address": ""
        }},
        "line_items": [
            {{
                "description": "",
                "quantity": "",
                "unit_price": "",
                "total": ""
            }}
        ],
        "subtotal": "",
        "tax_amount": "",
        "tax_rate": "",
        "total_amount": "",
        "currency": ""
    }}
    
    Important instructions:
    - If any field is not found, leave it as an empty string
    - Be precise with numerical values and maintain proper formatting
    - Only extract the fields that were specifically requested above
    - Return only the JSON object, no additional text or formatting
    - Ensure all currency amounts are in decimal format (e.g., "123.45")
    - For dates, use a consistent format (e.g., "MM/DD/YYYY" or "YYYY-MM-DD")
    """
    return prompt