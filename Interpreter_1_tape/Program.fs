open Helper
open System.IO
open Interpreter

[<EntryPoint>]
let main args =
    if args.Length = 4 then
        let rules = read_rules(args[0])
        let tape = read_tape(args[1])
        printfn "%A" (RMT (rules,(int args[2],int args[3]),(tape), Some 1))
    else if args.Length = 5 then
        let rules = read_rules(args[0])
        let tape = read_tape(args[1])
        printfn "%s" (System.String (RMT (rules,(int args[2],int args[3]),(tape), Some (int args[4]))))
    else if args.Length = 2 then
        let rules = read_rules(args[0])
        let tape = read_tape(args[1])
        printfn "%A" (RMT (rules,(1,21167),(tape), Some 1))
    else
        printfn "Expected 2,4,5 arugments - Recieved %A" args.Length
    0