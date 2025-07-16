
encoded_symbols = {
    'B': 'P',
    'b': 'p',
    '#': 'H',
    '0': 'O',
    '1': 'I',
    'S': 'Z',
    'M': 'W'
}

alfa = ['0', '1', 'B', '#', 'S', 'M','b','P','p','H','O','I','Z','W','$']
alfa_doller_removed = ['0', '1', 'B', '#', 'S', 'M','b','P','p','H','O','I','Z','W']
alfa_b_removed = ['0', '1', 'B', '#', 'S', 'M','P','p','H','O','I','Z','W','$']
alfa_p_removed = ['0', '1', 'B', '#', 'S', 'M','b','P','H','O','I','Z','W','$']
gamma = ['P','p','H','O','I','Z','W']
alfa_gamma_removed = [symbol for symbol in alfa if symbol not in gamma]
example = (1,('b','b'),2)

def expand(rules):
    expanded_rules = []
    for rule in rules:
        start = rule[0]
        final = rule[-1]
        if rule[1] == ('alfa','gamma'):
            for alfa_elm, gamma_elm in encoded_symbols.items():
                expanded_rules.append((start,(alfa_elm,gamma_elm),final))
        elif rule[1] == ('gamma','alfa'):
            for alfa_elm, gamma_elm in encoded_symbols.items():
                expanded_rules.append((start,(gamma_elm,alfa_elm),final))
        elif rule[1] == ('alfa','alfa'):
            for alfa_elm in alfa:
                expanded_rules.append((start,(alfa_elm,alfa_elm),final))
        elif rule[1] == ('gamma','gamma'):
            for gamma_elm in gamma:
                expanded_rules.append((start,(gamma_elm,gamma_elm),final))
        elif rule[1] == ('alfa','alfa'):
            for alfa_elm in alfa:
                expanded_rules.append((start,(alfa_elm,alfa_elm),final))
        elif rule[1] == ('alfa!=(gamma)','alfa!=(gamma)'):
            for alfa_elm in alfa_gamma_removed:
                expanded_rules.append((start,(alfa_elm,alfa_elm),final))
        elif rule[1] == ('alfa!=($)','alfa!=($)'):
            for alfa_elm in alfa_doller_removed:
                expanded_rules.append((start,(alfa_elm,alfa_elm),final))
        elif rule[1] == ('alfa!=(b)','alfa!=(b)'):
            for alfa_elm in alfa_b_removed:
                expanded_rules.append((start,(alfa_elm,alfa_elm),final))
        elif rule[1] == ('alfa!=(p)','alfa!=(p)'):
            for alfa_elm in alfa_b_removed:
                expanded_rules.append((start,(alfa_elm,alfa_elm),final))
        else:
            expanded_rules.append(rule)
    return expanded_rules
            