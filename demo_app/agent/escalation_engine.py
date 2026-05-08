from datetime import datetime

def check_escalation_triggers(order, user_message=None, gps_staleness_min=None):
    """
    Check if inquiry should be escalated to human.

    Returns: {
        'escalate': bool,
        'reason': str,
        'priority': str,
        'all_triggers': list
    }
    """
    triggers = []

    # Trigger 1: Order not found (handled in validator, but included for completeness)
    if not order:
        return {
            'escalate': True,
            'reason': 'ORDER_NOT_FOUND',
            'priority': 'MEDIUM',
            'all_triggers': [{'type': 'ORDER_NOT_FOUND', 'detail': 'Order ID not found in system'}]
        }

    # Trigger 2: GPS stale (>30 min)
    if gps_staleness_min and gps_staleness_min > 30:
        triggers.append({
            'type': 'GPS_STALE',
            'detail': f'{gps_staleness_min} min > 30 min threshold',
            'priority': 'HIGH'
        })

    # Trigger 3: Customer demands callback (NLP detection)
    if user_message:
        callback_keywords = ['speak', 'call me', 'talk to someone', 'agent', 'human', 'person', 'representative']
        if any(keyword in user_message.lower() for keyword in callback_keywords):
            triggers.append({
                'type': 'CALLBACK_REQUESTED',
                'detail': 'Customer explicitly requested human contact',
                'priority': 'HIGH'
            })

    # Trigger 4: High-value order + exception status
    if order.get('package_value', 0) > 500 and order.get('order_status') == 'EXCEPTION':
        triggers.append({
            'type': 'HIGH_VALUE_EXCEPTION',
            'detail': f'£{order["package_value"]} package in exception state',
            'priority': 'URGENT'
        })

    # Trigger 5: Delivery exception status (any value)
    if order.get('order_status') == 'EXCEPTION':
        triggers.append({
            'type': 'DELIVERY_EXCEPTION',
            'detail': f'Order status: EXCEPTION - requires human investigation',
            'priority': 'HIGH'
        })

    if triggers:
        # Return highest priority trigger
        priority_order = {'URGENT': 0, 'HIGH': 1, 'MEDIUM': 2}
        triggers_sorted = sorted(triggers, key=lambda x: priority_order.get(x['priority'], 3))

        return {
            'escalate': True,
            'reason': triggers_sorted[0]['type'],
            'priority': triggers_sorted[0]['priority'],
            'all_triggers': triggers
        }

    return {
        'escalate': False,
        'reason': None,
        'priority': None,
        'all_triggers': []
    }

def get_confidence_label(confidence):
    """Convert confidence score to human-readable label"""
    if confidence >= 0.90:
        return 'HIGH'
    elif confidence >= 0.70:
        return 'MEDIUM'
    else:
        return 'LOW'

def get_delegation_archetype(order, escalation_result, precision_eta_result=None):
    """
    Determine delegation archetype based on order state and escalation triggers.

    Returns: 'FULLY_AGENTIC', 'AGENT_LED', 'HUMAN_ONLY'
    """
    if escalation_result['escalate']:
        return 'HUMAN_ONLY'

    if precision_eta_result:
        # If precision ETA requested and confidence is medium, it's agent-led
        if precision_eta_result.get('confidence', 1.0) < 0.90:
            return 'AGENT_LED'

    # Default to fully agentic for standard lookup
    return 'FULLY_AGENTIC'
