open Interpreter
open Helper

let clear_state = read_rules("../Expanded_clear_state.txt")
let write_state = read_rules("../Expanded_write_state.txt")

// clear_state - Afprøvning
let result_clear =(RMT (clear_state,(1,0),([|'B';'B'|],[|'#';'1';'1';'#';'B';'B'|], [|'#';'1';'1';'#'|])))
printfn "%A" result_clear
//write_state - Afprøvning
printfn "%A" (RMT (write_state,(1,0),(result_clear)))


