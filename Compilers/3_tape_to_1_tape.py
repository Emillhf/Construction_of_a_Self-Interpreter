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
        tmp.append((count+14,("b","b"),count+147))
        tmp.append((count+14,("1","b"),count+16))
        tmp.append((count+15,("(LEFT)"),count+17))
        tmp.append((count+147,("(LEFT)"),count+142))
        tmp.append((count+16,("(LEFT)"),count+18))
        tmp.append((count+142,("b","b"),count+12))
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
        tmp.append((count+28,("gamma","gamma"),count+72))  
        
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
        tmp.append((count+44,("alfa","alfa"),count+45))
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
        tmp.append((count+6,("alfa","gamma"),count+72))
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
        
        tmp.append((count+142,("b","b"),count+14))
        tmp.append((count+15,("b","0"),count+14))
        tmp.append((count+16,("b","1"),count+14))
        tmp.append((count+17,"(RIGHT)",count+15))
        tmp.append((count+147,"(RIGHT)",count+142))
        tmp.append((count+18,"(RIGHT)",count+16))
        tmp.append((count+12,("0","b"),count+17))
        tmp.append((count+12,("b","b"),count+147))
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
        tmp.append((count+45,("alfa","alfa"),count+44))
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
    elif (tape1_elm == "(STAY)"):
        tmp.append((count+5,("gamma","gamma"),count+72))       
    
    tmp.append((count+72,"(RIGHT)",count+150))
    tmp.append((count+150,("alfa!=(gamma)","alfa!=(gamma)"),count+72))
    tmp.append((count+150,("gamma","gamma"),count+73))

    tmp.append((count+73,"(RIGHT)",count+74))
    tmp.append((count+74,("alfa!=(gamma)","alfa!=(gamma)"),count+73))
    tmp.append((count+74,("gamma","gamma"),count+75))
    
    if (tape3_elm == "(LEFT)"):
        tmp.append((count+75,(("gamma","alfa")),count+76))
        tmp.append((count+76,"(LEFT)",count+77))
        tmp.append((count+77,(("$","$")),count+78))
        tmp.append((count+77,(("alfa!=($)","alfa!=($)")),count+99))
        tmp.append((count+78,"(RIGHT)",count+79))
        tmp.append((count+79,(("alfa!=($)","alfa!=($)")),count+78))
        tmp.append((count+79,(("$","b")),count+80))
        tmp.append((count+80,"(RIGHT)",count+81))
        tmp.append((count+81,(("b","$")),count+82))
        tmp.append((count+82,"(LEFT)",count+83))
        tmp.append((count+83,"(LEFT)",count+84))
        tmp.append((count+84,(("$","$")),count+89))
        tmp.append((count+84,(("#","b")),count+143))
        tmp.append((count+84,(("b","b")),count+149))
        tmp.append((count+84,(("0","b")),count+85))
        tmp.append((count+84,(("1","b")),count+86))
        tmp.append((count+85,"(RIGHT)",count+87))
        tmp.append((count+143,"(RIGHT)",count+144))
        tmp.append((count+149,"(RIGHT)",count+148))
        tmp.append((count+86,"(RIGHT)",count+88))
        tmp.append((count+87,(("b","0")),count+82))
        tmp.append((count+144,(("b","#")),count+82))
        tmp.append((count+148,(("b","b")),count+82))
        tmp.append((count+88,(("b","1")),count+82))
        tmp.append((count+89,"(RIGHT)",count+90))
        tmp.append((count+90,(("b","p")),count+91))
        tmp.append((count+91,(("p","p")),count+92))
        tmp.append((count+92,"(LEFT)",count+93))
        tmp.append((count+93,(("$","$")),count+94))
        tmp.append((count+94,"(RIGHT)",count+95))
        tmp.append((count+95,"(RIGHT)",count+96))
        tmp.append((count+96,(("alfa!=($)","alfa!=($)")),count+97))
        tmp.append((count+97,"(LEFT)",count+98))
        tmp.append((count+98,("gamma","gamma"),count+151))
        
        tmp.append((count+99,"(RIGHT)",count+100))
        tmp.append((count+100,"(RIGHT)",count+101))
        tmp.append((count+101,(("alfa!=($)","alfa!=($)")),count+127))
        tmp.append((count+101,(("$","$")),count+102))
        tmp.append((count+102,"(LEFT)",count+103))
        tmp.append((count+103,(("alfa!=(b)","alfa!=(b)")),count+118))
        tmp.append((count+103,(("b","b")),count+104))
        tmp.append((count+104,"(RIGHT)",count+105))
        tmp.append((count+105,(("$","b")),count+106))
        tmp.append((count+106,"(LEFT)",count+107))
        tmp.append((count+107,(("b","$")),count+108))
        tmp.append((count+108,"(LEFT)",count+109))
        tmp.append((count+109,(("alfa","gamma")),count+110))
        tmp.append((count+110,"(RIGHT)",count+111))
        tmp.append((count+111,(("$","$")),count+112))
        tmp.append((count+112,"(LEFT)",count+113))
        tmp.append((count+113,"(LEFT)",count+114))
        tmp.append((count+114,(("alfa","alfa")),count+115))
        tmp.append((count+115,"(RIGHT)",count+116))
        tmp.append((count+116,"(RIGHT)",count+117))
        tmp.append((count+117,(("$","$")),count+97))
        tmp.append((count+118,"(LEFT)",count+119))
        tmp.append((count+119,(("alfa","gamma")),count+120))
        tmp.append((count+120,"(RIGHT)",count+121))
        tmp.append((count+121,"(RIGHT)",count+122))
        tmp.append((count+122,(("$","$")),count+123))
        tmp.append((count+123,"(LEFT)",count+124))
        tmp.append((count+124,"(LEFT)",count+125))
        tmp.append((count+125,"(LEFT)",count+126))
        tmp.append((count+126,(("alfa!=($)","alfa!=($)")),count+94))
        tmp.append((count+127,"(LEFT)",count+128))
        tmp.append((count+128,"(LEFT)",count+129))
        tmp.append((count+129,"(LEFT)",count+130))
        tmp.append((count+130,(("alfa!=($)","alfa!=($)")),count+134))
        tmp.append((count+130,(("$","$")),count+131))
        tmp.append((count+131,"(RIGHT)",count+132))
        tmp.append((count+132,(("alfa","gamma")),count+133))
        tmp.append((count+133,(("alfa!=(p)","alfa!=(p)")),count+92))
        tmp.append((count+134,"(RIGHT)",count+135))
        tmp.append((count+135,(("alfa","gamma")),count+136))
        tmp.append((count+136,"(LEFT)",count+137))
        tmp.append((count+137,(("alfa!=($)","alfa!=($)")),count+138))
        tmp.append((count+138,"(RIGHT)",count+139))
        tmp.append((count+140,"(RIGHT)",count+141))
        tmp.append((count+139,"(RIGHT)",count+140))
        tmp.append((count+141,(("alfa!=($)","alfa!=($)")),count+123))
    elif (tape3_elm == "(RIGHT)"):
        tmp.append((count+76,("alfa","gamma"),count+151))
        tmp.append((count+77,"(RIGHT)",count+76))
        tmp.append((count+78,("$","$"),count+77))
        tmp.append((count+99,("alfa!=($)","alfa!=($)"),count+77))
        tmp.append((count+79,"(LEFT)",count+78))
        tmp.append((count+78,("alfa!=($)","alfa!=($)"),count+79))
        tmp.append((count+80,("b","$"),count+79))
        tmp.append((count+81,"(LEFT)",count+80))
        tmp.append((count+82,("$","b"),count+81))
        tmp.append((count+83,"(RIGHT)",count+82))
        tmp.append((count+84,"(RIGHT)",count+83))
        tmp.append((count+89,("$","$"),count+84))
        tmp.append((count+85,("b","0"),count+84))
        tmp.append((count+145,("b","#"),count+84))
        tmp.append((count+149,("b","b"),count+84))
        tmp.append((count+86,("b","1"),count+84))
        tmp.append((count+87,"(LEFT)",count+85))
        tmp.append((count+88,"(LEFT)",count+86))
        tmp.append((count+146,"(LEFT)",count+145))
        tmp.append((count+148,"(LEFT)",count+149))
        tmp.append((count+82,("0","b"),count+87))
        tmp.append((count+82,("b","b"),count+148))
        tmp.append((count+82,("#","b"),count+146))
        tmp.append((count+82,("1","b"),count+88))
        tmp.append((count+90,"(LEFT)",count+89))
        tmp.append((count+91,("p","b"),count+90))
        tmp.append((count+92,("p","p"),count+91))
        tmp.append((count+93,"(RIGHT)",count+92))
        tmp.append((count+94,("$","$"),count+93))
        tmp.append((count+95,"(LEFT)",count+94))
        tmp.append((count+96,"(LEFT)",count+95))
        tmp.append((count+97,("alfa!=($)","alfa!=($)"),count+96))
        tmp.append((count+75,"(RIGHT)",count+97))
        tmp.append((count+100,"(LEFT)",count+99))
        tmp.append((count+101,"(LEFT)",count+100))
        tmp.append((count+127,("alfa!=($)","alfa!=($)"),count+101))
        tmp.append((count+102,("$","$"),count+101))
        tmp.append((count+103,"(RIGHT)",count+102))
        tmp.append((count+118,("alfa!=(b)","alfa!=(b)"),count+103))
        tmp.append((count+104,("b","b"),count+103))
        tmp.append((count+105,"(LEFT)",count+104))
        tmp.append((count+106,("b","$"),count+105))
        tmp.append((count+107,"(RIGHT)",count+106))
        tmp.append((count+108,("$","b"),count+107))
        tmp.append((count+109,"(RIGHT)",count+108))
        tmp.append((count+110,("gamma","alfa"),count+109))
        tmp.append((count+111,"(LEFT)",count+110))
        tmp.append((count+112,("$","$"),count+111))
        tmp.append((count+113,"(RIGHT)",count+112))
        tmp.append((count+114,"(RIGHT)",count+113))
        tmp.append((count+115,("alfa","alfa"),count+114))
        tmp.append((count+116,"(LEFT)",count+115))
        tmp.append((count+117,"(LEFT)",count+116))
        tmp.append((count+97,("$","$"),count+117))
        tmp.append((count+119,"(RIGHT)",count+118))
        tmp.append((count+120,("gamma","alfa"),count+119))
        tmp.append((count+121,"(LEFT)",count+120))
        tmp.append((count+122,"(LEFT)",count+121))
        tmp.append((count+123,("$","$"),count+122))
        tmp.append((count+124,"(RIGHT)",count+123))
        tmp.append((count+125,"(RIGHT)",count+124))
        tmp.append((count+126,"(RIGHT)",count+125))
        tmp.append((count+94,("alfa!=($)","alfa!=($)"),count+126))
        tmp.append((count+128,"(RIGHT)",count+127))
        tmp.append((count+129,"(RIGHT)",count+128))
        tmp.append((count+130,"(RIGHT)",count+129))
        tmp.append((count+134,("alfa!=($)","alfa!=($)"),count+130))
        tmp.append((count+131,("$","$"),count+130))
        tmp.append((count+132,"(LEFT)",count+131))
        tmp.append((count+133,("gamma","alfa"),count+132))
        tmp.append((count+92,("alfa!=(p)","alfa!=(p)"),count+133))
        tmp.append((count+135,"(LEFT)",count+134))
        tmp.append((count+136,("gamma","alfa"),count+135))
        tmp.append((count+137,"(RIGHT)",count+136))
        tmp.append((count+138,("alfa!=($)","alfa!=($)"),count+137))
        tmp.append((count+139,"(LEFT)",count+138))
        tmp.append((count+141,"(LEFT)",count+140))
        tmp.append((count+140,"(LEFT)",count+139))
        tmp.append((count+123,("alfa!=($)","alfa!=($)"),count+141))
    elif (tape3_elm == "(STAY)"):
        tmp.append((count+75,("gamma","gamma"),count+151))
    
    tmp.append((count+151,"(LEFT)",count+152))
    tmp.append((count+152,("alfa!=(gamma)","alfa!=(gamma)"),count+151))
    
    final_state = states[0][0][0][0][-1]
    if not(final_state in states_dict.keys()):
        states_dict[final_state] = count+153
    tmp.append((count+152,("gamma","gamma"),states_dict[final_state]))
    count +=154
    return Replace_final_state(tmp,count), count, states_dict


def Expand(instructions_top,instructions_bottom):
    states_dict = {'1': 3}
    connection_dict = {}
    final = []
    count = 1
    final.append([(count,"(RIGHT)",count+1)])
    final.append([(count+1,("alfa!=(gamma)","alfa!=(gamma)"),count)])
    final.append([(count+1,("gamma","gamma"),count+2)])

    count += 3
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

    print("finalstate :", count+2)
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
outfile = open("1_Tape_programs/" + name,'w+')
for elm1 in expanded:
    for elm in elm1:
        outfile.write(tuple_to_string(elm) + "\n")