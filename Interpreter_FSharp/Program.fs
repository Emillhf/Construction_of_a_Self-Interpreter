open System.IO
open Interpreter
open Helper
open Readers
open writer

// let clear_state = read_rules("../Expanded_clear_state.txt")
// let write_state = read_rules("../Expanded_write_state.txt")
//let clear_state= read_rules("Expanded_test.txt")
//let compare_state = read_rules("Expanded_compare_states.txt")
//let move_rule = read_rules("Expanded_test.txt")
// clear_state - Afprøvning

// let clear_and_write = read_rules("Expanded_RTM_Programs/clear_and_write.txt")
// let clear_and_write_tape = read_tape_file("Tapes_RTM/clear_and_write.txt")
// printfn "%A" (RMT (clear_and_write,(1,0),clear_and_write_tape))

// let rev_clear_and_write = read_rules("Expanded_RTM_Programs/rev_clear_state.txt")
// let rev_clear_and_write_tape = read_tape_file("Tapes_RTM/rev_clear_and_write.txt")
// printfn "%A" (RMT (rev_clear_and_write,(1,0),rev_clear_and_write_tape))

let symbol_rule = read_rules("Expanded_RTM_Programs/symbol_rule.txt")
//let compare_state = read_rules("Expanded_RTM_Programs/compare_states_q'.txt")
let apply_symbol = read_rules("Expanded_RTM_Programs/apply_symbol.txt")
let apply_symbol_tapes = read_tape_file("Tapes_RTM/apply_symbol.txt")
let URTM = read_rules("Expanded_RTM_programs/URTM.txt")
let rev_URTM = read_rules("Expanded_RTM_programs/rev_URTM.txt")
let move_rule = read_rules("Expanded_RTM_Programs/move_rule.txt")
let BinINC_tape = read_tape_file("Tapes_RTM/BinInc.txt")
let flip_tape = read_tape_file("Tapes_RTM/Flip.txt")
let BinInc_2_tape = read_tape_file("Tapes_RTM/BinInc_2.txt")
// printfn "%A" (RMT (apply_symbol,(1,0),apply_symbol_tapes))

// let symbol = read_rules("Expanded_RTM_Programs/symbol_rule.txt")
// let symbol_tapes = read_tape_file("Tapes_RTM/symbol_rule_test.txt")

// printfn "%A" (RMT (symbol,(1,0),symbol_tapes))

//Compare states - Afprøvning
//printfn "%A" (RMT (symbol_rule,(1,0),([|'b';'b'|],[|'#';'1';'0';'#';'B';'1';'#';'1';'0';'#'|], [|'#';'1';'0';'#'|])))
// printfn "%A" (RMT (URTM,(1,0),([|'b';'0';'b'|],[|'b';'M';'#';'1';'#';'0';'1';'#';'0';'1';'#';'M';'b'|], [|'b';'b';'b';'b';'b';'b';'b'|])))
// printfn "%A" (RMT (URTM,(1,0),([|'b';'0';'b'|],
//     [|'b';'M';'#';'1';'#';'0';'1';'#';'0';'1';'#';'M';'S';'#';'1';'0';'#';'0';'1';'#';'0';'#';'S';'b'|]
//     , [|'b';'b';'b';'b';'b';'b';'b'|])))
// printfn "%A" (RMT (move_rule,(1,0),([|'b';'b';'b'|],[|'#';'1';'#';'0';'1';'#';'0';'#';'M';'b'|], [|'#';'1';'#';'b';'b';'b';'b'|])))
//printfn "%A" URTM
//printfn "%A" (RMT (URTM,(1,0),(BinINC_tape)))
//printfn "%A" (RMT (URTM,(1,0),(flip_tape)))
//printfn "%A" (RMT (rev_URTM,(0,1),(BinInc_2_tape)))

//Move Rule - Afprøvning
//printfn "%A" (RMT (move_rule,(1,0),([|'B';'B';'B';'B';'B';'B'|],[|'#';'1';'0';'1';'#';'1';'0';'#';'0';'1';'1';'#'|], [|'#';'1';'0';'1';'#';'b'|])))


[<EntryPoint>]
let main args =
    if args.Length = 3 && args[2] = "test" then
        let rules = read_rules(args[0])
        let tapes = read_tape_file(args[1])
        let result = RMT (rules,(1,0),(tapes))
        let result_filename = Path.Combine(Path.GetDirectoryName(args[0]), "result.txt")
        writer.writeCharArrayToFile result_filename result
    else if args.Length = 2 then
        let rules = read_rules(args[0])
        let tapes = read_tape_file(args[1])
        printfn "%A" (RMT (rules,(1,0),(tapes)))
    else
        printfn "Expected 2 arugments - Recieved %A" args.Length
    0