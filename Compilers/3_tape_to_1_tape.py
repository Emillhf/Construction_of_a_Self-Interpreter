import re
import os
import sys
import Expand_1_tape
import Inverter
import Read_file

encoded_symbols = {
    'B': 'P',
    'b': 'p',
    '#': 'H',
    '0': 'O',
    '1': 'I',
    'S': 'Z',
    'M': 'W',
}
    
def groupByStates(rules:list[str]):
    pattern = re.compile(r"\((\d+),\((\(.*?\)),(\(.*?\)),(\(.*?\))\),(\d+)\)")
    states = {}
    for rule in rules:
        match =  (pattern.findall(rule))
        state = match[0][0]
        if state in states.keys():
            states[state].append(match[0])
        else:
            states[state] = match
    return list(states.values())

def inner_list(rules,tape):
    tape_dict = {}
    for rule in rules:
        tape_elm = rule[tape]
        if tape_elm in tape_dict.keys():
            tape_dict[tape_elm].append(rule)
        else:
            tape_dict[tape_elm] = [rule]
    return list(tape_dict.values())
        
def groupByTape1(state_rules):
    final = []
    for grouped_rules in state_rules:
        temp = []
        for rules in grouped_rules:
            temp.append(inner_list(rules,1))
        final.append(temp)

    return final

def groupByTape2(state_rules):
    final = []
    for rules in state_rules:
        final.append(inner_list(rules,2))
            
    return final

def groupByTape3(state_rules):
    final = []
    for grouped_rules in state_rules:
        temp1 = []
        for grouped_by_tape_1 in grouped_rules:
            temp2 = []
            for rules in grouped_by_tape_1:
                temp2.append(inner_list(rules,3))
            temp1.append(temp2)
        final.append(temp1)
    return final

def Replace_final_state(rules,updated_value):
    for idx,rule in enumerate(rules):
        if rule[-1] == 0:
            rule = list(rule)   
            rule[-1] = updated_value
            rules[idx] = tuple(rule)
        if rule[0] == 0:
            rule = list(rule)   
            rule[0] = updated_value
            rules[idx] = tuple(rule)
    return rules

def Expand_symbol_top_tree(states,count,states_dict,connection_dict):
    tmp = []
    start_state = states[0][0][0][0][0]
    if not(start_state in states_dict.keys()):
        states_dict[start_state] = count
    for tape2 in states:
        tape2_elm = tape2[0][0][0][2]
        count+=1
        tmp.append((states_dict[start_state],((encoded_symbols[tape2_elm[1]],encoded_symbols[tape2_elm[3]])),count))  
        count_tape2 = count
        count += 1
        tmp.append((count_tape2,"(LEFT)",count_tape2+1)) 
        tmp.append((count_tape2+1,("alfa!=(gamma)","alfa!=(gamma)"),count_tape2))      
        for tape1 in tape2:
            count +=1
            tape1_elm = tape1[0][0][1]

            tmp.append((count_tape2+1,((encoded_symbols[tape1_elm[1]]),encoded_symbols[tape1_elm[3]]),count))    
            count_tape1 = count
            
            tmp.append((count_tape1,"(RIGHT)",count_tape1+1)) 
            tmp.append((count_tape1+1,("alfa!=(gamma)","alfa!=(gamma)"),count_tape1))  

            tmp.append((count_tape1+1,((encoded_symbols[tape2_elm[3]],encoded_symbols[tape2_elm[3]])),count_tape1+2))  

            tmp.append((count_tape1+2,"(RIGHT)",count_tape1+3)) 
            tmp.append((count_tape1+3,("alfa!=(gamma)","alfa!=(gamma)"),count_tape1+2))    
            
            count += 4
            for tape3 in tape1:
                tape3_elm = tape3[0][3]
                connection_dict[tape3[0]] = count
                tmp.append((count_tape1+3,((encoded_symbols[tape3_elm[1]],encoded_symbols[tape3_elm[3]])),count))  
        count+=1
    return tmp, count, states_dict, connection_dict

