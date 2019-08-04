import time

print("start extraction!")

start_time = time.time()

# //////////////// #
# /// CONTEXTS /// #
# //////////////// #

from .data_ctx import *
from .data_ctx_mpis import *

# ///////////////////// #
# /// ORGANIZATIONS /// #
# ///////////////////// #

from .data_ous import *
from .data_ous_mpis import *

# /////////////// #
# /// PERSONS /// #
# /////////////// #

from .data_pers import *

# /////////////////// #
# /// DESCRIPTION /// #
# /////////////////// #

from .data_desc import *

# ///////////////// #
# /// LANGUAGES /// #
# ///////////////// #

from .data_lang import *

# //////////////// #
# /// JOURNALS /// #
# //////////////// #

from .data_jour import *

# ///////////// #
# /// ITEMS /// #
# ///////////// #

# from .data_items import *

# ///////////// #

print("finished extraction after %s sec!" % round(time.time() - start_time, 2))
