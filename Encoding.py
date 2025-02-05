import re

def Encode(program):
    translatedProgram = ""
    pattern = re.compile(r"\((\d+),\(\((.*?)\),(.*?)\,(.*?)\),(\d+)\)")
    for rule in program:
        match =  pattern.match(rule)
        if match.group(2)[1] == "," or match.group(3)[1] == "," or match.group(4)[1] == ",":
            symbol = EncodeSymbol(match.group(2)[0]) + EncodeSymbol(match.group(2)[2])
            translatedProgram += "S#" + ToBinary(match.group(1)) + "#" + symbol + "#" + ToBinary(match.group(5)[::-1])

            
        
        
def ToBinary(num: int):
    return bin(num)[2:]

def EncodeSymbol(s):
    
    return s

def EncodeMove(d):
    if (d == "LEFT"):
        return "10"
    elif (d == "RIGHT"):
        return "01"
    
    else:
        raise Exception("ENcodeMove went wrong", d)
    