#### HARD CODED ####
start_state = 1 ### Always the start state
final_state = 0 ### Always the final state

def StateTransition(Rules, start, final):
    States = {}
    count = start_state
    for Rule in Rules:
        if not(Rule[0] in States): 
            States[Rule[0]] = count
            count += 1
    States[start] = start_state
    States[final] = final_state
    
    updated_Rules = []
    print
    for Rule in Rules:
        updated_Rules.append((States[Rule[0]], Rule[1], States[Rule[2]]))
    return updated_Rules

rules = [(2,"", 400),
        (400,"",3),
        (3,"",4),
        (3,"",400),
        (3,"",4),
        (4,"",100),
        (100,"",5),
        (100,"",4)]

print(StateTransition(rules, 2, 5))
    
        
