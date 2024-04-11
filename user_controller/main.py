import config
from utils import encoder

app = config.connex_app
app.add_api(config.basedir / "user_api.yaml")
app.app.json_encoder = encoder.JSONEncoder

@app.route('/')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("3002"), debug=True)