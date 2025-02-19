open Interpreter
open Helper

let clear_state = read_rules("../Expanded_clear_state.txt")

printfn "%A" (RMT (clear_state,(1,0),([|'B';'B'|],[|'#';'1';'1';'#';'B';'B'|], [|'#';'1';'1';'#'|])))

