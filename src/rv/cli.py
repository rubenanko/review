from rv.modules import call_module
from typing import List
from rv.core.exceptions import make_safe
import sys

def main()->None:
    argv = sys.argv
    module = argv[1]
    
    if module == "f":   module = "functions"
    elif module == "s":   module = "show"
    
    call_module_safely = make_safe(call_module)

    if len(argv) == 1 or argv[1] == "--help":
        call_module_safely("help",[])
    else:
        call_module_safely(module,argv[2:])

if __name__ == "__main__":
    main()
