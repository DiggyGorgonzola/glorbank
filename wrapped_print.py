import builtins
import inspect
import os
from CBI import cbidict
active = cbidict["debug"][0]
_original_print = print

def wrapped_print(*args, **kwargs):
    if active:
        if inspect.stack()[1].function != "<module>":
            _original_print(f"\033[1m{os.path.basename(inspect.stack()[1].filename)}.{inspect.stack()[1].function} says  \033[0m", *args, **kwargs)
        else:
            _original_print(f"\033[1m{os.path.basename(inspect.stack()[1].filename)} says  \033[0m", *args, **kwargs)
        _original_print("\n")
    else:
        if inspect.stack()[1].function != "<module>":
            _original_print(f"\033[1m{os.path.basename(inspect.stack()[1].filename)}.{inspect.stack()[1].function} says a secret\033[0m")
        else:
            _original_print(f"\033[1m{os.path.basename(inspect.stack()[1].filename)} says a secret\033[0m")
        _original_print("\n")

builtins.print = wrapped_print