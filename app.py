# import datetime
# import sys
from helpers import ReadLines
from helpers import Entry
from helpers import Model

infile = "Meteologica_vacante_ProgC_Problema_20190903/Meteologica_vacante_ProgC_ProblemaDatos_20190903.txt"

data = ReadLines(infile)

print(len(data.all_entries))
print(len(data.observations))
print(len(data.predictions))

# transform arrays to 'Entry' objects
observations = []
predictions = []
for obs in data.observations:
    observations.append(Entry(obs))
for pred in data.predictions:
    predictions.append(Entry(pred))

m = Model(observations, predictions)
for pred in m.predict_on_ord:
    print(pred.date, pred.time, pred.energy_production, pred.wind_speed)

print(m.fitted_model[0])
print(m.fitted_model[1])

print(m.predicts)
