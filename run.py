# from test_DD import app
from test_DD import create_app

config_name = "development"
app = create_app(config_name)

app.run(host='0.0.0.0', port=5005, threaded=True)