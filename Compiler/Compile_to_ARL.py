import Read_file

## Ensuring All symbols have the correct length to match the ARL style
def ARL_encoding(symbol):
    if symbol == 'RIGHT':
        return 'RIGHT'
    elif symbol == 'LEFT':
        return 'LEFT '
    elif symbol == 'STAY':
        return 'STAY '
    else:
        return symbol + "    "
    
def Convert_to_ARL(rules):
    translated_rules = []
    for rule in rules:
        rule_elms = Read_file.extract_elms_tape(rule)
        if len(rule_elms[1]) > 1:
            ## Move rule translation
            translated_rules.append(f"(({rule_elms[0]} . (SLASH . ({ARL_encoding(rule_elms[1])} . {rule_elms[-1]}))) .")
        else:
            ## Symbol rule translation
            translated_rules.append(f"(({rule_elms[0]} . ({ARL_encoding(rule_elms[1])} . ({ARL_encoding(rule_elms[2])} . {rule_elms[-1]}))) .")
    translated_rules.append("nil" + ")"*len(rules))
    return translated_rules 

file_name = "URTM.txt"
program = Read_file.read_file("1_Tape_programs/" + file_name)
ARL = Convert_to_ARL(program)
Read_file.write_file_newline("ARL-URTM.txt",ARL)