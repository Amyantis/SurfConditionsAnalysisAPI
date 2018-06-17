from flasgger import Swagger, SwaggerView
from flask import Flask, Response
from flask_compress import Compress
from flask_cors import CORS

from src.datasets import get_wave_df, get_wind_df, get_weather_df, get_conditions_df, get_tides_df


class WavesView(SwaggerView):
    def get(self):
        """ Gets the waves data. """
        df = get_wave_df()
        return Response(df.to_csv(), mimetype='text/csv')


class WeatherView(SwaggerView):
    def get(self):
        """ Gets the weather data. """
        df = get_weather_df()
        return Response(df.to_csv(), mimetype='text/csv')


class ConditionsView(SwaggerView):
    def get(self):
        """ Gets the conditions data. """
        df = get_conditions_df()
        return Response(df.to_csv(), mimetype='text/csv')


class WindView(SwaggerView):
    def get(self):
        """ Gets the wind data. """
        df = get_wind_df()
        return Response(df.to_csv(), mimetype='text/csv')


class TidesView(SwaggerView):
    def get(self):
        """ Gets the tides data. """
        df = get_tides_df()
        return Response(df.to_csv(), mimetype='text/csv')


app = Flask(__name__)
swagger = Swagger(app)
compress = Compress()
compress.init_app(app)
CORS(app)

app.add_url_rule('/waves.csv', view_func=WavesView.as_view('waves.csv'), methods=['GET'])
app.add_url_rule('/conditions.csv', view_func=ConditionsView.as_view('conditions.csv'), methods=['GET'])
app.add_url_rule('/weather.csv', view_func=WeatherView.as_view('weather.csv'), methods=['GET'])
app.add_url_rule('/wind.csv', view_func=WindView.as_view('wind.csv'), methods=['GET'])
app.add_url_rule('/tides.csv', view_func=TidesView.as_view('tides.csv'), methods=['GET'])

app.run(debug=True)
