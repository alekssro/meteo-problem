import datetime
import math

class Entry:
    """store observation or prediction object with properties: date, energy production, wind speed.
        INPUT: string with date (YYYY-MM-DD), time (hh:mm), energy production
                and wind speed; separated by whitespace.
        OUTPUT: creates and object with the input fields as properties."""

    # define default variable values
    line = ""   # input string
    date_time = datetime.datetime.today()
    energy_production = None
    wind_speed = None
    list_fields = [date_time, energy_production, wind_speed]

    def __init__(self, list_fields):

        self.date_time = list_fields[0] + " " + list_fields[1]

        # save date and time as datetime type
        self.date_time = datetime.datetime.strptime(list_fields[0] + " " + list_fields[1],
                                                    '%Y-%m-%d %H:%M')

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
        INPUT: 2 lists of 'Entry' objects: (1) to be modelled and (2) to predict on
        OUTPUT: a text file which contains the slope and intersect values in the first line, the month
                and the 2 errors made as second line and the prediction of energy production (one per
                prediction entry)"""

    fitted_model = [0, 0]
    observations = []   # array of observations as Entry objects
    predict_on = []
    slope = 0
    intersect = 0

    def __init__(self, observations, predict_on):

        self.observations = observations    # array of Entry objects used to fit the model
        self.predict_on = predict_on

        # Order Entry arrays by 'time' and then 'date'
        # Sort observations
        self.observations = self.sortPreds(self.observations, by="date_time")
        # Sort elements to predict on
        self.predict_on = self.sortPreds(self.predict_on, by="date_time")

        # Save energy production and wind speed as float arrays
        self.y_observed = [obs.energy_production for obs in self.observations]  # store observed energy_production values
        self.x_observed = [obs.wind_speed for obs in self.observations]         # store observed wind_speed values
        self.x_predict = [pred.wind_speed for pred in self.predict_on]          # store to-predict wind_speed values

        # Fit Deming regression model and save slope and intersect as properties of the Model
        self.fitted_model = self.fitDeming(observations)
        self.slope = self.fitted_model[0]
        self.intersect = self.fitted_model[1]

        # Get predictions and save them as properties
        self.y_predicted = self.predictDeming(self.fitted_model, self.x_predict)
        for i in range(len(self.predict_on)):
            self.predict_on[i].energy_production = self.y_predicted[i]

        # # Get array with energy_production observed values
        # self.ep_observed = [obs.energy_production for obs in observations]
        #
        # self.ema_total = self.calcEMA(observed=self.ep_observed, predicted=self.ep_predicted)  # Error Medio Absoluto
        # self.ecm_total = self.calcECM(observed=self.ep_observed, predicted=self.ep_predicted)  # Error Cuadratico Medio

        # Write OUTPUT
        # self.write2file(fitmodel=self.fitted_model, ema=self.ema, ecm=self.ecm, predictions=self.ep_predicted)

    def calcEMA(self, observed, predicted):
        """method to calculate Mean Absolute Error (método para calcular Error Medio Absoluto)
            Re-implemented in python from ema.hpp source code file.
           INPUT: array of floats with observations and other array corresponding
                  to predictions
           OUTPUT: (float) percentage MAE/EMA"""

        error_acumulado = 0
        observacion_total = 0

        # observations and predictions should be same lenght
        if len(observed) != len(predicted):
            return 100

        for i in range(len(observed)):
            error_acumulado += abs(observed[i] - predicted[i])
            observacion_total += observed[i]

        if observacion_total < 1e-7:
            return 0

        ema = (error_acumulado / observacion_total) * 100

        return ema

    def calcECM(self, observed, predicted):
        """method to calculate Mean Cuadratic Error (método para calcular Error Cuadratico Medio)
           INPUT: 2 float arrays corresponding to (1) observations and (2) predictions
           OUTPUT: (float) percentage MCE/ECM"""
        error_cuadratico = 0
        observacion_total = 0
        n = len(observed)

        # observations and predictions should be same lenght
        if len(observed) != len(predicted):
            return 100

        for i in range(len(observed)):
            error_cuadratico += ((observed[i] - predicted[i]) ** 2)
            observacion_total += observed[i]

        if observacion_total < 1e-7:
            return 0

        ecm = ((100 * n) / observacion_total) * math.sqrt((error_cuadratico / n))

        return ecm

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

        # calculate slope (beta_1) and intersect (beta_0)
        beta_1 = (s_yy - delta * s_xx + math.sqrt((s_yy - delta * s_xx) ** 2 + 4 * delta * (s_xy) ** 2)) / (2 * s_xy)
        beta_0 = y_est - beta_1 * x_est

        return [beta_1, beta_0]

    # def groupByMonth(self, x):
    #     """method that devides the Entry elements in x by month
    #     INPUT: x, array of Entry objects
    #     OUTPUT: dictionary (key = month; value = array of Entry objects corresponding to that month)"""
    #
    #     grouped = defaultdict(list)
    #
    #     for k, v in x:
    #         grouped[k].append(v)
    #
    #     return grouped.items()

    def predictDeming(self, fitted_model, x):
        """method to generate predictions for each 'Entry' prediction object using the Deming model
            INPUT: fitted_model, array with slope and intersect as elements
                   x, array with floats corresponding to wind_speed; used to make predictions
            OUTPUT: array of floats with predicted energy production values for each entry."""

        predicted = []

        for pred in x:
            p = fitted_model[0] * pred + fitted_model[1]

            # if a prediction is negative, substitute by 0 (not possible to produce negative energy)
            if p < 0:
                p = 0

            predicted.append(float(p))  # array to return predictions as float

        return predicted

    def sortPreds(self, preds, by="date_time"):
        """method to sort the predictions by date and time. option to choose field to sort by:
                ('date_time', 'energy_production', 'wind_speed')
            INPUT: array of 'Entry' objects to be sorted.
            OUTPUT: array of ordered 'Entry' objects."""

        if by == "date_time":
            sortedPreds = sorted(preds,
                    key=lambda x: x.date_time.strftime('%Y-%m-%d %H:%M'), reverse=False)
        # datetime.datetime.strptime(str(x.date_time), '%Y-%m-%d %H:%M'), reverse=False)
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
        INPUT: file path with multiple lines. In each line, information of date (YYYY-MM-DD),
            time (hh:mm), energy production and wind speed; separated by whitespaces. observations
            and predictions are differentiated by the nº of fields (4 in obs, 3 in preds)
        OUTPUT: list with the input fields as elements."""

    infile = ""

    def __init__(self, infile):

        self.infile = infile
        self.all_entries = []
        # list with all entries (observations + predictions)
        self.all_entries = self.readLines(self.infile)
        self.observations = [item for item in self.all_entries if len(item) == 4]  # filter observations
        self.predictions = [item for item in self.all_entries if len(item) == 3]  # filter predictions

    def readLines(self, infile):

        lines = [line.rstrip('\n') for line in open(infile)]    # lines to elements in list

        for line in lines:
            if (line == "observaciones") or (line == "predicciones"):
                continue

            self.all_entries.append(line.split(' '))

        return self.all_entries
