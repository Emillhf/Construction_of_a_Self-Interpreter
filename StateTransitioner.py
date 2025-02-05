

def StateTransition(Rules):
    States = {}
    count = 1
    for Rule in Rules:
        if not(Rule[0] in States): 
            States[Rule[0]] = count
            count += 1
    States[Rules[-1][2]] = count
    
    updated_Rules = []
    for Rule in Rules:
        updated_Rules.append((States[Rule[0]], Rule[1], States[Rule[2]]))
    return updated_Rules

rules = [(1,"", 400),
        (400,"",3),
        (3,"",4),
        (3,"",400),
        (3,"",4),
        (4,"",100),
        (100,"",4),
        (100,"",6)]

print(StateTransition(rules))
    
        
