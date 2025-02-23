
def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

def Expand_macros(rules: str):
    for idx, rule in enumerate(rules):
        if "#load" in rule:
            macro = rule.split(" ")[1]
            filename = macro.split("(")[0]
            states = macro.split("(")[1].replace(")","").strip().split(",")
            if (len(states) == 2): #(start_state, final_state)
                rules[idx] = generel_expand(filename,states)
            elif (len(states) == 3): #(start_state, true_state, false_state)
                rules[idx] = condititional_expand(filename,states)
            else:
                print(f"Error, wrong macro input {states}, in rule {rule}")
                exit(1)
                
    return flatten(rules)

test = ["#load clear_state(1,4)",
        "#load write_state(4,11)"]


def generel_expand(filename : str, states : list[int]):
    res = []
    first_state, last_state = states
    file = open("Compiler/macros/" + filename + ".txt")
    lines = file.readlines()
    for line in lines:
        if "#load" in line:
            res.append(Expand_macros([line]))
        else:
            linesplit = line.strip().split(",")  
            first_state_rule = linesplit[0].replace("(","")
            last_state_rule = linesplit[-1].replace(")","")
            linesplit[0] = str(int(first_state_rule) + int(first_state)-1)
            if (last_state_rule == "0"):
                linesplit[-1] = last_state
            else:
                linesplit[-1] = str(int(last_state_rule) + int(first_state)-1)
            res.append("(" + ",".join(linesplit) + ")")
    return res
            

def condititional_expand(filename : str, states : list[int]):
    res = []
    first_state, true_state, false_state = states
    file = open("Compiler/macros/" + filename + ".txt")
    lines = file.readlines()
    for line in lines:
        if "#load" in line:
            res.append(Expand_macros([line]))
        else:
            linesplit = line.strip().split(",")  
            first_state_rule = linesplit[0].replace("(","")
            last_state_rule = linesplit[-1].replace(")","")
            linesplit[0] = str(int(first_state_rule) + int(first_state)-1) 
            if (last_state_rule == "0"):
                linesplit[-1] = true_state
            elif (last_state_rule == "-1"):
                linesplit[-1] = false_state
            else:
                linesplit[-1] = str(int(last_state_rule) + int(first_state)-1)
            res.append("(" + ",".join(linesplit) + ")")
    return res