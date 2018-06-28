from flasgger import Swagger
from flask_compress import Compress
from flask_cors import CORS

from src.api.app import app
from src.api.views import GlobalConditionsView, TidesView, WindView, \
    ConditionsView, WavesView, WeatherView, SpotView

swagger = Swagger(app)
compress = Compress()
compress.init_app(app)
CORS(app)

app.add_url_rule('/waves.json',
                 view_func=WavesView.as_view('waves.json'),
                 methods=['GET'])
app.add_url_rule('/conditions.json',
                 view_func=ConditionsView.as_view('conditions.json'),
                 methods=['GET'])
app.add_url_rule('/weather.json',
                 view_func=WeatherView.as_view('weather.json'),
                 methods=['GET'])
app.add_url_rule('/wind.json',
                 view_func=WindView.as_view('wind.json'),
                 methods=['GET'])
app.add_url_rule('/tides.json',
                 view_func=TidesView.as_view('tides.json'),
                 methods=['GET'])
app.add_url_rule('/global.json',
                 view_func=GlobalConditionsView.as_view('global.json'),
                 methods=['GET'])
app.add_url_rule('/spots.json',
                 view_func=SpotView.as_view('gu'),
                 methods=['GET'])

app.run(host="0.0.0.0", debug=False)
