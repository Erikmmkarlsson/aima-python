from csp import *

australia_csp = MapColoringCSP(list('RGB'), """SA: WA NT Q NSW V; NT: WA Q; NSW: Q V; T: """)

schedule_csp = MapColoringCSP(list('RGB'), """L1: L2 L3 L4; L2: L3; L3: L4 L5 L6; L4: L5 L6; L5: ; L6: L7; L7: """)


print(backtracking_search(schedule_csp, inference=forward_checking))
