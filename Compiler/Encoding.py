import re


def Encode(program):
    translatedProgram = ""
    for idx,rule in enumerate(program):
        if "LEFT" in rule or "RIGHT" in rule:
            move = EncodeMove(rule[1]) + EncodeMove(rule[2]) + EncodeMove(rule[3])
            translatedProgram += "M#" + ToBinary(int(rule[0])) + "#" + move + '#' + ToBinary(int(rule[4]))[::-1] + "#M"
        elif len(rule[1]) == 2 and len(rule[2]) == 2 and len(rule[3]) == 2:
            symbol = EncodeSymbol(rule[1]) + EncodeSymbol(rule[2]) + EncodeSymbol(rule[3])
            translatedProgram += "S#" + ToBinary(int(rule[0])) + "#" + symbol + '#' + ToBinary(int(rule[4]))[::-1] + "#S"
        else:
            raise Exception("The following rule is wrong: ", rule, idx)

    return translatedProgram
   
def ToBinary(num: int):
    return bin(num)[2:]

def EncodeSymbol(s):
    if s == 'b':
        return 'B'
    return s

def EncodeMove(d):
    if (d == "LEFT"):
        return "10"
    elif (d == "RIGHT"):
        return "01"
    elif (d == '__'):
        return d
    else:
        raise Exception("EncodeMove went wrong", d)
    
def extract_groups(groups):
    encoded = []
    for idx,group in enumerate(groups):
        if idx == 0 or idx == len(groups)-1:
            encoded.append(ToBinary(int(group)))
        elif group == '':
            encoded.append('__')
        else:
            encoded.append(group.replace(',',''))
    return encoded
