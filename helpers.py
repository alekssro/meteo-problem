import datetime
import sys

infile = "Meteologica_vacante_ProgC_Problema_20190903/Meteologica_vacante_ProgC_ProblemaDatos_20190903.txt"


class Entry:
    """store observation or prediction object with properties: date, energy production, wind speed.
        INPUT: string with date (YYYY-MM-DD), time (hh:mm), energy production
                and wind speed; separated by whitespace.
        OUTPUT: creates and object with the input fields as properties."""

    # define default variable values
    line = ""   # input string
    date = datetime.date.today()
    time = datetime.time(hour=0, minute=0)
    energy_production = None
    wind_speed = None
    list_fields = [date, time, energy_production, wind_speed]

    def __init__(self, list_fields):

        self.date = list_fields[0]
        self.time = list_fields[1]

        if len(list_fields) == 4:

            self.energy_production = list_fields[2]
            self.wind_speed = list_fields[3]
            self.entry_type = "obs"

        elif len(list_fields) == 3:

            self.wind_speed = list_fields[2]
            self.entry_type = "pred"


class Model:
    """adjust and model a list of 'Entry' objects; calculates the absolute mean error and the mean
            cuadratic error. additionally, makes predictions for a list of prediction 'Entry' objects.
        INPUT: List of 'Entry' objects to be modelled or to predict on
        OUTPUT: a text file which contains the slope and intersect values in the first line, the month
                and the 2 errors made as second line and the prediction of energy production (one per
                prediction entry)"""

    fitted_model = [0, 0]
    observations = []   # array of observations as Entry objects
    predict_on = []

    def __init__(self, observations, predict_on):

        # Fit Deming regression model
        self.fitted_model = self.fitDeming(observations)

        # Order entries to predict
        self.predict_on_ord = self.orderPreds(predict_on, by="time")
        self.predict_on_ord = self.orderPreds(self.predict_on_ord, by="date")

        # Get predictions & errors
        self.predicts = self.predictDeming(model=self.fitted_model, predict_on=self.predict_on_ord)
        self.ema = self.calcEMA(observed=self.observations, predicted=self.predicts)  # Error Medio Absoluto
        self.ecm = self.calcECM(observed=self.observations, predicted=self.predicts)  # Error Cuadratico Medio

        # Write OUTPUT
        self.write2file(fitmodel=self.fitted_model, ema=self.ema, ecm=self.ecm, predictions=self.predictss)


class ReadLines:
    """read lines of input file and creates lists with its elements in order to create Entry objects.
        INPUT: string with date (YYYY-MM-DD), time (hh:mm), energy production
                and wind speed; separated by whitespace. observations and predictions are
                differentiated by the nº of fields (4 in obs, 3 in preds)
        OUTPUT: list with the input fields as elements."""

    infile = ""

    def __init__(self, infile):

        self.infile = infile
        self.all_entries = []
        # list with all entries (observations + predictions)
        self.all_entries = self.readLines(self.infile)
        self.observations = [item for item in self.all_entries if len(
            item) == 4]  # filter observations
        self.predictions = [item for item in self.all_entries if len(
            item) == 3]  # filter predictions

    def readLines(self, infile):

        lines = [line.rstrip('\n') for line in open(
            infile)]    # lines to elements in list

        for line in lines:
            if (line == "observaciones") or (line == "predicciones"):
                continue

            self.all_entries.append(line.split(' '))

        return self.all_entries
