import re
import json
from datetime import datetime

def load_orders():
    """Load mock orders from JSON file"""
    with open('data/mock_orders.json', 'r') as f:
        return json.load(f)

def extract_order_id(message):
    """
    Extract order ID from customer message.
    Supports formats: AX-771-3344, #AX-771-3344, AX 771 3344
    """
    # Pattern 1: Standard format with hyphens
    pattern1 = r'#?([A-Z]{2}-\d{3}-\d{4})'
    match = re.search(pattern1, message.upper())
    if match:
        return match.group(1)

    # Pattern 2: Format with spaces (normalize to hyphens)
    pattern2 = r'#?([A-Z]{2})\s+(\d{3})\s+(\d{4})'
    match = re.search(pattern2, message.upper())
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"

    # Pattern 3: No separators (assume format AXXXXXXXXX)
    pattern3 = r'#?([A-Z]{2})(\d{3})(\d{4})'
    match = re.search(pattern3, message.upper())
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"

    return None

def validate_order(order_id):
    """
    Validate order ID exists in system.
    Returns: order dict if found, None otherwise
    """
    orders = load_orders()
    for order in orders:
        if order['order_id'] == order_id:
            return order
    return None

def check_customer_match(order, customer_phone=None):
    """
    Verify customer phone matches order (security check).
    Returns: True if match or no phone provided, False otherwise
    """
    if not customer_phone:
        return True  # Skip validation if no phone provided (for demo)

    return order['customer_phone'] == customer_phone
