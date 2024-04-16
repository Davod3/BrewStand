import config
from utils import encoder
import psutil
from prometheus_client import generate_latest, Gauge

app = config.connex_app
app.add_api(config.basedir / "review_api.yaml")
app.app.json_encoder = encoder.JSONEncoder

@app.route('/')
def health_check():
    return "OK", 200

@app.route('/metrics')
def metrics():
    return generate_latest()

def getCPU():
    return psutil.cpu_percent()

def getMemUsage():
    return psutil.virtual_memory().percent

cpu_usage_metric = Gauge('review_cpu_usage', 'Shows the current the pecentage of cpu being used by the process')
cpu_usage_metric.set_function(getCPU)

memory_usage_metric = Gauge('review_mem_usage', 'Shows current percentage of memory used')
memory_usage_metric.set_function(getMemUsage)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("3003"), debug=True)