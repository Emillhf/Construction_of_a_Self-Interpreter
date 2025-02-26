open Interpreter
open Helper
open Readers

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
// printfn "%A" (RMT (apply_symbol,(1,0),apply_symbol_tapes))

// let symbol = read_rules("Expanded_RTM_Programs/symbol_rule.txt")
// let symbol_tapes = read_tape_file("Tapes_RTM/symbol_rule_test.txt")

// printfn "%A" (RMT (symbol,(1,0),symbol_tapes))

//Compare states - Afprøvning
//printfn "%A" (RMT (symbol_rule,(1,0),([|'0';'b'|],[|'#';'1';'0';'#';'0';'1';'#';'1';'0';'#'|], [|'#';'0';'0';'#'|])))
printfn "%A" (RMT (symbol_rule,(1,0),([|'b';'b'|],[|'#';'1';'0';'0';'#';'b';'1';'#';'1';'0';'0';'#'|], [|'#';'1';'0';'#'|])))

//Move Rule - Afprøvning
//printfn "%A" (RMT (move_rule,(1,0),([|'B';'B';'B';'B';'B';'B'|],[|'#';'1';'0';'1';'#';'1';'0';'#';'0';'1';'1';'#'|], [|'#';'1';'0';'1';'#';'b'|])))

