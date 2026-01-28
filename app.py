from flask import Flask, request
from api import register_all
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / '.env')

app = Flask(__name__)
@app.after_request
def after_request(resp):
    origin = request.headers.get('Origin')
    if origin in {'https://www.565455.xyz', 'http://dev.565455.xyz', 'http://localhost:5500'}:
        resp.headers['Access-Control-Allow-Origin'] = origin
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return resp

register_all(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5520, debug=True)