def Expand_symbol_bottom_tree(states,count,states_dict,connection_dict):
    tmp = []
    start_state = states[0][0][0][0][0]
    if not(start_state in states_dict.keys()):
        states_dict[start_state] = count
    for tape2 in states:
        tape2_elm = tape2[0][0][0][2]
        count+=1
        tmp.append((states_dict[start_state],((encoded_symbols[tape2_elm[1]],encoded_symbols[tape2_elm[1]])),count))  
        count_tape2 = count
        count += 1
        tmp.append((count_tape2,"(LEFT)",count_tape2+1)) 
        tmp.append((count_tape2+1,("alfa!=(gamma)","alfa!=(gamma)"),count_tape2))      
        for tape1 in tape2:
            count +=1
            tape1_elm = tape1[0][0][1]

            tmp.append((count_tape2+1,((encoded_symbols[tape1_elm[1]]),encoded_symbols[tape1_elm[1]]),count))    
            count_tape1 = count
            
            tmp.append((count_tape1,"(RIGHT)",count_tape1+1)) 
            tmp.append((count_tape1+1,("alfa!=(gamma)","alfa!=(gamma)"),count_tape1))  

            tmp.append((count_tape1+1,((encoded_symbols[tape2_elm[1]],encoded_symbols[tape2_elm[1]])),count_tape1+2))  

            tmp.append((count_tape1+2,"(RIGHT)",count_tape1+3)) 
            tmp.append((count_tape1+3,("alfa!=(gamma)","alfa!=(gamma)"),count_tape1+2))    
            
            count += 4
            for tape3 in tape1:
                tape3_elm = tape3[0][3]
                tmp.append((count_tape1+3,((encoded_symbols[tape3_elm[1]],encoded_symbols[tape3_elm[1]])),connection_dict[Inverter.Invert_compiler(tape3)[0]]))  
            # count += 1
        count+=1
    return Inverter.Invert1Tape_compiler(tmp[::-1]), count, states_dict

def Expand_move(states,count,states_dict):
    tmp = []
    start_state = states[0][0][0][0][0]
    if not(start_state in states_dict.keys()):
            states_dict[start_state] = count

    tape1_elm = states[0][0][0][0][1]
    tape2_elm = states[0][0][0][0][2]
    tape3_elm = states[0][0][0][0][3]
    count+=1
    tmp.append((states_dict[start_state],("gamma","gamma"),count))

    if not(tape2_elm == "(STAY)"):
        tmp.append((count,("gamma","alfa"),count+1))
        tmp.append((count+1,tape2_elm,count+2))
        tmp.append((count+2,("alfa","gamma"),count+3))
    else:
        tmp.append((count,("gamma","gamma"), count+3)) 
        
    tmp.append((count+3,"(LEFT)",count+4))
    tmp.append((count+4,("alfa!=(gamma)","alfa!=(gamma)"),count+3))
    
    if not(tape1_elm == "(STAY)"):
        tmp.append((count+4,("gamma","alfa"),count+5))
        tmp.append((count+5,tape1_elm,count+6))
        tmp.append((count+6,("alfa","gamma"),count+7))
    else:
        tmp.append((count+4,("gamma","gamma"), count+7))
         
    tmp.append((count+7,"(RIGHT)",count+8))
    tmp.append((count+8,("alfa!=(gamma)","alfa!=(gamma)"),count+7))
    tmp.append((count+8,("gamma","gamma"),count+9))
    tmp.append((count+9,"(RIGHT)",count+10))
    tmp.append((count+10,("alfa!=(gamma)","alfa!=(gamma)"),count+9))
    
    if not(tape3_elm == "(STAY)"):
        tmp.append((count+10,("gamma","alfa"),count+11))
        tmp.append((count+11,tape3_elm,count+12))
        tmp.append((count+12,("alfa","gamma"),count+13))
    else:
        tmp.append((count+10,("gamma","gamma"), count+13)) 
    tmp.append((count+13,"(LEFT)",count+14))
    tmp.append((count+14,("alfa!=(gamma)","alfa!=(gamma)"),count+13))
    
    final_state = states[0][0][0][0][-1]
    if not(final_state in states_dict.keys()):
        states_dict[final_state] = count+15
    tmp.append((count+14,("gamma","gamma"),states_dict[final_state] ))
    count +=16
    return Replace_final_state(tmp,count), count, states_dict


