from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    return jsonify(message="Hello from the mock server!")

if __name__ == "__main__":
    app.run(port=5001)