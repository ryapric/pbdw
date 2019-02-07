using CSV
using DataFrames
using Dates
using GLM

url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
fred_id = "MONAN" # MO Total Non-Farm Employment
today = Dates.today()
start_date = today - Dates.Year(5)
end_date = today

# Shitty way around not asking for an API key
# Should eventually call httr::GET() with a key, to directly return a dataframe
tmpfile = mktemp()[1]
download("$url?id=$fred_id&cosd=$start_date&coed=$end_date", tmpfile)

df = CSV.read(tmpfile)

# Prep
df[:DATE] = Dates.Date.(df[:DATE])
df[:trend] = [1:size(df, 1);]
df[:month] = categorical(Dates.month.(df[:DATE]))
df[:label] = "Actual"

# Fit linear model, because Julia doesn't have a forecast/time-series library
# Need fred_id to be dynamic, so 
y = Symbol(eval(:fred_id))
@eval fit = lm(@formula($y ~ trend + month), df);

# "Forecast"
h = 12

df_fcast = @eval DataFrame(
    DATE = [df[end, :DATE] + Dates.Month(i) for i in 1:h],
    trend = [(df[end, :trend] + 1):(df[end, :trend] + h);]
)
df_fcast[:month] = categorical(Dates.month.(df_fcast[:DATE]))

@eval df_fcast[Symbol(eval(fred_id))] = predict(fit, df_fcast);
df_fcast[:label] = "Forecast"

# NO GODDAMN AUTO NAME RESOLUTION FUCKING WHAT
# BEHOLD, METAAAPROOOGRAMMINGGG
orderednames = Meta.parse('[' * join([':' * String(names(df)[i]) for i in 1:size(df,2)], ", ") * ']')
df_fcast = @eval df_fcast[$orderednames]
append!(df, df_fcast)
