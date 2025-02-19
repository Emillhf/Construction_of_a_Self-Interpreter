
def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

def Expand_macros(rules: str):
    
    for idx, rule in enumerate(rules):
        if "#load" in rule:
            res = []
            macro = rule.split(" ")[1]
            filename = macro.split("(")[0]
            first_state, last_state = macro.split("(")[1].strip(")").split(",")
            file = open("Compiler/macros/" + filename + ".txt")
            lines = file.readlines()
            for line in lines:
                if "#load" in line:
                    res.append(Expand_macros([line]))
                else:
                    line = line.strip()     
                    linesplit = line.split(",")  
                    first_state_rule = linesplit[0].strip("(") 
                    last_state_rule = linesplit[-1].strip(")") 
                    linesplit[0] = str(int(first_state_rule) + int(first_state)-1)
                    if (last_state_rule != "0"):
                        linesplit[-1] = str(int(last_state_rule) + int(first_state)-1)
                    else:
                        linesplit[-1] = str(int(last_state_rule) + int(last_state))
                    res.append("(" + ",".join(linesplit) + ")")
                # print(first_state,last_state,linesplit) 
            rules[idx] = res
    return flatten(rules)

test = ["#load clear_state(1,4)",
        "#load write_state(4,11)"]