import time

print("start extraction of stats!")

start_time = time.time()

from .journals import *
from .persons import *
from .records import *

print("finished extraction after %s sec!" % round(time.time() - start_time, 2))
