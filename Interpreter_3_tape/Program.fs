open System.IO
open Interpreter
open Helper
open Readers
open writer

[<EntryPoint>]
let main args =
    if args.Length = 3 && args[2] = "test" then

        let result_filename = Path.Combine(Path.GetDirectoryName(args[0]), "result.txt")
        let rules = read_rules(args[0])
        let tapes = read_tape_file(args[1])
        let result = RMT (rules,(1,0),(tapes))

        writer.writeCharArrayToFile result_filename result
    else if args.Length = 4 then
        let rules = read_rules(args[0])
        let tapes = read_tape_file(args[1])
        printfn "%A" (System.String (first (RMT (rules,(int args[2],int args[3]),(tapes)))))

    else if args.Length = 2 then

        let rules = read_rules(args[0])
        let tapes = read_tape_file(args[1])
        // printfn "Work-tape before : %A\n Work-tape after : %A" (System.String (first tapes)) (System.String (first (RMT (rules,(1,0),(tapes)))))
        printfn "%A" (System.String (first (RMT (rules,(1,0),(tapes)))))
    else
        printfn "Expected 2 arugments - Recieved %A" args.Length
    0