import config
from utils import encoder

app = config.connex_app
app.add_api(config.basedir / "payment_api.yaml")
app.app.json_encoder = encoder.JSONEncoder

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("3006"), debug=True)