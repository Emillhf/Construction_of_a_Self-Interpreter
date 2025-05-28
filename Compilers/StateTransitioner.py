import re
#### HARD CODED ####
start_state = "1" ### Always the start state
final_state = "0" ### Always the final state

def StateTransition(rules, start : str, final : str):
    pattern = re.compile(r"\((\d+)(,\(\(.*?\),\(.*?\),\(.*?\)\),)(\d+)\)")
    States = {}
    count = 2
    States[start] = start_state
    States[final] = final_state
    for rule in rules:
        match =  (pattern.findall(rule))[0]
        if not(match[0] in States): 
            States[match[0]] = count
            count += 1    
    updated_Rules = []
    for rule in rules:
        match =  (pattern.findall(rule))[0]
        updated_Rules.append("(" + str(States[match[0]]) + match[1] + str(States[match[2]]) + ")\n")
    sorted_rules= sorted(updated_Rules, key=lambda x: x[0])

    return sorted_rules