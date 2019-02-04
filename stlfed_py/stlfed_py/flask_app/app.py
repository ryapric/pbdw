from flask import Flask, request
from waitress import serve
import datetime
import pandas as pd

def create_app(test_config = None):
    app = Flask(__name__)

    # Flag for when running tests
    testing = True if (test_config is not None and test_config['TESTING']) else False

    # Index
    @app.route('/api/health', methods = ['GET'])
    def index():
        return 'Get forecasted data by either ...', 200
    #end index

    # Health check
    @app.route('/api/health', methods = ['GET'])
    def app_health():
        return '{"msg": "ok"}', 200
    # end app_health

    @app.route('/api/fcast', methods = ['GET'])
    def fcast():
        """
        Will take either URL params, OR JSON body of the request, but not both.
        If the former, do not set 'application/json' as Content-Type in header.
        """
        fred_id_default = 'MONAN'
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        start_date_default = (pd.to_datetime(today) - pd.DateOffset(years = 5)).strftime('%Y-%m-%d')
        end_date_default = today
        
        json_data = request.get_json()
        if json_data is None:
            fred_id = request.args.get('fred_id', default = fred_id_default, type = str)
            start_date = request.args.get('start_date', default = start_date_default, type = str)
            end_date = request.args.get('end_date', default = end_date_default, type = str)
        else:
            fred_id = json_data['fred_id'] if 'fred_id' in json_data else fred_id_default
            start_date = json_data['start_date'] if 'start_date' in json_data else start_date_default
            end_date = json_data['end_date'] if 'end_date' in json_data else end_date_default

        return f'{fred_id}, from {start_date} to {end_date}', 200
    # end api_fcast

    return app
# end create_app

def main(host = '0.0.0.0', port = 8089):
    app = create_app()
    serve(app, host = host, port = port)
# end main

if __name__ == '__main__':
    main()
