import datetime
import json

def test_health(client):
    r = client.get('/api/health')
    assert r.status_code == 200
    assert r.data == b'{"msg": "ok"}'
# end test_health

def test_fcast(client):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    fred_id = 'UNRATE'
    start_date = '2018-01-01'
    r = client.get(f'/api/fcast?fred_id={fred_id}&start_date={start_date}')
    assert r.data == f'{fred_id}, from {start_date} to {today}'.encode('utf-8')
# end test_fcast
