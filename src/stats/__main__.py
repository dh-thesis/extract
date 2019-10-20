import time

from . import journals
from . import persons
from . import records

print("start extraction of stats!")

start_time = time.time()

journals.routine()
persons.routine()
records.routine()

print("finished extraction after %s sec!" % round(time.time() - start_time, 2))
