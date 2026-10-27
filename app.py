from flask import Flask, render_template, request, jsonify
from modules.engine import PrecisionFarmingEngine
from modules.db import (
    init_db,
    save_recommendation,
    recent_recommendations,
)
from modules.weather import get_weather

app = Flask(__name__)
engine = PrecisionFarmingEngine()

# Connect to Neon and create the schema if it doesn't exist.
init_db()

@app.get('/')
def home():
    return render_template('index.html')

@app.post('/api/recommend')
def recommend():
    try:
        data = request.get_json(force=True)
        inputs = {k: float(data[k]) for k in ['N','P','K','temperature','humidity','ph','rainfall','soil_moisture']}
        soil_type = data.get('soil_type', 'Loamy')
        growth_stage = data.get('growth_stage', 'Vegetative')
        result = engine.recommend(inputs, soil_type, growth_stage)
        save_recommendation(inputs, soil_type, growth_stage, result)
        return jsonify({'success': True, **result})
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({'success': False, 'error': f'Please check all input values. {exc}'}), 400
    except Exception as exc:
        app.logger.exception('Recommendation failed')
        return jsonify({'success': False, 'error': 'Could not generate a recommendation. Check the server terminal.'}), 500

@app.post('/api/weather')
def weather():
    data = request.get_json(force=True)
    return jsonify(get_weather(data.get('city',''), data.get('api_key','')))

@app.get('/api/history')
def history():
    return jsonify({'success': True, 'items': recent_recommendations()})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
