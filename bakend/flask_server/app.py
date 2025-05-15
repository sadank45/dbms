
from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database configuration - replace with your actual database credentials
DB_CONFIG = {
    'dbname': 'hotel',
    'user': 'postgres',
    'password': 'rohitsharma45',
    'host': 'localhost',
    'port': '5432'
}

class DatabaseHandler:
    def __init__(self, db_config):
        self.db_config = db_config
    
    def _get_connection(self):
        print("connected")
        return psycopg2.connect(**self.db_config)
    
    def read_data(self, query, params=None):
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    if params:
                        cur.execute(query, params)
                    else:
                        cur.execute(query)
                    return cur.fetchall()
        except Exception as e:
            return {'error': str(e)}

    def write_data(self, query, params=None):
        query = """
        INSERT INTO users (username, email, password_hash, created_at) 
        VALUES (%s, %s, %s, %s)
        RETURNING id;"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    if params:
                        cur.execute(query, params)
                    else:
                        cur.execute(query)
                    conn.commit()
                    return {'status': 'success'}
        except Exception as e:
            return {'error': str(e)}

# Initialize database handler
db = DatabaseHandler(DB_CONFIG)

# Routes
@app.route('/')
def main():
    return render_template("index.html")

@app.route('/db/read')
def read_route():
    # Example query - modify according to your table structure
    query = "SELECT * FROM your_table ORDER BY id DESC LIMIT 10"
    result = db.read_data(query)
    return jsonify(result)

@app.route('/db/write', methods=['POST'])
def write_route():
    data = request.json.get('data')
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Example query - modify according to your table structure
    query = "INSERT INTO your_table (content) VALUES (%s)"
    result = db.write_data(query, (data,))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)