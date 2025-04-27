
def Invert_Move(rule):
    result = []
    for elm in rule:
        if elm == "RIGHT":
            result.append("(LEFT)")
        elif elm == "LEFT":
            result.append("(RIGHT)")
        else:
            result.append("(STAY)")
    return result
            
def Invert_1_tape(rules):
    for idx, rule in enumerate(rules):
        rule = rule.split(",")
        rule = [(elm.replace('(', '')).replace(')','') for elm in rule]
        rule[0], rule[-1] = rule[-1], rule[0]
        if len(rule) == 3:
            move_inverted = Invert_Move(rule[1:-1])
            rules[idx] = f"({rule[0]},{move_inverted[0]},{rule[-1]})"
        else:
            rule[1], rule[2] = rule[2], rule[1]
            rules[idx] = f"({rule[0]},({rule[1]},{rule[2]}),{rule[-1]})".replace("'", '')
    return rules

name = input()
file = open("1_Tape_programs/" + name, 'r')
lines = file.readlines()
lines = [line.strip() for line in lines]
inverted = Invert_1_tape(lines)
outfile = open("1_Tape_programs/rev_" + name,'w+')
for elm in inverted:
    outfile.write(elm + "\n")