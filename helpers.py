import datetime
import math

infile = "Meteologica_vacante_ProgC_Problema_20190903/Meteologica_vacante_ProgC_ProblemaDatos_20190903.txt"


class Entry:
    """store observation or prediction object with properties: date, energy production, wind speed.
        INPUT: string with date (YYYY-MM-DD), time (hh:mm), energy production
                and wind speed; separated by whitespace.
        OUTPUT: creates and object with the input fields as properties."""

    # define default variable values
    line = ""   # input string
    date = datetime.datetime.today()
    time = datetime.time()
    energy_production = None
    wind_speed = None
    list_fields = [date, time, energy_production, wind_speed]

    def __init__(self, list_fields):

        self.date = list_fields[0]
        self.time = list_fields[1]

        if len(list_fields) == 4:
            # save properties of observation Entry object
            self.energy_production = float(list_fields[2])
            self.wind_speed = float(list_fields[3])
            self.entry_type = "obs"

        elif len(list_fields) == 3:
            # save properties of prediction Entry object
            self.wind_speed = float(list_fields[2])
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
        self.predict_on_ord = self.sortPreds(predict_on, by="time")
        self.predict_on_ord = self.sortPreds(self.predict_on_ord, by="date")

        # Get predictions & errors
        self.predicts = self.predictDeming(fitted_model=self.fitted_model,
                                           predict_on=self.predict_on_ord)
        self.ema = self.calcEMA(observed=self.observations, predicted=self.predicts)  # Error Medio Absoluto
        self.ecm = self.calcECM(observed=self.observations, predicted=self.predicts)  # Error Cuadratico Medio

        # Write OUTPUT
        self.write2file(fitmodel=self.fitted_model, ema=self.ema, ecm=self.ecm, predictions=self.predicts)

    def fitDeming(self, observations, delta=1):
        """method to fit the Deming regression model.
            INPUT: array of 'Entry' objects corresponding to observations. option to choose delta.
            OUTPUT: array of floats with 2 elements; [0]: slope, [1]: intersect"""

        # intialize variables to calculate
        x_sum = 0
        y_sum = 0
        s_xx = 0
        s_xy = 0
        s_yy = 0
        N = len(observations)

        # calculate estimates of x and y
        for obs in observations:
            x_sum += obs.wind_speed
            y_sum += obs.energy_production
        x_est = x_sum / N
        y_est = y_sum / N

        # calculate s values
        for obs in observations:
            s_xx += ((obs.wind_speed - x_est) ** 2)
            s_xy += ((obs.wind_speed - x_est) * (obs.energy_production - y_est))
            s_yy += ((obs.energy_production - y_est) ** 2)
        s_xx = (s_xx / (N-1))
        s_xy = (s_xy / (N-1))
        s_yy = (s_yy / (N-1))

        print(x_est, y_est, N, s_xx, s_xy, s_yy)

        # calculate slope (beta_0) and intersect (beta_1)
        beta_1 = (s_yy - delta * s_xx + math.sqrt((s_yy - delta * s_xx) ** 2 + 4 * delta * (s_xy) ** 2)) / (2 * s_xy)
        beta_0 = y_est - beta_1 * x_est

        return [beta_1, beta_0]

    def predictDeming(self, fitted_model, predict_on):
        """method to generate predictions for each 'Entry' prediction object using the Deming model
            INPUT: fitted_model, array with slope and intersect as elements
                   predict_on, array with 'Entry' objects for which predictions will be made
            OUTPUT: array of floats with predicted energy production values for each entry"""

        predicted = []

        for pred in predict_on:
            p = fitted_model[0] * pred.wind_speed + fitted_model[1]
            # if a prediction is negative, substitute by 0 (not possible to produce negative energy)
            if p < 0:
                p = 0

            predicted.append(p)

        return predicted

    def sortPreds(self, preds, by="date"):
        """method to sort the predictions by date and time. option to choose field to sort by:
                ('date', 'time', 'energy_production', 'wind_speed')
            INPUT: array of 'Entry' objects to be sorted.
            OUTPUT: array of ordered 'Entry' objects."""

        if by == "date":
            sortedPreds = sorted(preds,
                    key=lambda x: datetime.datetime.strptime(x.date, '%Y-%m-%d'), reverse=False)
        elif by == "time":
            sortedPreds = sorted(preds,
                    key=lambda x: datetime.datetime.strptime(x.time, '%H:%M'), reverse=False)
        elif by == "energy_production":
            sortedPreds = sorted(preds,
                    key=lambda x: x.energy_production, reverse=False)
        elif by == "wind_speed":
            sortedPreds = sorted(preds,
                    key=lambda x: x.wind_speed, reverse=False)
        else:
            return preds

        return sortedPreds

    def write2file(self, fitmodel, ema, ecm, predictions):
        pass


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
