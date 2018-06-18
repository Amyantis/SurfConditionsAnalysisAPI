from flasgger import Swagger, SwaggerView
from flask import Flask, Response
from flask_compress import Compress
from flask_cors import CORS

from src.datasets import get_wave_df, get_wind_df, get_weather_df, get_conditions_df, get_tides_df


class WavesView(SwaggerView):
    def get(self):
        """ Gets the waves data. """
        df = get_wave_df()
        return df.to_json(orient='records')


class WeatherView(SwaggerView):
    def get(self):
        """ Gets the weather data. """
        df = get_weather_df()
        return df.to_json(orient='records')


class ConditionsView(SwaggerView):
    def get(self):
        """ Gets the conditions data. """
        df = get_conditions_df()
        return df.to_json(orient='records')


class WindView(SwaggerView):
    def get(self):
        """ Gets the wind data. """
        df = get_wind_df()
        return df.to_json(orient='records')


class TidesView(SwaggerView):
    def get(self):
        """ Gets the tides data. """
        df = get_tides_df()
        return df.to_json(orient='records')


app = Flask(__name__)
swagger = Swagger(app)
compress = Compress()
compress.init_app(app)
CORS(app)

app.add_url_rule('/waves.json', view_func=WavesView.as_view('waves.json'), methods=['GET'])
app.add_url_rule('/conditions.json', view_func=ConditionsView.as_view('conditions.json'), methods=['GET'])
app.add_url_rule('/weather.json', view_func=WeatherView.as_view('weather.json'), methods=['GET'])
app.add_url_rule('/wind.json', view_func=WindView.as_view('wind.json'), methods=['GET'])
app.add_url_rule('/tides.json', view_func=TidesView.as_view('tides.json'), methods=['GET'])

app.run(debug=True)
