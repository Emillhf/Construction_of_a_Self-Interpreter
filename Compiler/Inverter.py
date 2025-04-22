import re
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

def Invert_1Tape_move(move):
    if move == '"(RIGHT)"':
        return ("(LEFT)")
    elif move == '"(LEFT)"':
        return ("(RIGHT)")
    else:
        return ("(STAY)")

            
def Invert(rules):
    for idx, rule in enumerate(rules):
        rule = rule.split(",")
        rule = [(elm.replace('(', '')).replace(')','') for elm in rule]
        rule[0], rule[-1] = rule[-1], rule[0]
        if len(rule) == 5:
            move_inverted = Invert_Move(rule[1:-1])
            rules[idx] = f"({rule[0]},({move_inverted[0]},{move_inverted[1]},{move_inverted[2]}),{rule[-1]})"
        else:
            rule[1], rule[2] = rule[2], rule[1]
            rule[3], rule[4] = rule[4], rule[3]
            rule[5], rule[6] = rule[6], rule[5]
            rules[idx] = f"({rule[0]},(({rule[1]},{rule[2]}),({rule[3]},{rule[4]}),({rule[5]},{rule[6]})),{rule[-1]})".replace("'", '')
    return rules

def Invert1Tape(rules):
    for idx, rule in enumerate(rules):
        if (rule == ""):
            continue
        rule = rule.split(",")
        rule[0] = rule[0].replace("(","")
        rule[-1] = rule[-1].replace(")","")
        
        rule[0], rule[-1] = rule[-1], rule[0]
        if len(rule) == 3:
            # rule[1] = rule[1][1:-1]
            move_inverted = Invert_1Tape_move(rule[1])
            rules[idx] = f'tmp.append(({rule[0]},"{move_inverted}",{rule[-1]}))'
        else:
            rule[1] = rule[1][1::]
            rule[2] = rule[2][:-1]

            rule[1], rule[2] = rule[2], rule[1]
            rules[idx] = f"tmp.append(({rule[0]},({rule[1]},{rule[2]}),{rule[-1]}))".replace("'", '')
    return rules

def AddNumToCount(num, rules):
    for idx, rule in enumerate(rules):
        if (rule == ""):
            continue        
        match = re.findall("count\+\d+",rule)
        start_state = str(int(match[0][6:])+num)
        final_state = str(int(match[1][6:])+num)
        rule = rule.split(",")
        rule[0] = start_state
        rule[-1] = final_state
        if len(rule) == 3:
            rules[idx] = f'tmp.append((count+{rule[0]},{rule[1]},count+{rule[-1]}))'
        else:
            rules[idx] = f"tmp.append((count+{rule[0]},{rule[1]},{rule[2]},count+{rule[-1]}))".replace("'", '')
    return rules
# name = input()
# file = open("1_Tape_programs/" + name, 'r')
# lines = file.readlines()
# lines = [line.strip() for line in lines]
# inverted = Invert1Tape(lines)
# outfile = open("1_Tape_programs/" + "rev_" + name,'w+')
# for elm in inverted:
#     outfile.write(elm + "\n")
    
name = "move_right_file.txt"
file = open(name, 'r')
lines = file.readlines()
lines = [line.strip().replace("tmp.append","") for line in lines]
inverted = Invert1Tape(lines)
# updated_states = AddNumToCount(70,inverted)
# outfile = open( "rev_" + name,'w+')
for elm in inverted:
    print(elm )
    
