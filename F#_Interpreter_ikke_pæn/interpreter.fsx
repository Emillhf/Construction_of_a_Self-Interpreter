#load "read_file.fsx"
open System
open System.Text.RegularExpressions

type Rule = string*(string*string*string)*string

let first (a,_,_) = a
let second (_,b,_) = b
let third (_,_,c) = c

let BinToDec(s:string) = Convert.ToInt32(s)
let RMT(rules:List<list<Rule>>,input:array<char>,states:array<string>) =
    let start = int(states[1])
    let final = int(states[2])
    let mutable current_state = int(states[0])
    let mutable idx1 = 0
    let mutable idx2 = 0

    let write1(replace:string) = failwith "Something wrong"
    let write2(replace:string) = input[idx2] <- replace[1] 
    let write3(replace:int) = current_state <- replace

    let move1 (move:string, num) = idx1 <- idx1 + num
    let move2 (move:string, num) = idx2 <- idx2 + num
    let move3 (move:string, num) = current_state <- current_state + num
    
    let check (rule:String*String*String) =
        let result1= 
            match first rule with
                | "__" -> true
                | "$$" | "€€" -> true
                | _ -> false
        let result2 = 
            match second rule with
                | "__" -> true
                | "$$" | "€€" -> true
                | _ -> (second rule)[0] = input[idx2]

        result1 && result2

    let act (rules:Rule) =
        let rule = second(rules)
        match first rule with 
            | "__" -> ()
            | "$$" -> move1(first rule,-1)
            | "€€" -> move1(first rule,1)
            | _ -> write1(first rule)
        match second rule with 
            | "__" -> ()
            | "$$" -> move2(second rule,-1)
            | "€€" -> move2(second rule,1)
            | _ -> write2(second rule)
        write3(BinToDec(third(rules)))

    let search (rules:List<List<Rule>>) =
        let rec search_rec(rules_state: List<Rule>) = 
            match rules_state with
                | [rule:Rule] -> if check(second rule) then act rule
                | rule :: rest -> 
                    if check (second rule) then act rule
                    else search_rec rest
                | _ -> failwith "Shit wrong"
        search_rec(rules[current_state - 1])

    while not(current_state = final) do
        search rules
    input

let decode_rules(rules:string) = 
    let rules_seperated = Array.filter(fun (elm:string) -> elm.Length > 0) (rules.Split([|'M';'S'|])) |> Array.toList
    List.map(fun (elm : string)-> 
        elm.Split('#')) rules_seperated 


let seperate_rules_into_states(rules:List<Rule>) = 
    List.groupBy(fun (elm:Rule) -> first elm) rules 
    |> List.map(fun elm -> snd elm)

let rules, input,states = Read_file.read_file("1_Tape_example.txt")
printfn "%A" (decode_rules(rules[0]))

