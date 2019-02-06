#!/usr/bin/env python3

from flask import Flask, request, Response
from waitress import serve
import pandas as pd
import stlfed_py.io.get as get
import stlfed_py.forecast.ets as fc

def create_app(test_config = None):
    app = Flask(__name__)

    # Flag for when running tests
    testing = True if (test_config is not None and test_config['TESTING']) else False

    # Index
    @app.route('/', methods = ['GET'])
    def index():
        helpstr = """
        Get forecasted data by hitting /api/fcast with a valid query string
        containing fred_id, start_date, and end_date.
        The defaults are MONAN, five years ago, and today, respectively.
        """
        return helpstr, 200
    #end index

    # Health check
    @app.route('/api/health', methods = ['GET'])
    def app_health():
        return '{"msg": "ok"}', 200
    # end app_health

    @app.route('/api/fcast', methods = ['GET'])
    def fcast():
        """
        Note that hitting this endpoint will return a JSON string that IS
        PROBABLY NOT SORTED (data is serialized to a dict, which are unsorted),
        so unless you control for it here, the client will need to sort the
        values themselves.
        """
        start_date_default = get.start_date_default
        end_date_default = get.end_date_default

        fred_id = request.args.get('fred_id', default = 'MONAN', type = str)
        start_date = request.args.get('start_date', default = start_date_default, type = str)
        end_date = request.args.get('end_date', default = end_date_default, type = str)

        try:
            df = get.get_fred(fred_id, start_date, end_date)
        except:
            errmsg = """
                Please check your fred_id, and/or dates, and try again. fred_id
                must be a valid FRED series ID, a list of which can be found here:
                https://fred.stlouisfed.org/tags/series. Hovering over the
                link will show you the series ID as the last URL component.
                start_date and end_date must be in the format YYYY-MM-DD. No
                exceptions. Figure it out.
            """
            return errmsg, 400
        df_fcast = fc.fredcast(df, fred_id)

        # Enforce response is *clean* JSON
        # just df.to_json() still returns text/html, and calling flask.jsonify()
        # on it adds too many escape characters
        resp = Response(
            response = df_fcast.to_json(orient = 'records'),
            status = 200,
            mimetype = 'application/json'
        )
        return resp
    # end api_fcast

    return app
# end create_app

def main(host = '0.0.0.0', port = 8089):
    app = create_app()
    serve(app, host = host, port = port)
# end main

if __name__ == '__main__':
    main()
