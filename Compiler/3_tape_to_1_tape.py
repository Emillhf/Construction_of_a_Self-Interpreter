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
    tape_dict = {}
    for rule in rules:
        tape_elm = rule[tape]
        if tape_elm in tape_dict.keys():
            tape_dict[tape_elm].append(rule)
        else:
            tape_dict[tape_elm] = [rule]
    return list(tape_dict.values())
        
def groupByTape2(state_rules):
    final = []
    for rules in state_rules:
        final.append(inner_list(rules,2))
            
    return final
# def groupByTape1(state_rules:list[list[tuple[str]]]):
#     final = []
#     for rules in state_rules:
#         final.append(inner_list(rules,1))
            
#     return final

def groupByTape1(state_rules):
    final = []
    for grouped_rules in state_rules:
        temp = []
        for rules in grouped_rules:
            temp.append(inner_list(rules,1))
        final.append(temp)

    return final
# def groupByTape2(state_rules:list[list[list[tuple[str]]]]):
#     final = []
#     for grouped_rules in state_rules:
#         temp = []
#         for rules in grouped_rules:
#             temp.append(inner_list(rules,2))
#         final.append(temp)
#     return final

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
# def groupByTape3(state_rules):
#     final = []
#     for grouped_rules in state_rules:
#         temp1 = []
#         for grouped_by_tape_1 in grouped_rules:
#             temp2 = []
#             for rules in grouped_by_tape_1:
#                 temp2.append(inner_list(rules,3))
#             temp1.append(temp2)
#         final.append(temp1)
#     return final

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
                tmp.append((count_tape1+3,((encoded_symbols[tape3_elm[1]],encoded_symbols[tape3_elm[3]])),count))  
            
                tmp.append((count,"(LEFT)",count+1))
                tmp.append((count+1,("alfa!=(gamma)","alfa!=(gamma)"),count))
                
                tmp.append((count+1,((encoded_symbols[tape2_elm[3]],encoded_symbols[tape2_elm[3]])),count+2))  
                                
                final_state = tape3[0][-1]
                if not(final_state in states_dict.keys()):
                    tmp.append((count+9,((encoded_symbols[tape2_elm[3]],encoded_symbols[tape2_elm[3]])),count+10))  
                    states_dict[final_state] = count+10
                else:
                    tmp.append((count+9,((encoded_symbols[tape2_elm[3]],encoded_symbols[tape2_elm[3]])),states_dict[final_state]))  
                count += 11
            # count += 1
        count+=1
    return tmp, count, states_dict

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
    # tmp.append((count,"(RIGHT)",count+1))
    # tmp.append((count+1,("alfa!=(gamma)","alfa!=(gamma)"),count))
    tmp.append((count,("gamma","alfa"),count+1))
    tmp.append((count+1,tape2_elm,count+2))
    tmp.append((count+2,("alfa","gamma"),count+3))
    
    tmp.append((count+3,"(LEFT)",count+4))
    tmp.append((count+4,("alfa!=(gamma)","alfa!=(gamma)"),count+3))
    
    # Et udkast til hvordan man kan lave tapes uendelig
    tmp.append((count+4,("gamma","gamma"),count+5))
    if (tape1_elm == "(RIGHT)"):
        tmp.append((count+5,("gamma","alfa"),count+6))
        tmp.append((count+6,("(RIGHT)"),count+7))
        tmp.append((count+7,("$","$"),count+8)) #VI BEFINDER OS HELE VEJEN PÅ HØJRE SIDE AF TAPE 1
        tmp.append((count+7,("alfa!=($)","alfa!=($)"),count+29))
        tmp.append((count+8,("(LEFT)"),count+9))
        
        tmp.append((count+9,("alfa!=($)","alfa!=($)"),count+8)) #Goto the (left) $ on tape 1
        tmp.append((count+9,("$","b"),count+10))
        tmp.append((count+10,("(LEFT)"),count+11))
        tmp.append((count+11,("b","$"),count+12))
        tmp.append((count+12,("(RIGHT)"),count+13))
        tmp.append((count+13,("(RIGHT)"),count+14))
        tmp.append((count+14,("$","$"),count+19)) #all the way to the (right) $ on tape 1
        tmp.append((count+14,("0","b"),count+15))
        tmp.append((count+14,("1","b"),count+16))
        tmp.append((count+15,("(LEFT)"),count+17))
        tmp.append((count+16,("(LEFT)"),count+18))
        tmp.append((count+17,("b","0"),count+12))
        tmp.append((count+18,("b","1"),count+12))
        tmp.append((count+19,("(LEFT)"),count+20)) 
        tmp.append((count+20,("b","p"),count+21)) #FINISHED #Står på p #CASE 1 er færdig        
        tmp.append((count+21,("p","p"),count+22))    ## (1)  ##
        
        tmp.append((count+22,("(RIGHT)"),count+23))
        
        tmp.append((count+23,("$","$"),count+24))    ## (3)  ##
        tmp.append((count+24,("(LEFT)"),count+25))
        tmp.append((count+25,("(LEFT)"),count+26))
        tmp.append((count+26,("alfa!=($)","alfa!=($)"),count+27))    ## (4)  ##
        
        tmp.append((count+27,("(RIGHT)"),count+28))   ## FINAL ##
        
        tmp.append((count+29,("(LEFT)"),count+30))
        tmp.append((count+30,("(LEFT)"),count+31))
        
        tmp.append((count+31,("alfa!=($)","alfa!=($)"),count+57))
        tmp.append((count+31,("$","$"),count+32))
        
        tmp.append((count+32,("(RIGHT)"),count+33))
        tmp.append((count+33,("alfa!=(b)","alfa!=(b)"),count+48))
        tmp.append((count+33,("b","b"),count+34))
        
        tmp.append((count+34,("(LEFT)"),count+35))
        tmp.append((count+35,("$","b"),count+36))
        tmp.append((count+36,("(RIGHT)"),count+37))
        tmp.append((count+37,("b","$"),count+38))
        tmp.append((count+38,("(RIGHT)"),count+39))
        tmp.append((count+39,("alfa","gamma"),count+40))
        tmp.append((count+40,("(LEFT)"),count+41))
        tmp.append((count+41,("$","$"),count+42))
        tmp.append((count+42,("(RIGHT)"),count+43))
        tmp.append((count+43,("(RIGHT)"),count+44))
        tmp.append((count+44,("alfa!=($)","alfa!=($)"),count+45))
        tmp.append((count+45,("(LEFT)"),count+46))
        tmp.append((count+46,("(LEFT)"),count+47))
        tmp.append((count+47,("$","$"),count+27)) ## (4) ##
        
        tmp.append((count+48,("(RIGHT)"),count+49))
        tmp.append((count+49,("alfa","gamma"),count+50))
        tmp.append((count+50,("(LEFT)"),count+51))
        tmp.append((count+51,("(LEFT)"),count+52))
        tmp.append((count+52,("$","$"),count+53)) ## (2) ##
        tmp.append((count+53,("(RIGHT)"),count+54))
        tmp.append((count+54,("(RIGHT)"),count+55))
        tmp.append((count+55,("(RIGHT)"),count+56))
        tmp.append((count+56,("alfa!=($)","alfa!=($)"),count+24)) ## (3) ##
        
        tmp.append((count+57,("(RIGHT)"),count+58))
        tmp.append((count+58,("(RIGHT)"),count+59))
        tmp.append((count+59,("(RIGHT)"),count+60))
        tmp.append((count+60,("alfa!=($)","alfa!=($)"),count+64))        
        tmp.append((count+60,("$","$"),count+61)) 
        tmp.append((count+61,("(LEFT)"),count+62))
        tmp.append((count+62,("alfa","gamma"),count+63)) 
        tmp.append((count+63,("alfa!=(p)","alfa!=(p)"),count+22))  ## (1) ##
        
        tmp.append((count+64,("(LEFT)"),count+65)) 
        tmp.append((count+65,("alfa","gamma"),count+66)) 
        tmp.append((count+66,("(RIGHT)"),count+67)) 
        tmp.append((count+67,("alfa!=($)","alfa!=($)"),count+68)) 
        tmp.append((count+68,("(LEFT)"),count+69)) 
        tmp.append((count+69,("(LEFT)"),count+70)) 
        tmp.append((count+70,("(LEFT)"),count+71)) 
        tmp.append((count+71,("alfa!=($)","alfa!=($)"),count+53))  ## (2) ##
    elif (tape1_elm == "(LEFT)"):
        tmp.append((count+6,("alfa","gamma"),count+28))
        tmp.append((count+7,"(LEFT)",count+6))
        tmp.append((count+8,("$","$"),count+7))
        tmp.append((count+29,("alfa!=($)","alfa!=($)"),count+7))
        tmp.append((count+9,"(RIGHT)",count+8))

        tmp.append((count+8,("alfa!=($)","alfa!=($)"),count+9))
        tmp.append((count+10,("b","$"),count+9))
        tmp.append((count+11,"(RIGHT)",count+10))
        tmp.append((count+12,("$","b"),count+11))
        tmp.append((count+13,"(LEFT)",count+12))
        tmp.append((count+14,"(LEFT)",count+13))
        tmp.append((count+19,("$","$"),count+14))
        tmp.append((count+15,("b","0"),count+14))
        tmp.append((count+16,("b","1"),count+14))
        tmp.append((count+17,"(RIGHT)",count+15))
        tmp.append((count+18,"(RIGHT)",count+16))
        tmp.append((count+12,("0","b"),count+17))
        tmp.append((count+12,("1","b"),count+18))
        tmp.append((count+20,"(RIGHT)",count+19))
        tmp.append((count+21,("p","b"),count+20))
        tmp.append((count+22,("p","p"),count+21))

        tmp.append((count+23,"(LEFT)",count+22))

        tmp.append((count+24,("$","$"),count+23))
        tmp.append((count+25,"(RIGHT)",count+24))
        tmp.append((count+26,"(RIGHT)",count+25))
        tmp.append((count+27,("alfa!=($)","alfa!=($)"),count+26))

        tmp.append((count+5,"(LEFT)",count+27))

        tmp.append((count+30,"(RIGHT)",count+29))
        tmp.append((count+31,"(RIGHT)",count+30))

        tmp.append((count+57,("alfa!=($)","alfa!=($)"),count+31))
        tmp.append((count+32,("$","$"),count+31))

        tmp.append((count+33,"(LEFT)",count+32))
        tmp.append((count+48,("alfa!=(b)","alfa!=(b)"),count+33))
        tmp.append((count+34,("b","b"),count+33))

        tmp.append((count+35,"(RIGHT)",count+34))
        tmp.append((count+36,("b","$"),count+35))
        tmp.append((count+37,"(LEFT)",count+36))
        tmp.append((count+38,("$","b"),count+37))
        tmp.append((count+39,"(LEFT)",count+38))
        tmp.append((count+40,("gamma","alfa"),count+39))
        tmp.append((count+41,"(RIGHT)",count+40))
        tmp.append((count+42,("$","$"),count+41))
        tmp.append((count+43,"(LEFT)",count+42))
        tmp.append((count+44,"(LEFT)",count+43))
        tmp.append((count+45,("alfa!=($)","alfa!=($)"),count+44))
        tmp.append((count+46,"(RIGHT)",count+45))
        tmp.append((count+47,"(RIGHT)",count+46))
        tmp.append((count+27,("$","$"),count+47))

        tmp.append((count+49,"(LEFT)",count+48))
        tmp.append((count+50,("gamma","alfa"),count+49))
        tmp.append((count+51,"(RIGHT)",count+50))
        tmp.append((count+52,"(RIGHT)",count+51))
        tmp.append((count+53,("$","$"),count+52))
        tmp.append((count+54,"(LEFT)",count+53))
        tmp.append((count+55,"(LEFT)",count+54))
        tmp.append((count+56,"(LEFT)",count+55))
        tmp.append((count+24,("alfa!=($)","alfa!=($)"),count+56))

        tmp.append((count+58,"(LEFT)",count+57))
        tmp.append((count+59,"(LEFT)",count+58))
        tmp.append((count+60,"(LEFT)",count+59))
        tmp.append((count+64,("alfa!=($)","alfa!=($)"),count+60))
        tmp.append((count+61,("$","$"),count+60))
        tmp.append((count+62,"(RIGHT)",count+61))
        tmp.append((count+63,("gamma","alfa"),count+62))
        tmp.append((count+22,("alfa!=(p)","alfa!=(p)"),count+63))

        tmp.append((count+65,"(RIGHT)",count+64))
        tmp.append((count+66,("gamma","alfa"),count+65))
        tmp.append((count+67,"(LEFT)",count+66))
        tmp.append((count+68,("alfa!=($)","alfa!=($)"),count+67))
        tmp.append((count+69,"(RIGHT)",count+68))
        tmp.append((count+70,"(RIGHT)",count+69))
        tmp.append((count+71,"(RIGHT)",count+70))
        tmp.append((count+53,("alfa!=($)","alfa!=($)"),count+71))

        
        
        
        
        
        
        # tmp.append((count+22,("(LEFT)"),count+23))
        # tmp.append((count+23,("(LEFT)"),count+24))
        # tmp.append((count+24,("$","$"),count+45)) #VI BEFINDER OS HELE VEJEN PÅ VENSTRE SIDE AF TAPE 1
        # tmp.append((count+24,("alfa!=($)","alfa!=($)"),count+25))
        # # #case 5 / 2
        # tmp.append((count+25,("(RIGHT)"),count+26))
        # tmp.append((count+26,("(RIGHT)"),count+27))
        # tmp.append((count+27,("(RIGHT)"),count+28))
        # tmp.append((count+28,("$","$"),count+29)) #goto case 2
        # tmp.append((count+28,("alfa!=($)","alfa!=($)"),count+32)) # goto case 5
        
        # tmp.append((count+29,("(LEFT)"),count+30)) # case 2 begin
        # tmp.append((count+30,("alfa","gamma"),count+31)) #case 2 FINSIH
        # tmp.append((count+31,("(RIGHT)"),count+35))
        
        
        # tmp.append((count+32,("(LEFT)"),count+33)) #case 5 begin
        # tmp.append((count+33,("alfa","gamma"),count+34)) #case 5 FINSIH
        # tmp.append((count+34,("(RIGHT)"),count+36))
        
        # tmp.append((count+35,("$","$"),count+37)) #from case 2
        # tmp.append((count+36,("alfa!=($)","alfa!=($)"),count+37)) #from case 5
        # tmp.append((count+37,("(LEFT)"),count+38))
        # tmp.append((count+38,("(LEFT)"),count+39))
        # tmp.append((count+39,("(LEFT)"),count+40))
        
        # tmp.append((count+40,("alfa!=($)","alfa!=($)"),count+41)) #from case 2+5
        # tmp.append((count+59,("$","$"),count+41)) #from case 3+4
        # tmp.append((count+41,("(RIGHT)"),count+43))
        # tmp.append((count+43,("(RIGHT)"),count+44)) 
        # tmp.append((count+44,("(RIGHT)"),count+70)) 
        
        
        # tmp.append((count+45,("(RIGHT)"),count+46))
        # tmp.append((count+46,("b","b"),count+51)) #goto case 3
        # tmp.append((count+46,("alfa!=(b)","alfa!=(b)"),count+47)) #case 4
        # tmp.append((count+47,("(RIGHT)"),count+48)) # case 4 finish
        # tmp.append((count+48,("alfa","gamma"),count+50)) #FINSIH
        # tmp.append((count+50,("(LEFT)"),count+58)) # case 4 finish
        
        

        # #case 3
        # tmp.append((count+51,("(LEFT)"),count+52))
        # tmp.append((count+52,("$","b"),count+53))
        # tmp.append((count+53,("(RIGHT)"),count+54))
        # tmp.append((count+54,("b","$"),count+55))
        # tmp.append((count+55,("(RIGHT)"),count+56))
        # tmp.append((count+56,("alfa","gamma"),count+57)) #FINSIH
        # # tmp.append((count+56,("(LEFT)"),count+57))
        
        # # UNITED CASE 3 AND 4 below here
        # tmp.append((count+57,("$","$"),count+59))
        # tmp.append((count+58,("alfa!=($)","alfa!=($)"),count+60)) #from case 4   

        
        # #START SHIFT LEFT #case 1
        # tmp.append((count+8,("(LEFT)"),count+9))
        # tmp.append((count+9,("alfa!=($)","alfa!=($)"),count+8)) #Goto the (left) $ on tape 1
        # tmp.append((count+9,("$","b"),count+10))
        # tmp.append((count+10,("(LEFT)"),count+11))
        # tmp.append((count+11,("b","$"),count+12))
        # tmp.append((count+12,("(RIGHT)"),count+13))
        # tmp.append((count+13,("(RIGHT)"),count+14))
        # tmp.append((count+14,("$","$"),count+19)) #all the way to the (right) $ on tape 1
        # tmp.append((count+14,("0","b"),count+15))
        # tmp.append((count+14,("1","b"),count+16))
        # tmp.append((count+15,("(LEFT)"),count+17))
        # tmp.append((count+16,("(LEFT)"),count+18))
        # tmp.append((count+17,("b","0"),count+12))
        # tmp.append((count+18,("b","1"),count+12))
        # tmp.append((count+19,("(LEFT)"),count+20)) 
        # tmp.append((count+20,("b","p"),count+21)) #FINISHED #Står på p #CASE 1 er færdig
        # tmp.append((count+21,("(RIGHT)"),count+61)) 
               
        
        
        # #Unite case 1 with 2,3,4,5
        # tmp.append((count+61,("$","$"),count+62)) 
        # tmp.append((count+70,("alfa!=($)","alfa!=($)"),count+62))
        # tmp.append((count+62,("(LEFT)"),count+63))
        # tmp.append((count+63,("gamma","gamma"),count+64))

        #reversi
        # tmp.append((count+100,("$","$"),count+101))
        # # tmp.append((count+7,("alfa!=($)","alfa!=($)"),count+22)) - skal for-egnes med resten
        # tmp.append((count+102,("(LEFT)"),count+103))
        # tmp.append((count+104,("alfa","gamma"),count+105))
    
    # tmp.append((count+4,("gamma","alfa"),count+5))
    # tmp.append((count+5,tape1_elm,count+6))
    # tmp.append((count+6,("alfa","gamma"),count+7))
    
    # tmp.append((count+7,"(RIGHT)",count+8))
    # tmp.append((count+8,("alfa!=(gamma)","alfa!=(gamma)"),count+7))
    # tmp.append((count+8,("gamma","gamma"),count+9))
    # tmp.append((count+9,"(RIGHT)",count+10))
    # tmp.append((count+10,("alfa!=(gamma)","alfa!=(gamma)"),count+9))
    # tmp.append((count+10,("gamma","alfa"),count+11))
    # tmp.append((count+11,tape3_elm,count+12))
    # tmp.append((count+12,("alfa","gamma"),count+13))
    
    # tmp.append((count+13,"(LEFT)",count+14))
    # tmp.append((count+14,("alfa!=(gamma)","alfa!=(gamma)"),count+13))
    
    final_state = states[0][0][0][0][-1]
    if not(final_state in states_dict.keys()):
        states_dict[final_state] = count+72
    tmp.append((count+28,("gamma","gamma"),states_dict[final_state]))
    count +=73
    return Replace_final_state(tmp,count), count, states_dict