def Expand(instructions_top,instructions_bottom):
    states_dict = {'1': 8}
    connection_dict = {}
    final = []
    count = 1
    final.append([(count,("b","b"),count+1)])
    final.append([(count+1,"(RIGHT)",count+2)])
    final.append([(count+2,("$","$"),count+3)])
    final.append([(count+3,"(RIGHT)",count+4)])
    final.append([(count+4,("alfa!=(gamma)","alfa!=(gamma)"),count+3)])
    final.append([(count+4,("gamma","gamma"),count+5)])

    final.append([(count+5,"(RIGHT)",count+6)])
    final.append([(count+6,("alfa!=(gamma)","alfa!=(gamma)"),count+5)])
    final.append([(count+6,("gamma","gamma"),count+7)])

    count += 8
    for states in instructions_top:
        if (states[0][0][0][0][1] == "(LEFT)" or
            states[0][0][0][0][1] == "(RIGHT)" or
            states[0][0][0][0][1] == "(STAY)"):
            result, count, states_dict = Expand_move(states,count,states_dict)
        else:
            result, count, states_dict, connection_dict = Expand_symbol_top_tree(states,count,states_dict,connection_dict)
        final.append(result)
    for states in instructions_bottom:
        if (states[0][0][0][0][1] == "(LEFT)" or
            states[0][0][0][0][1] == "(RIGHT)" or
            states[0][0][0][0][1] == "(STAY)"):
            continue
        else:
            result, count, states_dict = Expand_symbol_bottom_tree(states,count,states_dict,connection_dict)
        final.append(result)
    final.append([(states_dict['0'],"(LEFT)",count+1)])
    final.append([(count+1,("alfa!=(gamma)","alfa!=(gamma)"),states_dict['0'])])
    final.append([(count+1,("gamma","gamma"),count+2)])

    # final.append([(count+2,"(LEFT)",count+3)])
    # final.append([(count+3,("alfa!=(gamma)","alfa!=(gamma)"),count+2)])
    # final.append([(count+3,("gamma","gamma"),count+4)])
    
    final.append([(count+2,"(LEFT)",count+3)])
    final.append([(count+3,("alfa!=($)","alfa!=($)"),count+2)])
    final.append([(count+3,("$","$"),count+4)])
    final.append([(count+4,"(LEFT)",count+5)])
    final.append([(count+5,("b","b"),count+6)])

    print("finalstate :", count+6)
    return final
    
def group(rules):
    return groupByTape3(groupByTape1(groupByTape2(groupByStates(rules))))

def tuple_to_string(tuple):
    if ("RIGHT" in tuple[1] or
        "LEFT" in tuple[1] or
        "STAY" in tuple[1]):
        return "(" + str(tuple[0]) + "," + str(tuple[1]) + "," + str(tuple[2]) + ")"
    else:
        symbol = tuple[1]
        return "(" + str(tuple[0]) + ",(" + symbol[0] + "," + (symbol[1]) + ")," + str(tuple[2]) + ")"
    

file_name,name = Read_file.input_file()
lines = Read_file.read_file(file_name)
forward_lines = lines.copy()
Inverted_lines = Inverter.Invert(lines)
tape1 = (Expand(group(forward_lines),group(Inverted_lines)))
expanded = []
for elm in tape1:
    expanded.append(Expand_1_tape.expand(elm))
if name.find("/") == -1:
    outfile = open("1_Tape_programs/" + name,'w+')
else:
    outfile = open(name, 'w+')
for elm1 in expanded:
    for elm in elm1:
        outfile.write(tuple_to_string(elm) + "\n")