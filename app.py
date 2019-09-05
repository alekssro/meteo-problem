# import datetime
# import sys
from helpers import ReadLines
from helpers import Entry

infile = "Meteologica_vacante_ProgC_Problema_20190903/Meteologica_vacante_ProgC_ProblemaDatos_20190903.txt"

data = ReadLines(infile)

entry_try = Entry(data.predictions[1])

print(entry_try.date)
print(entry_try.time)
print(entry_try.energy_production)
print(entry_try.wind_speed)