def Expand(instructions):
    states_dict = {'1': 3}
    final = []
    count = 1
    final.append([(count,"(RIGHT)",count+1)])
    final.append([(count+1,("alfa!=(gamma)","alfa!=(gamma)"),count)])
    final.append([(count+1,("gamma","gamma"),count+2)])
    # final.append([(count+2,"(RIGHT)",count+3)])
    # final.append([(count+3,("alfa!=(gamma)","alfa!=(gamma)"),count+2)])
    # final.append([(count+3,("gamma","gamma"),count+4)])
    count += 3
    for states in instructions:
        if (states[0][0][0][0][1] == "(LEFT)" or
            states[0][0][0][0][1] == "(RIGHT)" or
            states[0][0][0][0][1] == "(STAY)"):
            result, count, states_dict = Expand_move(states,count,states_dict)
        else:
            result, count, states_dict = Expand_symbol(states,count,states_dict)
        final.append(result)
    # final.append([(states_dict['0'],"(LEFT)",count+1)])
    # final.append([(count+1,("alfa!=(gamma)","alfa!=(gamma)"),states_dict['0'])])
    # final.append([(count+1,("gamma","gamma"),count+2)])

    print(states_dict, "finalstate :", states_dict['0'])
    return final
    
# def group(rules):
#     return groupByTape3(groupByTape2(groupByTape1(groupByStates(rules))))
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
# test = ["(1,((0,0),(#,#),(#,b)),2)",
#         "(1,((b,b),(b,b),(1,1)),2)",
#         "(1,((b,b),(b,b),(#,b)),2)",
#         "(2,((STAY),(RIGHT),(RIGHT)),3)",
#        "(3,((0,0),(0,0),(0,0)),2)"]

# test_single = [[[[[(('1','(0,0)','(#,#)','(#,b)','2'))]]]]]
# state_rules = groupByStates(test)

# grouped_by_tape_1 = groupByTape1(state_rules)
#print(grouped_by_tape_1, len(grouped_by_tape_1))
# grouped_by_tape_2 = groupByTape2(grouped_by_tape_1)
#print(grouped_by_tape_2, len(grouped_by_tape_2))
# grouped_by_tape_3 = groupByTape3(grouped_by_tape_2)
#print(len(grouped_by_tape_3))
# for elm1 in grouped_by_tape_3:
#     for elm2 in elm1:
#         for elm3 in elm2: 
#             for elm4 in elm3:
#                 print(elm4)

# name = "Move_test.txt"
# name = "Write_0_or_1.txt"
# name = "clear_state.txt"
# name = "write_state.txt"
# name = "apply_symbol.txt"
# name = "URTM.txt"
# name = "move_right.txt"
name = "move_left.txt"
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