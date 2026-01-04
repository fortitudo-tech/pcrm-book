from flask import Flask, render_template, send_file, jsonify
import os
import subprocess
from datetime import datetime

app = Flask(__name__)

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """Run the liquidity_website_plotly.py script to regenerate data and charts"""
    try:
        script_path = os.path.join(BASE_DIR, 'liquidity_website_plotly.py')
        result = subprocess.run(
            ['python', script_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            return jsonify({
                'status': 'success',
                'message': 'Data refreshed successfully',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'Error: {result.stderr}'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/charts/<chart_name>')
def get_chart(chart_name):
    """Serve interactive HTML chart files"""
    try:
        chart_path = os.path.join(BASE_DIR, chart_name)
        if os.path.exists(chart_path) and chart_name.endswith('.html'):
            return send_file(chart_path, mimetype='text/html')
        else:
            return "Chart not found", 404
    except Exception as e:
        return str(e), 500

@app.route('/api/chart_exists/<chart_name>')
def chart_exists(chart_name):
    """Check if a chart file exists"""
    chart_path = os.path.join(BASE_DIR, chart_name)
    return jsonify({'exists': os.path.exists(chart_path)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
