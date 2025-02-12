import re
#### HARD CODED ####
start_state = 1 ### Always the start state
final_state = 0 ### Always the final state

def StateTransition(Rules, start : str, final : str):
    pattern = re.compile(r"\((\d+),\(\((.*?)\),\((.*?)\),\((.*?)\)\),(\d+)\)")
    States = {}
    count = start_state
    for rule in Rules:
        match =  pattern.findall(rule)
        extracted = extract_groups(match[0])
        if not(extracted[0] in States): 
            States[extracted[0]] = count
            count += 1
    States[start] = start_state
    States[final] = final_state
    
    updated_Rules = []
    for rule in Rules:
        match =  pattern.findall(rule)
        extracted = extract_groups(match[0])
        updated_Rules.append((States[extracted[0]], extracted[1], extracted[2], extracted[3], States[extracted[4]]))
    return updated_Rules


def extract_groups(groups):
    encoded = []
    for idx,group in enumerate(groups):
        if idx == 0 or idx == len(groups)-1:
            encoded.append(group)
        elif group == '':
            encoded.append('__')
        else:
            encoded.append(group.replace(',',''))
    return encoded
    
        
