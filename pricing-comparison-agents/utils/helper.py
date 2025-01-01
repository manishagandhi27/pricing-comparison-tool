

def get_english_product_name(title):
    # Remove RTL characters and non-English text
    english_chars = ''.join(char for char in title if ord(char) < 128)
    
    # Clean up remaining text
    clean_title = english_chars.replace('Amazon.com:', '').strip()
    
    # Return first meaningful part or whole title if short
    parts = clean_title.split()
    return ' '.join(parts[:6]) if len(parts) > 6 else clean_title
  