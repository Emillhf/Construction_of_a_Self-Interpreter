open System.Text.RegularExpressions
open System.IO

let first (a,_,_) = a
let second (_,b,_) = b
let third (_,_,c) = c

type Symbol = char*char
type Move = string

type Operation = Symbol of Symbol | Move of Move
type Rule = int*Operation*int

type tape = array<char>

let RMT(rules:Map<int,list<Rule>>, (start1,final1):int*int,tape:tape, startingIdx:int option) =
    File.WriteAllText("log.txt", "\n")

    let start = start1 //Starting state is always 1
    let final = final1 //Final state is always 0
    let mutable idx = defaultArg startingIdx 0
    let mutable current_state = start
    let mutable previous_state = -1

    let write(symbol:char) = tape[idx] <- symbol

    let updateCurrentState (newState:int) = current_state <- newState

    let move (num:int) = idx <- idx + num
        
    let check (rule:Operation) =
        match rule with 
            | Move(_) -> true
            | Symbol(t1) -> fst t1 = tape[idx]

    let act (rule:Rule) =
        // printfn "%A" rule
        // printfn "%A" tape
        // printfn "%A" idx
        // File.AppendAllText("log.txt", System.String(tape) + "\n")
        // File.AppendAllText("log.txt", "idx: " + idx.ToString() + "\n\n")
        // File.AppendAllText("log.txt", rule.ToString() + "\n")
        
        match second rule with 
            | Move(t1) -> 
                match t1 with
                    | "STAY" -> ()
                    | "RIGHT" -> move(1)
                    | "LEFT" -> move(-1)
                    | _-> failwith "Error when moving "
            | Symbol(t1) -> 
                write(snd t1)

        updateCurrentState (third rule) //Update current_state

    let search (rules_list:Map<int,list<Rule>>) =
        let rec search_rec(rules_state: List<Rule>) = 
            match rules_state with
                | [rule:Rule] -> 
                    if check(second rule) then act rule
                | rule :: rest -> 
                    if check (second rule) then act rule
                    else search_rec rest
                | _ -> failwith "Shit wrong"
        //printfn "%A" current_state
        search_rec(rules_list[current_state])

    while not(current_state = final) do
        if not(previous_state = current_state) then
            previous_state <- current_state
            search rules
        else 
            
            printfn "%A" rules[current_state]
            printfn "%A" (tape,idx, tape[idx])
            printfn "%A" (tape,idx, tape[idx])
            failwith "Rules are wrong in the above state"

    tape

open System.IO


let read_tape_file(filename:string) =
    let lines = File.ReadAllLines(filename)
    let exclamationmark = Array.findIndex(fun elm -> elm = "!") lines
    let dollar = Array.findIndex(fun elm -> elm = "$") lines

    let input = lines[0..exclamationmark-1][0] |> Seq.toArray
    let rules = lines[exclamationmark+1..dollar-1][0] |> Seq.toArray
    let states = lines[dollar+1..][0] |> Seq.toArray
    Array.append (Array.append input rules) states

let String_to_rule(rules:List<string>) =
    let pattern = @"\((\d+),\((.+)\),(\d+)\)"
    List.map(fun rule -> 
        let matches = Regex.Match(rule, pattern)
        let s1 = int(matches.Groups[1].Value)
        let s2 = int(matches.Groups[3].Value)
        let operation =
            match matches.Groups[2].Value.Contains(',') with
                | true -> Symbol((matches.Groups[2].Value[0],matches.Groups[2].Value[2]))
                | false -> Move(matches.Groups[2].Value)
        (s1,operation,s2)
        ) rules

let seperate_rules_into_states(rules:List<Rule>) = 
    List.sortBy(fun (elm:Rule) -> first elm) rules
    |> List.groupBy(fun (elm:Rule) -> first elm)
    |> Map.ofList


let read_rule_file(filename:string) =
    File.ReadAllLines(filename) |> List.ofArray
let read_rules(filename:string) =
    read_rule_file(filename)
    |> String_to_rule
    |> seperate_rules_into_states

let Write_0_or_1 = read_rules("1_Tape_programs/Write_0_or_1.txt")
let Move = read_rules("1_Tape_programs/Move_test.txt")
let rev_Move = read_rules("1_Tape_programs/rev_Move_test.txt")
let clear = read_rules("1_Tape_programs/clear_state.txt")
let rev_clear = read_rules("1_Tape_programs/rev_clear_state.txt")
let write = read_rules("1_Tape_programs/write_state.txt")
let apply_symbol = read_rules("1_Tape_programs/apply_symbol.txt")
let rev_apply_symbol = read_rules("1_Tape_programs/rev_apply_symbol.txt")
let URTM = read_rules("1_Tape_programs/URTM.txt")
// let rev_URTM = read_rules("1_Tape_programs/rev_URTM.txt")
let URTM_ends_on_one = read_rules("1_Tape_programs/URTM_worktape_ends_on_one.txt")
//let rev_URTM_ends_on_one = read_rules("1_Tape_programs/rev_URTM_worktape_ends_on_one.txt")

