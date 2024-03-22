import config
from utils import encoder

app = config.connex_app
app.add_api(config.basedir / "openapi.yaml")
app.app.json_encoder = encoder.JSONEncoder


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
