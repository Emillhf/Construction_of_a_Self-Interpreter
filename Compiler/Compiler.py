import Encoding
import StateTransitioner
import Expander
import os




program = ["(0,((),(RIGHT),()),1)",
            "(1,((),(0,1),(1,2)),2)",
            "(1,((),(1,0),(1,2)),2)",
            "(1,((),(LEFT),()),2)"]

BinINC = ["(1,((B,B),(),()),2)",
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



input = "1101"
rules_enc = Encoding.Encode(StateTransitioner.StateTransition(BinINC, "1", "6"))



f = open(os.getcwd() + "/F#_Interpreter_ikke_pæn/test.txt", "w")
f.write("B" + input + "B\n!\n")
f.write("B" + rules_enc +"B\n$\n")
f.write("B")
f.close()