from flask import Flask, jsonify, request
import psycopg2
import redis
import os
from config import Config

app = Flask(__name__)

DB_CONFIG = {
    "host": Config.DB_HOST,
    "port": Config.DB_PORT,
    "database": Config.DB_NAME,
    "user": Config.DB_USER,
    "password": Config.DB_PASSWORD
}

redis_client = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

@app.route("/")
def home():
    return jsonify({"app": "Lab5 API", "status": "running"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/db-test")
def db_test():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({"status": "success", "database": version})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route("/cache-test")
def cache_test():
    try:
        redis_client.set("test_key", "test_value", ex=60)
        value = redis_client.get("test_key")
        return jsonify({"status": "success", "redis": "connected", "test_value": value})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)