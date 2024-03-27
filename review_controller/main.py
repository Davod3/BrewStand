from flask import Flask

app = Flask(__name__)

@app.route('/items/{itemId}/review', methods=['PUT'])
def newScore():
    return "Testing"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("3004"), debug=True)