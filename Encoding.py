import re


def Encode(program):
    translatedProgram = ""
    pattern = re.compile(r"\((\d+),\(\((.*?)\),\((.*?)\),\((.*?)\)\),(\d+)\)")
    for idx,rule in enumerate(program):
        match =  pattern.findall(rule)
        extracted = extract_groups(match[0])
        if "LEFT" in extracted or "RIGHT" in extracted:
            move = EncodeMove(extracted[1]) + EncodeMove(extracted[2]) + EncodeMove(extracted[3])
            translatedProgram += "M#" + extracted[0] + "#" + move + '#' + extracted[4][::-1] + "#M"
        elif len(extracted[1]) == 2 and len(extracted[2]) == 2 and len(extracted[3]) == 2:
            symbol = EncodeSymbol(extracted[1]) + EncodeSymbol(extracted[2]) + EncodeSymbol(extracted[3])
            translatedProgram += "S#" + extracted[0] + "#" + symbol + '#' + extracted[4][::-1] + "#S"
        else:
            raise Exception("The following rule is wrong: ", rule, idx)
    return translatedProgram
   
def ToBinary(num: int):
    return bin(num)[2:]

def EncodeSymbol(s):
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

program = ["(0,((),(RIGHT),()),1)",
            "(1,((),(0,1),(1,2)),2)",
            "(1,((),(1,0),(1,2)),2)",
            "(1,((),(LEFT),()),2)"]

BinINC = ["(1,((),(B,B),(B,2)),2)",
        "(2,((),(RIGHT),()),3)",
        "(3,((),(0,1),()),4)",
        "(3,((),(1,0),()),2)",
        "(3,((),(B,B),()),4)",
        "(4,((),(LEFT),()),5)",
        "(5,((),(0,0),()),4)",
        "(5,((),(B,B),()),6)"]
print(Encode(BinINC))
    