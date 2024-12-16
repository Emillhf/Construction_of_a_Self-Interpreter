open Interpreter
let INC:List<Rule> =   [(1,Replace('B','B'), 2)
                        (2,Move("RIGHT"),3)
                        (3,Replace('0','1'),4)
                        (3,Replace('1','0'),2)
                        (3,Replace('B','B'),4)
                        (4,Move("LEFT"),5)
                        (5,Replace('0','0'),4)
                        (5,Replace('B','B'),6)]
let DecINC:List<Rule> =[(6,Replace('B','B'),5)
                        (4,Replace('0','0'),5)
                        (5,Move("RIGHT"),4)
                        (4,Replace('B','B'),3)
                        (2,Replace('0','1'),3)
                        (4,Replace('1','0'),3)
                        (3,Move("LEFT"),2)
                        (2,Replace('B','B'), 1)]

let Start:int*int = (1,6)
let decStart:int*int = (6,1)
let tapes:tapes = ("B1101",(),())
let decTapes:tapes = ("B0011",(),())
printfn "%A" (RMT (INC,Start, tapes))
printfn "%A" (RMT (DecINC,decStart, decTapes))

