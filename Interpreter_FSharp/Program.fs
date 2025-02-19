open Interpreter
open Helper

// let clear_state = read_rules("../Expanded_clear_state.txt")
// let write_state = read_rules("../Expanded_write_state.txt")
// let clear_and_write = read_rules("../Expanded_clear_and_write.txt")
let compare_state = read_rules("../Expanded_compare_states.txt")

// clear_state - Afprøvning
// let result_clear =(RMT (clear_state,(1,0),([|'B';'B'|],[|'#';'1';'1';'#';'B';'B'|], [|'#';'1';'1';'#'|])))
// printfn "%A" result_clear
//write_state - Afprøvning
//printfn "%A" (RMT (write_state,(1,0),(result_clear)))

//printfn "%A" (RMT (clear_and_write,(1,0),([|'B';'B'|],[|'#';'0';'1';'#';'0';'1';'#';'B'|], [|'#';'0';'1';'#';'B'|])))

//Compare states - Afprøvning
printfn "%A" (RMT (compare_state,(1,0),([|'B';'B'|],[|'#';'1';'0';'1';'#';'B';'B';'B'|], [|'#';'1';'0';'0';'#'|])))


