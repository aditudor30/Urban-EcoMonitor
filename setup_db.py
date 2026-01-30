import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_CONFIG = "dbname=postgres user=postgres password=password host=localhost"

def init_db():
    try:
        conn = psycopg2.connect(DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS sensor_data;")
        
        # Tabel nou cu coloana VENTILATION
        cur.execute("""
            CREATE TABLE sensor_data (
                time TIMESTAMPTZ NOT NULL,
                temperature DOUBLE PRECISION,
                humidity DOUBLE PRECISION,
                pressure DOUBLE PRECISION,
                co2 DOUBLE PRECISION,
                people INTEGER,
                power_usage DOUBLE PRECISION,
                hvac_target DOUBLE PRECISION,
                energy_cost DOUBLE PRECISION,
                is_eco INTEGER,
                light_lux DOUBLE PRECISION,
                light_dimmer DOUBLE PRECISION,
                ventilation_control DOUBLE PRECISION -- <--- NOU: Viteza ventilatorului (%)
            );
        """)
        
        try:
            cur.execute("SELECT create_hypertable('sensor_data', 'time');")
        except:
            pass

        print("The database is ready for Smart Ventilation!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    init_db()