

alfa = ('0','1','b')
beta = ('0', '1', 'B', 'S', 'M', '#')

def expand_alfa(rule):
    expanded = []
    if 'alfa' in rule:
        for symbol in alfa:
            expanded.append(rule.replace('alfa', symbol))
    else:
        return [rule]
    return expanded
        
def expand_beta(rule):
    expanded = []
    if 'beta' in rule:
        for symbol in beta:
            expanded.append(rule.replace('beta', symbol))
    else:
        return [rule]
    return expanded
    
def expand_rules(rules):
    expanded_rules = []
    for rule in rules:
        for betas in expand_alfa(rule):
            expanded_rules.append(expand_beta(betas))
    return [rule for rules in expanded_rules for rule in rules]

example_rule_alfa = "(1,((alfa,alfa),(0,1),(0,0)),2)"
example_rule_beta = "(1,((0,0),(beta,beta),(0,0)),2)"
example_rule_alfaAndBeta = ["(1,((alfa,alfa),(beta,beta),(0,0)),2)"]

print(expand_rules(example_rule_alfaAndBeta))
print(len(expand_rules(example_rule_alfaAndBeta)))