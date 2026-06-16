from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Creatvs-Est</h1><p>Flask está rodando!</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
