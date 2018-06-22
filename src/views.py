from datetime import datetime

import pandas as pd
import pytz
from flasgger import SwaggerView, fields
from marshmallow import Schema
from webargs.flaskparser import use_kwargs

from src.datasets import get_wave_df, get_tides_df, get_weather_df, \
    get_wind_df, get_conditions_df


class APISchema(Schema):
    class Meta:
        strict = True


class Resource(APISchema):
    start_date = fields.DateTime(missing=datetime.now(tz=pytz.utc).isoformat())


class GlobalConditionsView(SwaggerView):
    parameters = Resource

    @use_kwargs(Resource())
    def get(self, start_date):
        """ Gets the global conditions at once. """
        df_wave = get_wave_df()
        df_tides = get_tides_df()
        df_weather = get_weather_df()
        df_wind = get_wind_df()

        def suffix(df, suffix="", inplace=False):
            return df.rename(
                columns={c: suffix + c for c in df.columns if c != "timestamp"},
                inplace=inplace)

        df = pd.merge(
            suffix(df_wave, "wave_"), suffix(df_wind, "wind_"), on='timestamp')
        df = pd.merge(
            df, suffix(df_weather, "weather_"), on='timestamp')
        df = pd.merge(
            df, suffix(df_tides, "tides_"), on='timestamp')

        df = df[df.timestamp > start_date]
        return df.to_json(orient='records')


class TidesView(SwaggerView):
    def get(self):
        """ Gets the tides data. """
        df = get_tides_df()
        return df.to_json(orient='records')


class WindView(SwaggerView):
    def get(self):
        """ Gets the wind data. """
        df = get_wind_df()
        return df.to_json(orient='records')


class ConditionsView(SwaggerView):
    def get(self):
        """ Gets the conditions data. """
        df = get_conditions_df()
        return df.to_json(orient='records')


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
