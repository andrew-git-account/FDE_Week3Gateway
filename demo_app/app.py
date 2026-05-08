from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

from agent.order_validator import extract_order_id, validate_order
from agent.eta_calculator import get_standard_eta, calculate_precision_eta
from agent.escalation_engine import check_escalation_triggers, get_confidence_label, get_delegation_archetype

app = Flask(__name__)
CORS(app)

# In-memory decision log for demo
decision_log = []

# Demo statistics
demo_stats = {
    'total_inquiries': 0,
    'deflected': 0,
    'escalated': 0,
    'avg_response_time_ms': 850,
    'baseline_response_time_min': 8.5
}

@app.route('/')
def index():
    """Customer inquiry page"""
    return render_template('index.html')

@app.route('/admin')
def admin():
    """Admin panel page"""
    return render_template('admin.html')

@app.route('/comparison')
def comparison():
    """Comparison view page"""
    return render_template('comparison.html')

@app.route('/api/inquire', methods=['POST'])
def inquire():
    """
    Process customer ETA inquiry (standard lookup).

    Request: {
        'message': 'Where is order AX-771-3344?'
    }

    Response: {
        'success': bool,
        'order_id': str,
        'response_message': str,
        'eta_window': str,
        'delegation_level': str,
        'escalation': dict or None,
        'response_time_ms': int
    }
    """
    start_time = datetime.now()

    data = request.json
    message = data.get('message', '')

    # Extract order ID
    order_id = extract_order_id(message)

    if not order_id:
        return jsonify({
            'success': False,
            'error': 'Could not find order ID in message. Please include your order number (e.g., AX-771-3344).',
            'response_time_ms': int((datetime.now() - start_time).total_seconds() * 1000)
        })

    # Validate order exists
    order = validate_order(order_id)

    if not order:
        escalation = check_escalation_triggers(None, message)
        log_decision(order_id, 'ORDER_NOT_FOUND', 'HUMAN_ONLY', escalation, start_time)

        return jsonify({
            'success': False,
            'order_id': order_id,
            'error': f'Order {order_id} not found in system. Please check the order number and try again, or click "Speak with someone" for assistance.',
            'escalation': escalation,
            'response_time_ms': int((datetime.now() - start_time).total_seconds() * 1000)
        })

    # Check escalation triggers
    escalation = check_escalation_triggers(order, message)

    if escalation['escalate']:
        log_decision(order_id, 'STANDARD_LOOKUP_ESCALATED', 'HUMAN_ONLY', escalation, start_time)

        return jsonify({
            'success': True,
            'order_id': order_id,
            'order': order,
            'escalation': escalation,
            'response_message': generate_escalation_message(escalation, order),
            'delegation_level': 'HUMAN_ONLY',
            'response_time_ms': int((datetime.now() - start_time).total_seconds() * 1000)
        })

    # Get standard ETA
    eta_result = get_standard_eta(order)

    response_message = f"Your order {order_id} is out for delivery on route {order['route_id']}. Scheduled delivery window: {eta_result['eta_window']} today."

    if order['order_status'] != 'OUT_FOR_DELIVERY':
        response_message = f"Your order {order_id} status: {order['order_status']}. Scheduled delivery window: {eta_result['eta_window']}."

    log_decision(order_id, 'STANDARD_LOOKUP', 'FULLY_AGENTIC', None, start_time)

    demo_stats['total_inquiries'] += 1
    demo_stats['deflected'] += 1

    return jsonify({
        'success': True,
        'order_id': order_id,
        'order': order,
        'response_message': response_message,
        'eta_window': eta_result['eta_window'],
        'delegation_level': 'FULLY_AGENTIC',
        'escalation': None,
        'response_time_ms': int((datetime.now() - start_time).total_seconds() * 1000)
    })

