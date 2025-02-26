import re

alfa = ['0', '1', 'b']
beta = ['0', '1', 'b', '#']

def expand_alfa(rule, alfa_current = alfa):
    expanded = []
    if 'alfa' in rule:
        for symbol in alfa_current:
            expanded.append(rule.replace('alfa', symbol))
    else:
        return [rule]
    return expanded
        
def expand_beta(rule, beta_current = beta):
    expanded = []
    if 'beta' in rule:
        for symbol in beta_current:
            expanded.append(rule.replace('beta', symbol))
    else:
        return [rule]
    return expanded

def remove_duplicates(list1,list2):
    return [elm for elm in list1 if elm not in list2]

def restricted_expand(rule,alfa,beta):
    restricted_alfas = set()
    restricted_betas = set()
    if '!=' in rule:
        pattern = r'\b\w+!=\([^)]+\)'
        matches = re.findall(pattern, rule)
        if len(matches) > 0:
            pattern = r'\w+!=\(([^()]+)\)'
            for match in matches:
                removed = re.findall(pattern, match)[0].split(',')
                if 'alfa' in match:
                    restricted_alfas = restricted_alfas.union(set(removed))
                elif 'beta' in match:
                    restricted_betas = restricted_betas.union(set(removed))
                else:
                    raise ValueError("Something wrong in restriction")
    return remove_duplicates(alfa,list(restricted_alfas)), remove_duplicates(beta,list(restricted_betas))

def remove_equals(rule):
    if '!=' in rule:
        pattern = r'!=\([^)]+\)'
        matches = re.findall(pattern, rule)
        for match in set(matches):
            rule = rule.replace(match,'')
    return rule
    
def expand_rules(rules,alfa,beta):
    expanded_rules = []
    for rule in rules:
        removed_alfas, removed_beta = restricted_expand(rule,alfa,beta)
        rule = remove_equals(rule)
        for betas in expand_alfa(rule,removed_alfas):
            expanded_rules.append(expand_beta(betas,removed_beta))
    return [rule for rules in expanded_rules for rule in rules]

example_rule_alfa = "(1,((alfa,alfa),(0,1),(0,0)),2)"
example_rule_beta = "(1,((0,0),(beta,beta),(0,0)),2)"
example_rule_alfaAndBeta = ["(1,((alfa,alfa),(beta,beta),(0,0)),2)"]
example_rule_alfaAndBeta = ["(1,((alfa!=(b,1),alfa!=(b,1)),(beta!=(M),beta!=(M)),(0,0)),2)"]
