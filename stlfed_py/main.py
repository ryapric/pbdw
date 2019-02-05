#!/usr/bin/env python3

import stlfed_py.io.get as get
import stlfed_py.io.db as db
import stlfed_py.forecast.ets as fc

# Note that if this was made distributable, you should consider controlling your
# namespace in the highest-level __init__.py file. So then, you can just run
# `import stlfed_py as fc`, and all the following functions could belong the
# same, controlled namespace.

fred_id = 'MONAN' # MO Total Non-Farm Employment

df = get.get_fred(fred_id)
df_fcast = fc.fredcast(df, fred_id)
db.db_write(df_fcast, fred_id)
