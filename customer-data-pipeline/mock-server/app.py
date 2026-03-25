from flask import Flask, jsonify, request
import json
import os
from pathlib import Path

app = Flask(__name__)

def load_customers():
    data_path = Path(__file__).parent / "data" / "customers.json"
    with open(data_path, 'r') as f:
        return json.load(f)

CUSTOMERS = load_customers()

@app.route('/api/customers', methods=['GET'])
def get_customers():
    """
    Get paginated list of customers
    Query params:
    - page: page number (default: 1)
    - limit: records per page (default: 10)
    """
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        if page < 1:
            page = 1
        if limit < 1:
            limit = 10
        if limit > 100:
            limit = 100
        
        total = len(CUSTOMERS)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        rt_idx:end_idx
        
        return jsonify({
            "data": data,
            "total": total,
            "page": page,
            "limit": limit
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get single customer by ID"""
    try:
        customer = next((c for c in CUSTOMERS if c['customer_id'] == customer_id), None)
        
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        
        return jsonify(customer), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "mock-server"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
