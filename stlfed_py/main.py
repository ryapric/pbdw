#!/usr/bin/env python3

import stlfed_py.io.get as get
import stlfed_py.io.db as db
import stlfed_py.forecast.ets as fc

fred_id = 'MONAN' # MO Total Non-Farm Employment

df = get.get_fred(fred_id)
df_fcast = fc.fredcast(df, fred_id)
db.db_write(df_fcast, fred_id)
