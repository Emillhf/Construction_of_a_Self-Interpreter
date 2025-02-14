import Encoding
import StateTransitioner
import Expander
import os




program = ["(0,((),(RIGHT),()),1)",
            "(1,((),(0,1),(1,2)),2)",
            "(1,((),(1,0),(1,2)),2)",
            "(1,((),(LEFT),()),2)"]

BinINC = ["(1,((B,B),(beta,beta),()),2)", ## kan indsætte et beta på operation 2
        "(2,((RIGHT),(),()),3)",
        "(3,((0,1),(),()),4)",
        "(3,((1,0),(),()),2)",
        "(3,((B,B),(),()),4)",
        "(4,((LEFT),(),()),5)",
        "(5,((0,0),(),()),4)",
        "(5,((B,B),(),()),6)"]

BinDec = ["(2,((),(B,B),()),1)",
        "(3,((),(LEFT),()),2)",
        "(4,((),(1,0),()),3)",
        "(2,((),(0,1),()),3)",
        "(4,((),(B,B),()),3)",
        "(5,((),(RIGHT),()),4)",
        "(4,((),(0,0),()),5)",
        "(6,((),(B,B),()),5)"
        ]

filename_user = input("Please give a path to a file where the program resides without .txt\n")
file_user = open(os.getcwd() +"/" + filename_user + ".txt","r")
lines_user = file_user.readlines()
rules_user = [rule.removesuffix("\n") for rule in lines_user]
start_state_user = input("Please give an start state\n")
final_state_user = input("Please give an final state\n")

inputt = "1101"
##rules_enc = Encoding.Encode(StateTransitioner.StateTransition(Expander.expand_rules(BinINC,Expander.alfa,Expander.beta), "1", "6"))
rules_enc = Encoding.Encode(
    StateTransitioner.StateTransition(
        Expander.expand_rules(
            rules_user,Expander.alfa,Expander.beta), start_state_user, final_state_user))

f = open(os.getcwd() + "/" + filename_user + "_enc" + ".txt", "w+")
f.write("B" + inputt + "B\n!\n")
f.write("B" + rules_enc +"B\n$\n")
f.write("B#1#B")
f.close()