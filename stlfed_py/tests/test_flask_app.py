import datetime
import json
import pandas as pd

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
    assert r.is_json
    data = json.loads(r.data.decode('utf-8'))
    assert list(data[0].keys()) == ['DATE', fred_id, 'label', 'MAPE']
    df = pd.DataFrame(data = data)
    df = df.sort_values('DATE')
    assert len(df) == len(data)
# end test_fcast