let rewind = read_rules("1_Tape_programs/rewind_program_tape.txt")
let rewind_final = read_rules("1_Tape_programs/rewind_program_tape_final.txt")
let compare_start_final = read_rules("1_Tape_programs/compare_final_state.txt")

let input_compare_final = [|'O';'b';'!';'p';'#';'0';'1';'#';'0';'1';'#';'0';'1';'#';'$';'H';'1';'1';'#'|]
let input_rewind = [|'p'; 'b'; 'b'; 'b'; 'b';'!';'p'; 'S'; '#'; '1'; '#'; 'B'; 'B'; '#'; '0'; '1'; '#'; 'S'; 'b';'$';'b'; 'b'; 'b'; 'b'; 'H'; 'b'|]
let input_rewind_final = [|'p'; 'b'; 'b'; 'b'; 'b';'!';'p'; 'S'; '#'; '1'; '#'; 'B'; 'B'; '#'; '0'; '1'; '#'; 'S'; 'b';'$';'p'; 'b'; 'b'; 'b'; 'b'; 'b'|]
let input = [|'I';'0';'!';'p';'b';'$';'p';'b'|]
let rev_input = [|'I'; '0'; '!'; 'I'; 'b'; '$'; 'I'; 'b'|]
let input2 = [|'p';'0';'!';'p';'b';'$';'O';'b'|]
let input3 = [|'p';'1';'!';'H';'0';'1';'#';'0';'1';'#';'$';'H';'0';'1';'#';|]
let rev_clear_input = [|'p'; '1'; '!'; '#'; '0'; '1'; 'H'; '0'; '1'; '#'; '$'; 'b'; 'b'; 'b'; 'p'|]
let input_apply = [|'O';'b';'!';'H';'0';'1';'#';'0';'1';'#';'0';'1';'#';'$';'H';'0';'1';'#';|]
let rev_input_apply = [|'I';'b';'!';'H';'0';'1';'#';'0';'1';'#';'0';'1';'#';'$';'H';'0';'1';'#';|]

let input_URTM = [|'b';'b';'$';'p';'1';'0';'$';'p';'M';'#';'1';'#';'0';'1';'#';'0';'1';'#';'M';'S';'#';'1';'0';'#';'1';'B';'#';'0';'#';'S';'b';'$';'p';'$';'b';'b';'b';'b';'b'|]
let input_rev_URTM = [|'p';'b';'!';'p';'M';'#';'1';'#';'1';'0';'#';'0';'1';'#';'M';'S';'#';'1';'0';'#';'1';'B';'#';'0';'#';'S';'b';'$';'b';'b';'p';'b';'b';'b';'b';'b'|]


let input_test_infinate_one_long = [|'b';'$';'I';'$';'p';'$';'I';'$';'b'|] //STARTING IDX CHANGED TO 4
let input_test_infinate_case1 = [|'b';'$';'1';'1';'O';'$';'p';'$';'I';'1';'0';'0';'$';'b'|] //STARTING IDX CHANGED TO 4
let rev_input_test_infinate_case1 = [|'$';'1';'1';'0';'p';'$';'p';'$';'p';'1';'1';'0';'0';'$'|]
let input_test_infinate_case2 = [|'b';'$';'1';'I';'0';'$';'p';'$';'1';'I';'0';'$';'b'|] //STARTING IDX CHANGED TO 3
let rev_input_test_infinate_case2 =[|'b'; '$'; '1'; '1'; 'O'; '$'; 'p';'$'; 'I'; '1'; '0'; '$';'b'|]
let input_test_infinate_case3 = [|'b';'$';'p';'0';'1';'$';'p';'$';'1';'0';'p';'$';'b'|] //STARTING IDX CHANGED TO 2
let rev_input_test_infinate_case3 =[|'b';'b'; '$'; 'O'; '1'; '$'; 'p';'$';'1';'O';'$';'b';'b'|]
let input_test_infinate_case4 = [|'b';'$';'I';'0';'1';'$';'p';'$';'1';'0';'I';'$';'b'|]  //STARTING IDX CHANGED TO 2
let rev_input_test_infinate_case4 = [|'b'; '$'; '1'; 'O'; '1'; '$'; 'p'; '$'; '1'; 'O'; '1'; '$';'b'|] 
let input_test_infinate_case5 = [|'b';'$';'1';'1';'O';'1';'1';'1';'$';'p';'$';'1';'1';'O';'1';'1';'1';'$';'b'|] //STARTING IDX CHANGED TO 3
let rev_input_test_infinate_case5 = [|'b'; '$';'1'; '1'; '0'; 'I'; '1';'1'; '$'; 'p'; '$';'1'; 'I'; '0'; '1'; '1';'1'; '$';'b'|]
let test_infinate_case_right = read_rules("1_Tape_programs/move_right_t1_left_t3.txt")
let rev_test_infinate_case_right = read_rules("1_Tape_programs/rev_move_right.txt")
let test_infinate_case_left = read_rules("1_Tape_programs/move_left_t1_right_t3.txt")

