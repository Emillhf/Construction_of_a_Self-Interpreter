
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
            rules[idx] = f"({rule[0]},({rule[1],rule[2]},{rule[3],rule[4]},{rule[5],rule[6]}),{rule[-1]})".replace("'", '')
    return rules


example = ["(1,((alfa,alfa),(#,#),(#,b)),2)",
        "(2,((STAY),(RIGHT),(RIGHT)),3)",
        "(3,((alfa,alfa),(#,#),(#,b)),0)",
        "(3,((alfa,alfa),(beta,beta),(beta,b)),2)"]

print(Invert(example))