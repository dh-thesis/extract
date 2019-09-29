import time

print("start extraction of graph!")

start_time = time.time()

# //////////////// #
# /// CONTEXTS /// #
# //////////////// #

from .contexts import *
from .contexts_mpis import *

# ///////////////////// #
# /// ORGANIZATIONS /// #
# ///////////////////// #

from .ous import *
from .ous_mpis import *

# /////////////// #
# /// PERSONS /// #
# /////////////// #

from .persons import *

# /////////////////// #
# /// DESCRIPTION /// #
# /////////////////// #

from .descriptor import *

# ///////////////// #
# /// LANGUAGES /// #
# ///////////////// #

from .languages import *

# //////////////// #
# /// JOURNALS /// #
# //////////////// #

from .journals import *


# ///////////// #

print("finished extraction after %s sec!" % round(time.time() - start_time, 2))
