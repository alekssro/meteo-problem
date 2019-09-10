# import datetime
# import sys
from helpers import ReadLines
from helpers import Entry
from helpers import Model

infile = "data/Meteologica_vacante_ProgC_ProblemaDatos_20190903.txt"

# Read file into array of arrays (lines x <words)
data = ReadLines(infile)

# Transform array to arrays of 'Entry' objects
observations = []
predictions = []
for obs in data.observations:
    observations.append(Entry(obs))
for pred in data.predictions:
    predictions.append(Entry(pred))

# Fit Deming model and predict on predictions from input file
meteo_model = Model(observations, predictions)

# Calculate EMA and ECM errors by month on observations
# Group observation Entry objects by month and save to dictionary
months = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
entries_by_month = {}
entries_by_month.update(dict.fromkeys(months, []))      # initialize dictionary with months as keys
for entry in meteo_model.observations:
    month = str(entry.date_time.month)
    entries_by_month[month] = entries_by_month[month] + [entry]

# Get output
if __name__ == "__main__":
    
    # Print model slope and intersect, in that order
    print(format(meteo_model.slope, '.2f'), format(meteo_model.intersect, '.2f'))

    # Predict on observations by month and calculate EMA and ECM errors
    for month in months:

        # Get array with wind_speed values (X) and energy_production values (Y) (by month)
        wind_speed_observed = [obs.wind_speed for obs in entries_by_month[month]]
        energy_production_observed = [obs.energy_production for obs in entries_by_month[month]]

        # Predict energy production using the model
        energy_production_predicted = meteo_model.predictDeming(fitted_model=meteo_model.fitted_model,
                                                                x=wind_speed_observed)

        # Calculate EMA and ECM errors
        ema = meteo_model.calcEMA(observed=energy_production_observed, predicted=energy_production_predicted)
        ecm = meteo_model.calcECM(observed=energy_production_observed, predicted=energy_production_predicted)

        print("Mes" + month, format(ema, '.2f'), format(ecm, '.2f'))

    # Print prediction results
    res_predictions = meteo_model.predict_on
    for i in range(len(res_predictions)):
        print(res_predictions[i].date_time.strftime('%Y-%m-%d %H:%M'),
            format(res_predictions[i].energy_production, '.0f'))

