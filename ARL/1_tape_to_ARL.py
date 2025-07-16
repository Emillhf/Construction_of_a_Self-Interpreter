import Read_file
import sys

## Ensuring All symbols have the correct length to match the ARL style
def ARL_encoding(symbol):
    if symbol == 'RIGHT':
        return 'RIGHT'
    elif symbol == 'LEFT':
        return 'LEFT '
    elif symbol == 'STAY':
        return 'STAY '
    elif symbol == 'b':
        return 'BLANK'
    else:
        return symbol + "    "
    
def Convert_to_ARL(rules):
    translated_rules = []
    for rule in rules:
        rule_elms = Read_file.extract_elms_tape(rule)
        if len(rule_elms[1]) > 1:
            ## Move rule translation
            translated_rules.append(f"  (({rule_elms[0]} . (SLASH . ({ARL_encoding(rule_elms[1])} . {rule_elms[-1]}))) .")
        else:
            ## Symbol rule translation
            translated_rules.append(f"  (({rule_elms[0]} . ({ARL_encoding(rule_elms[1])} . ({ARL_encoding(rule_elms[2])} . {rule_elms[-1]}))) .")
    translated_rules.append("nil" + ")"*len(rules))
    return translated_rules 

### Convert b to Blank
def Convert_to_Blank(symbol):
    if symbol == 'b':
        return 'BLANK'
    return symbol

def Convert_tape(tape):
    translated_tape = "("
    for idx, symbol in enumerate(tape):
        if idx == len(tape)-1:
            translated_tape += (Convert_to_Blank(symbol) + " . nil")
        else:
            translated_tape +=  (Convert_to_Blank(symbol) + " . (")
    translated_tape += ")"*len(tape)
    return translated_tape

path, file_name = Read_file.input_file()
output = "ARL/ARL-" + file_name
start = "Start = '31"
end = "End = '1"
rules = "Rules ='"
added_space = "\n\n// Tape for full specialization"
tape_variable = "S_right = '"
tape = "$I$I$I$"
program = Read_file.read_file("1_Tape_programs/" + file_name)


ARL = [start] + [end] + [rules] + Convert_to_ARL(program) + [added_space] + [tape_variable + Convert_tape(tape)]
Read_file.write_to_file(output.replace('.txt','.spec'),ARL)