printfn "%A" (RMT (test_infinate_case_right, (1,293), input_test_infinate_one_long, Some 2)) 


printfn "%A" (RMT (test_infinate_case_right, (1,293), input_test_infinate_case1, Some 4)) 
// // printfn "%A" (RMT (rev_test_infinate_case_right, (292,1), rev_input_test_infinate_case1, Some 4) = input_test_infinate_case1) 
printfn "%A\n" (RMT (test_infinate_case_left, (1,293), rev_input_test_infinate_case1, Some 4))  


printfn "%A" (RMT (test_infinate_case_right, (1,293), input_test_infinate_case2, Some 4)) 
// // printfn "%A" (RMT (rev_test_infinate_case_right, (292,1), rev_input_test_infinate_case2, Some 4) = input_test_infinate_case2) 
printfn "%A\n" (RMT (test_infinate_case_left, (1,292), rev_input_test_infinate_case2, Some 4)) 

printfn "%A" (RMT (test_infinate_case_right, (1,292), input_test_infinate_case3, Some 3))
// // printfn "%A" (RMT (rev_test_infinate_case_right, (292,1), rev_input_test_infinate_case3, Some 3)  = input_test_infinate_case3) 
printfn "%A\n" (RMT (test_infinate_case_left, (1,292), rev_input_test_infinate_case3, Some 3)) 

printfn "%A" (RMT (test_infinate_case_right, (1,292), input_test_infinate_case4, Some 3)) 
// // printfn "%A" (RMT (rev_test_infinate_case_right, (292,1), rev_input_test_infinate_case4, Some 3) = input_test_infinate_case4) 
printfn "%A\n" (RMT (test_infinate_case_left, (1,292), rev_input_test_infinate_case4, Some 3)) 

printfn "%A" (RMT (test_infinate_case_right, (1,292), input_test_infinate_case5, Some 5))
// // printfn "%A" (RMT (rev_test_infinate_case_right, (292,1), rev_input_test_infinate_case5, Some 5) = input_test_infinate_case5) 
printfn "%A" (RMT (test_infinate_case_left, (1,292), rev_input_test_infinate_case5, Some 5)) 

let bin_inc = [|'b';'b';'b';'b';'$';'p';'0';'0';'1';'1';
                    '$';
                    'p';'S';'#';'1';'#';'B';'B';'#';'0';'1';'#';'S';'M';'#';'1';'0';'#';'0';'1';'#';'1';'1';'#';'M';'S';'#';'1';'1';'#';'0';'1';'#';'0';'0';'1';'#';'S';'S';'#';'1';'1';'#';'1';'0';'#';'0';'1';'#';'S';'S';'#';'1';'1';'#';'B';'B';'#';'0';'0';'1';'#';'S';'M';'#';'1';'0';'0';'#';'1';'0';'#';'1';'0';'1';'#';'M';'S';'#';'1';'0';'1';'#';'0';'0';'#';'0';'0';'1';'#';'S';'S';'#';'1';'0';'1';'#';'B';'B';'#';'0';'#';'S';'b';
                    '$';
                    'p';'$';'b';'b';'b';'b';'b';'b';'b';'b';'b';'b';'b';'b';'b';'b';
                |]
// printfn "%A" (RMT (Move,(1,42),input))
// printfn "%A" (RMT (rev_Move,(42,1),rev_input))
//printfn "%A" (RMT (rev_Move,(25,1),RMT (Move,(1,25),input)))

// printfn "%A" (RMT (Write_0_or_1,(1,187),input2))
//printfn "%A" (RMT (clear,(1,311),input3))
// printfn "%A" res
//printfn "%A" (RMT (rev_clear,(311,1),rev_clear_input))
// printfn "%A" (RMT (write,(1,430), res))
//printfn "%A" (RMT (apply_symbol,(1,547),input_apply))
// printfn "%A" (RMT (rev_apply_symbol, (547,1), rev_input_apply))

//printfn "%A" (RMT (URTM,(1,9678),input_URTM, None))

//printfn "%A" (RMT (URTM,(1,29518),input_URTM, Some 5))
//printfn "%A" (RMT (rev_URTM,(14544,1),RMT (URTM,(1,14544),input_URTM)))
printfn "%A" (RMT (rev_URTM,(29518,1),bin_inc, Some 5))
//printfn "%A" (RMT (rev_URTM,(29518,1),input_rev_URTM, Some 5))
// printfn "%A" (RMT (rev_URTM_ends_on_one,(14460,1),input_rev_URTM))

// printfn "%A" (RMT (Move,(1,34),input))
// printfn "%A" (RMT (Write_0_or_1,(1,187),input2))

//printfn "%A" (RMT (rewind,(1,579),input_rewind))
//printfn "%A" (RMT (rewind_final,(1,579),input_rewind_final))

//printfn "%A" (RMT (compare_start_final,(1,536),input_compare_final))