@app.route('/api/precision-eta', methods=['POST'])
def precision_eta():
    """
    Calculate precision ETA based on GPS data.

    Request: {
        'order_id': 'AX-771-3344'
    }

    Response: {
        'success': bool,
        'eta_start': str,
        'eta_end': str,
        'confidence': float,
        'confidence_label': str,
        'gps_staleness_min': int,
        'calculation_details': dict,
        'delegation_level': str,
        'escalation': dict or None,
        'response_time_ms': int
    }
    """
    start_time = datetime.now()

    data = request.json
    order_id = data.get('order_id')

    # Validate order
    order = validate_order(order_id)

    if not order:
        return jsonify({
            'success': False,
            'error': 'Order not found'
        })

    # Calculate precision ETA
    eta_result = calculate_precision_eta(order)

    # Check if escalation triggered
    if eta_result.get('escalation_triggered'):
        escalation = {
            'escalate': True,
            'reason': 'GPS_STALE',
            'priority': 'HIGH',
            'all_triggers': [{
                'type': 'GPS_STALE',
                'detail': eta_result['escalation_reason'],
                'priority': 'HIGH'
            }]
        }

        log_decision(order_id, 'PRECISION_ETA_ESCALATED', 'HUMAN_ONLY', escalation, start_time)

        demo_stats['total_inquiries'] += 1
        demo_stats['escalated'] += 1

        return jsonify({
            'success': True,
            'escalation': escalation,
            'response_message': f"I'm unable to provide a precise ETA due to outdated location data (last updated {eta_result['gps_staleness_min']} min ago). Connecting you with a specialist who can contact the driver directly. Hold time: ~2 minutes.",
            'delegation_level': 'HUMAN_ONLY',
            'gps_staleness_min': eta_result['gps_staleness_min'],
            'response_time_ms': int((datetime.now() - start_time).total_seconds() * 1000)
        })

    # Successful precision ETA calculation
    confidence_label = get_confidence_label(eta_result['confidence'])
    delegation_level = 'AGENT_LED' if eta_result['confidence'] < 0.90 else 'FULLY_AGENTIC'

    details = eta_result['calculation_details']
    response_message = f"Based on current driver location ({details['driver_location']}, last updated {eta_result['gps_staleness_min']} min ago), your delivery is estimated between {eta_result['eta_start']}-{eta_result['eta_end']}. {details['remaining_stops']} stops remaining. Confidence: {confidence_label}."

    log_decision(order_id, 'PRECISION_ETA', delegation_level, None, start_time, eta_result)

    demo_stats['total_inquiries'] += 1
    demo_stats['deflected'] += 1

    return jsonify({
        'success': True,
        'response_message': response_message,
        'eta_start': eta_result['eta_start'],
        'eta_end': eta_result['eta_end'],
        'confidence': eta_result['confidence'],
        'confidence_label': confidence_label,
        'gps_staleness_min': eta_result['gps_staleness_min'],
        'calculation_details': details,
        'delegation_level': delegation_level,
        'escalation': None,
        'response_time_ms': int((datetime.now() - start_time).total_seconds() * 1000)
    })

@app.route('/api/escalate', methods=['POST'])
def escalate():
    """
    Manually escalate to human agent.

    Request: {
        'order_id': 'AX-771-3344',
        'reason': 'Customer requested callback'
    }
    """
    data = request.json
    order_id = data.get('order_id')
    reason = data.get('reason', 'Customer requested human contact')

    escalation = {
        'escalate': True,
        'reason': 'CALLBACK_REQUESTED',
        'priority': 'HIGH',
        'all_triggers': [{
            'type': 'CALLBACK_REQUESTED',
            'detail': reason,
            'priority': 'HIGH'
        }]
    }

    log_decision(order_id, 'MANUAL_ESCALATION', 'HUMAN_ONLY', escalation, datetime.now())

    demo_stats['total_inquiries'] += 1
    demo_stats['escalated'] += 1

    return jsonify({
        'success': True,
        'response_message': 'Connecting you with a customer service specialist. Hold time: ~2 minutes.',
        'escalation': escalation
    })

@app.route('/api/decision-log', methods=['GET'])
def get_decision_log():
    """Get decision log for admin panel"""
    return jsonify({
        'log': decision_log,
        'stats': demo_stats
    })

@app.route('/api/demo-stats', methods=['GET'])
def get_demo_stats():
    """Get demo statistics for comparison view"""
    return jsonify({
        'current_state': {
            'response_time_p50_min': 8.5,
            'response_time_p95_min': 17.0,
            'eta_precision_hours': 4,
            'deflection_rate_pct': 0,
            'daily_labor_hours': 73,
            'annual_cost': 301000
        },
        'agent_state': {
            'response_time_p50_sec': 30,
            'response_time_p95_sec': 120,
            'eta_precision_min': 30,
            'deflection_rate_pct': 90,
            'daily_labor_hours': 7,
            'annual_savings': 301000
        },
        'live_stats': demo_stats
    })

def log_decision(order_id, action, delegation_level, escalation, start_time, eta_result=None):
    """Log agent decision to in-memory log"""
    response_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)

    decision_log.append({
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'order_id': order_id,
        'action': action,
        'delegation_level': delegation_level,
        'response_time_ms': response_time_ms,
        'escalated': escalation is not None and escalation.get('escalate', False),
        'escalation_reason': escalation.get('reason') if escalation else None,
        'confidence': eta_result.get('confidence') if eta_result else None
    })

def generate_escalation_message(escalation, order):
    """Generate human-friendly escalation message"""
    reason = escalation.get('reason', 'UNKNOWN')

    messages = {
        'GPS_STALE': 'I\'m unable to provide a precise ETA due to outdated location data. Connecting you with a specialist who can contact the driver directly.',
        'CALLBACK_REQUESTED': 'Connecting you with a customer service specialist.',
        'HIGH_VALUE_EXCEPTION': f'Your high-value order (£{order["package_value"]}) requires specialist attention due to a delivery exception.',
        'DELIVERY_EXCEPTION': 'Your order has a delivery exception that requires specialist attention.',
        'ORDER_NOT_FOUND': 'I couldn\'t find that order number. A specialist can help verify your order details.'
    }

    return messages.get(reason, 'Connecting you with a specialist for assistance.') + ' Hold time: ~2 minutes.'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
