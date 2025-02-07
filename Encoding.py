import re


def Encode(program):
    translatedProgram = ""
    pattern = re.compile(r"\((\d+),\(\((.*?)\),\((.*?)\),\((.*?)\)\),(\d+)\)")
    for rule in program:
        match =  pattern.findall(rule)
        extracted = extract_groups(match[0])
        operation = EncodeLanguage(extracted[1]) + EncodeLanguage(extracted[2]) + EncodeLanguage(extracted[3])
        translatedProgram += "#" + extracted[0] + "#" + operation + '#' + extracted[4][::-1] + "#"
    return translatedProgram
   
def ToBinary(num: int):
    return bin(num)[2:]

def EncodeLanguage(d):
    if (d == "LEFT"):
        return "$$"
    elif (d == "RIGHT"):
        return "€€"
    else:
        return d
    
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
    