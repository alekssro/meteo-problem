# import datetime
# import sys
from helpers import ReadLines
from helpers import Entry
from helpers import Model

infile = "data/Meteologica_vacante_ProgC_ProblemaDatos_20190903.txt"

data = ReadLines(infile)

# Transform arrays to 'Entry' objects
observations = []
predictions = []
for obs in data.observations:
    observations.append(Entry(obs))
for pred in data.predictions:
    predictions.append(Entry(pred))

# Fit Deming model and predict on predictions from input file
meteo_model = Model(observations, observations)
print(meteo_model.slope, meteo_model.intersect)

# Get prediction results
res_predictions = meteo_model.predict_on
for i in range(len(res_predictions)):
    print(res_predictions[i].date_time, meteo_model.y_observed[i],
          res_predictions[i].energy_production, res_predictions[i].wind_speed)

# Compare observed energy production values with predictions obtained on the same data, using the model
energy_production_observed = meteo_model.y_observed
wind_speed_observed = meteo_model.x_observed
energy_production_predicted = meteo_model.predictDeming(fitted_model=meteo_model.fitted_model,
                                                        x=wind_speed_observed)

# Calculate EMA and ECM errors by month on observations
# Filter observation Entry objects by month
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
for month in months:
    for entry in observations:
        if int(month) == entry.date_time.month:
            print("hello")
temp = meteo_model.groupByMonth(x=observations)

# Calculate EMA and ECM errors
ema = meteo_model.calcEMA(observed=energy_production_observed, predicted=energy_production_predicted)
ecm = meteo_model.calcECM(observed=energy_production_observed, predicted=energy_production_predicted)
print(ema, ecm)


# for i in range(len(ep_observed)):
#     print([i], ep_predicted[i])

# print(type(meteo_model.observations[0]), type(meteo_model.predict_on[0]))
# print(len(meteo_model.ep_observed), len(meteo_model.ep_predicted))
# print(meteo_model.ep_predicted)
# print(meteo_model.calcEMA(meteo_model.ep_observed, meteo_model.ep_predicted))

# print(m.predicts)
# for pred in m.predict_on_ord:
#     print(pred.date, pred.time, pred.energy_production, pred.wind_speed)

# OUTPUT
