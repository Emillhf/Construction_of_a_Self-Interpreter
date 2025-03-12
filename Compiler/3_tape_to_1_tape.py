import re
import sys
import Expand_1_tape

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
    tape1_dict = {}
    for rule in rules:
        tape1_elm = rule[tape]
        if tape1_elm in tape1_dict.keys():
            tape1_dict[tape1_elm].append(rule)
        else:
            tape1_dict[tape1_elm] = [rule]
    return list(tape1_dict.values())
        
def groupByTape1(state_rules:list[list[tuple[str]]]):
    final = []
    for rules in state_rules:
        final.append(inner_list(rules,1))
            
    return final

def groupByTape2(state_rules:list[list[list[tuple[str]]]]):
    final = []
    for grouped_rules in state_rules:
        temp = []
        for rules in grouped_rules:
            temp.append(inner_list(rules,2))
        final.append(temp)
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

def Expand_symbol(states,count,states_dict):
    tmp = []
    start_state = states_dict[states[0][0][0][0][0]]
    for tape1 in states:
        tape1_elm = tape1[0][0][0][1]
        tmp.append((start_state,((encoded_symbols[tape1_elm[1]],encoded_symbols[tape1_elm[3]])),count))  
        count_tape1 = count
        tmp.append((count_tape1,"(RIGHT)",count_tape1+1)) 
        count += 1
        tmp.append((count_tape1+1,("alfa!=(gamma)","alfa!=(gamma)"),count_tape1))      
        for tape2 in tape1:
            tape2_elm = tape2[0][0][2]
            tmp.append((count_tape1+1,((encoded_symbols[tape2_elm[1]]),encoded_symbols[tape2_elm[3]]),count+1))    
            count += 1
            count_tape2 = count
            tmp.append((count_tape2,"(RIGHT)",count_tape2+1)) 
            tmp.append((count_tape2+1,("alfa!=(gamma)","alfa!=(gamma)"),count_tape2))    
            for tape3 in tape2:
                count += 2
                tape3_elm = tape3[0][3]
                tmp.append((count_tape2+1,((encoded_symbols[tape3_elm[1]],encoded_symbols[tape3_elm[3]])),0))  
                
        count += 1
    
    tmp_final = count
    count += 1
    tmp.append((0,"(LEFT)",count))
    tmp.append((count,("alfa!=(gamma)","alfa!=(gamma)"),0))
    tmp.append((count,("gamma","gamma"),count+1))
    count += 1
    tmp.append((count,"(LEFT)",count+1))
    tmp.append((count+1,("alfa!=(gamma)","alfa!=(gamma)"),count))
    final_state = states[0][0][0][0][-1]
    if not(final_state in states_dict.keys()):
        states_dict[final_state] = count
        tmp.append((count+1,("gamma","gamma"),count+2))
    else:
        tmp.append((count+1,("gamma","gamma"),states_dict[final_state]))
    count += 2
    return Replace_final_state(tmp,tmp_final), count, states_dict

def Expand_move(states,count,states_dict):
    tmp = []
    start_state = states_dict[states[0][0][0][0][0]]
    tape1_elm = states[0][0][0][0][1]
    tape2_elm = states[0][0][0][0][2]
    tape3_elm = states[0][0][0][0][3]
    
    tmp.append((start_state,("gamma","alfa"),count))
    tmp.append((count,tape1_elm,count+1))
    tmp.append((count+1,("alfa","gamma"),count+2))
    tmp.append((count+2,"(RIGHT)",count+3))
    tmp.append((count+3,("alfa!=(gamma)","alfa!=(gamma)"),count+2))
    tmp.append((count+3,("gamma","alfa"),count+5))
    tmp.append((count+5,tape2_elm,count+6))
    tmp.append((count+6,("alfa","gamma"),count+7))
    tmp.append((count+7,"(RIGHT)",count+8))
    tmp.append((count+8,("alfa!=(gamma)","alfa!=(gamma)"),count+7))
    tmp.append((count+8,("gamma","alfa"),count+10))
    tmp.append((count+10,tape3_elm,count+11))
    tmp.append((count+11,("alfa","gamma"),count+12))
    tmp.append((count+12,"(LEFT)",count+14))
    tmp.append((count+14,("alfa!=(gamma)","alfa!=(gamma)"),count+12))
    tmp.append((count+14,("gamma","gamma"),count+15))
    tmp.append((count+15,"(LEFT)",count+16))
    tmp.append((count+16,("alfa!=(gamma)","alfa!=(gamma)"),count+15))
    tmp.append((count+16,("gamma","gamma"),0))
    
    count += 17
    final_state = states[0][0][0][0][-1]
    if not(final_state in states_dict.keys()):
        states_dict[states[0][0][0][0][-1]] = count
    return Replace_final_state(tmp,count), count+1, states_dict


def Expand(instructions):
    states_dict = {'1': 1}
    final = []
    count = 2
    for states in instructions:
        if (states[0][0][0][0][1] == "(LEFT)" or
            states[0][0][0][0][1] == "(RIGHT)" or
            states[0][0][0][0][1] == "(STAY)"):
            result, count, states_dict = Expand_move(states,count,states_dict)
            final.append(result)
        else:
            result, count, states_dict = Expand_symbol(states,count,states_dict)
            final.append(result)
            
    print(states_dict)
    return final
    
def group(rules):
    return groupByTape3(groupByTape2(groupByTape1(groupByStates(rules))))

def tuple_to_string(tuple):
    if ("RIGHT" in tuple[1] or
        "LEFT" in tuple[1] or
        "STAY" in tuple[1]):
        return "(" + str(tuple[0]) + "," + str(tuple[1]) + "," + str(tuple[2]) + ")"
    else:
        symbol = tuple[1]
        return "(" + str(tuple[0]) + ",(" + symbol[0] + "," + (symbol[1]) + ")," + str(tuple[2]) + ")"
test = ["(1,((0,0),(#,#),(#,b)),2)",
        "(1,((b,b),(b,b),(1,1)),2)",
        "(1,((b,b),(b,b),(#,b)),2)",
        "(2,((STAY),(RIGHT),(RIGHT)),3)",
       "(3,((0,0),(0,0),(0,0)),2)"]

test_single = [[[[[(('1','(0,0)','(#,#)','(#,b)','2'))]]]]]
state_rules = groupByStates(test)
grouped_by_tape_1 = groupByTape1(state_rules)
#print(grouped_by_tape_1, len(grouped_by_tape_1))
grouped_by_tape_2 = groupByTape2(grouped_by_tape_1)
#print(grouped_by_tape_2, len(grouped_by_tape_2))
grouped_by_tape_3 = groupByTape3(grouped_by_tape_2)
#print(len(grouped_by_tape_3))
# for elm1 in grouped_by_tape_3:
#     for elm2 in elm1:
#         for elm3 in elm2: 
#             for elm4 in elm3:
#                 print(elm4)

name = "Write_0_or_1.txt"
file = open("Expanded_RTM_programs/"+name, 'r')
lines = file.readlines()
lines = [line.strip() for line in lines]
tape1 = (Expand(group(lines)))
expanded = []
for elm in tape1:
    expanded.append(Expand_1_tape.expand(elm))
outfile = open("1_Tape_programs/" + name,'w+')
for elm1 in expanded:
    for elm in elm1:
        outfile.write(tuple_to_string(elm) + "\n")