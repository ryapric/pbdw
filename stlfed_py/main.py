#!/usr/bin/env python3

from stlfed_py.io.get import get_fred
from stlfed_py.forecast.ets import fredcast
from stlfed_py.io.db import db_write

# Note that if this was made distributable, you should consider controlling your
# namespace in the highest-level __init__.py file. So then, you can just run
# `import stlfed_py as fc`, and all the following functions could belong the
# same, controlled namespace.

fred_id = 'MONAN' # MO Total Non-Farm Employment

df = get_fred(fred_id)
df_fcast = fredcast(df, fred_id)
db_write(df_fcast, fred_id)
