#load "read_file.fsx"
open System
open System.Text.RegularExpressions

type Operation = Move of String*String*String | Symbol of string*string*string
type Rule = string*Operation*string

let first (a,_,_) = a
let second (_,b,_) = b
let third (_,_,c) = c

let BinToDec(s:string) = Convert.ToInt32(s,2)
let reverse (s:string) = s |> Seq.rev |> String.Concat

let decode_rules(rules:string) = 
    let string_to_rule (rule:string) = 
        let pattern = @"(S|M)#(\d+)#(.+)#(\d+)#(S|M)"
        let matchResult = Regex.Match(rule, pattern)
        let symbolType = matchResult.Groups.[1].Value // "S" or "M"
        let num1 = matchResult.Groups.[2].Value
        let rawSymbols = matchResult.Groups.[3].Value
        let num2 = matchResult.Groups.[4].Value
        let operation =
            match symbolType with
            | "S" -> Symbol(rawSymbols[0..1], rawSymbols[2..3], rawSymbols[4..5])
            | "M" -> Move(rawSymbols[0..1], rawSymbols[2..3], rawSymbols[4..5])
            | _ -> failwith "When creating rules neither M or S is matched"
        (num1, operation, num2)

    let splitString (input: string) =
        let pattern = @"[SM]#(\d+)#(.+?)#(\d+)#[SM]"
        let matches = Regex.Matches(input, pattern)
        matches |> Seq.cast<Match> |> Seq.map (fun m -> string_to_rule m.Value )  
        |> Seq.toList

    splitString rules


let seperate_rules_into_states(rules:List<Rule>) = 
    let res = List.sortBy(fun (elm:Rule) -> BinToDec(first elm)) rules
            |> List.groupBy(fun (elm:Rule) -> first elm)
            |> List.map(fun elm -> snd elm)
    printfn "%A" 
    res

let RMT(input:array<char>, rules:array<char>, states:array<char>) =
    let rules_tuple = seperate_rules_into_states (decode_rules (String.Concat (rules)))
    let start = 1 //Starting state is always 1
    let final = 0 //Final state is always 0
    let mutable idx1 = 0
    let mutable idx2 = 0
    let mutable idx3 = 0
    let mutable current_state =start
    let write1(replace:char) = input[idx1] <- replace
    let write2(replace:char) = rules[idx2] <- replace
    let write3(replace:char) = states[idx3] <- replace

    let updateCurrentState (newState:int)= current_state <- newState

    let move1 (num:int) = idx1 <- idx1 + num
    let move2 (num:int) = idx2 <- idx2 + num
    let move3 (num:int) = idx3  <- idx3 + num
    
    let check (operation:Operation) =
        match operation with
            | Move(_,_,_) -> 
                true
            | Symbol(a,b,c) -> 
                let res1 = 
                    match a with
                        | "__" -> true
                        | _-> (a[0] = input[idx1])
                let res2 = 
                    match b with
                        | "__" ->  true
                        | _-> (b[0] = rules[idx2]) 
                let res3 = 
                    match c with
                        | "__" -> true
                        | _-> (c[0] = states[idx3])
                res1 && res2 && res3

    let act (rule:Rule) =
        let operation  = second(rule)
        match operation with 
            | Move(t1,t2,t3) -> 
                match t1 with
                    | "__" -> ()
                    | "01" -> move1(1)
                    | "10" -> move1(-1)
                    |_-> failwith "Error when moving "
                match t2 with
                    | "__" -> ()
                    | "01" -> move2(1)
                    | "10" -> move2(-1)
                    |_-> failwith "Error when moving"
                match t3 with               
                    | "__" -> ()
                    | "01" -> move3(1)
                    | "10" -> move3(-1)
                    |_-> failwith "Error when moving"
            | Symbol(a,b,c) -> 
                match a with
                    | "__" -> ()
                    | _-> write1(a[1])
                match b with
                    | "__" -> ()
                    | _-> write2(b[1])
                match c with
                    | "__" -> ()
                    | _-> write3(c[1]) 
        updateCurrentState (BinToDec (reverse (third (rule)))) //Update current_state

    let search (rules_list:List<List<Rule>>) =
        let rec search_rec(rules_state: List<Rule>) = 
            match rules_state with
                | [rule:Rule] -> 
                    if check(second rule) then act rule
                | rule :: rest -> 
                    if check (second rule) then act rule
                    else search_rec rest
                | _ -> failwith "Shit wrong"
        search_rec(rules_list[current_state - 1]) // -1 due to 0 indexing

    while not(current_state = final) do
        search rules_tuple
    
    (input, rules, states)

let input, rules,states = Read_file.read_file("compare_states_enc.txt")
//let rules_tuple = seperate_rules_into_states (decode_rules (String.Concat (rules)))
printfn "%A" (RMT (input, rules, states))

