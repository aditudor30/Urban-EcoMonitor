from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

DB_CONFIG = "dbname=postgres user=postgres password=password host=localhost"

def get_db():
    return psycopg2.connect(DB_CONFIG)

@app.route('/api/ingest', methods=['POST'])
def ingest():
    data = request.json
    try:
        conn = get_db()
        cur = conn.cursor()
        query = """
            INSERT INTO sensor_data (time, temperature, humidity, pressure, co2, people, power_usage, hvac_target, energy_cost, is_eco, light_lux, light_dimmer, ventilation_control)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (
            data['timestamp'], 
            data.get('temp', 0), data.get('hum', 0), 1013, 
            data.get('co2', 400), data.get('people', 0), 
            data.get('power', 0), data.get('hvac', 22.0),
            data.get('cost', 0.0), data.get('is_eco', 1),
            data.get('lux', 0), data.get('dimmer', 0),
            data.get('fan_speed', 0) # <--- AICI
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"msg": "Salvat"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/status', methods=['GET'])
def status():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sensor_data ORDER BY time DESC LIMIT 1")
        row = cur.fetchone()
        
        cur.execute("SELECT SUM(energy_cost) FROM sensor_data")
        res_total = cur.fetchone()
        total_bill = res_total[0] if res_total and res_total[0] else 0.0
        
        cur.close()
        conn.close()

        if row:
            return jsonify({
                "timestamp": row[0].strftime("%H:%M"),
                "temperature": row[1],
                "humidity": row[2],
                "co2": row[4],
                "people": row[5],
                "power": row[6],
                "hvac_target": row[7] if len(row) > 7 else 0,
                "total_bill": round(total_bill, 2),
                "is_eco": row[9] if len(row) > 9 else 1,
                "lux": row[10] if len(row) > 10 else 0,
                "dimmer": row[11] if len(row) > 11 else 0,
                "fan_speed": row[12] if len(row) > 12 else 0 
            })
        else:
            return jsonify({"msg": "No data"}), 200
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def history():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT time, temperature, co2 FROM sensor_data ORDER BY time DESC LIMIT 20")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        rows = rows[::-1]
        return jsonify({
            "labels": [row[0].strftime("%H:%M") for row in rows],
            "temp": [row[1] for row in rows],
            "co2": [row[2] for row in rows]
        })
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/api/analytics', methods=['GET'])
def analytics():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT is_eco, COUNT(*) FROM sensor_data GROUP BY is_eco")
        rows_eco = cur.fetchall()
        eco_count = 0; waste_count = 0
        for r in rows_eco:
            if r[0] == 1: eco_count = r[1]
            else: waste_count = r[1]
        
        cur.execute("SELECT EXTRACT(HOUR FROM time) as hour, AVG(power_usage) FROM sensor_data GROUP BY hour ORDER BY hour ASC")
        rows_hourly = cur.fetchall()
        
        cur.execute("SELECT AVG(temperature), MAX(people), SUM(energy_cost) FROM sensor_data")
        kpi_row = cur.fetchone()
        cur.close()
        conn.close()

        return jsonify({
            "pie_data": [eco_count, waste_count],
            "bar_labels": [int(r[0]) for r in rows_hourly],
            "bar_data": [r[1] for r in rows_hourly],
            "avg_temp": round(kpi_row[0], 1) if kpi_row and kpi_row[0] else 0,
            "max_people": kpi_row[1] if kpi_row and kpi_row[1] else 0,
            "total_cost_all_time": round(kpi_row[2], 2) if kpi_row and kpi_row[2] else 0
        })
    except Exception as e: return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)