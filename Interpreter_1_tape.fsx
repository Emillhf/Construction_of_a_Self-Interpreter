open System.Text.RegularExpressions
let first (a,_,_) = a
let second (_,b,_) = b
let third (_,_,c) = c

type Symbol = char*char
type Move = string

type Operation = Symbol of Symbol | Move of Move
type Rule = int*Operation*int

type tape = array<char>

let RMT(rules:Map<int,list<Rule>>, (start1,final1):int*int,tape:tape) =
    let start = start1 //Starting state is always 1
    let final = final1 //Final state is always 0
    let mutable idx = 0
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
        // printfn "%A" (idx1, idx2, idx3)
        // printfn "%A" (rule)
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
        printfn "%A" current_state
        search_rec(rules_list[current_state])

    while not(current_state = final) do
        if not(previous_state = current_state) then
            previous_state <- current_state
            search rules
        else 
            
            printfn "%A" rules[current_state]
            printfn "%A" (tape,idx)
            failwith "Rules are wrong in the above state"
    // printfn "%A" (idx1, idx2, idx3) 
    tape

open System.IO

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

let program = read_rules("1_Tape_programs/Write_0_or_1.txt")

let input = [|'p';'0';'!';'p';'b';'$';'p';'b'|]

printfn "%A" (RMT (program,(1,0),input))