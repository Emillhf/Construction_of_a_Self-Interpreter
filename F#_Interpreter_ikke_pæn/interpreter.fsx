#load "read_file.fsx"
open System.Text.RegularExpressions

type Replace = char*char
type Move = string

type Operation = Replace of Replace | Move of Move
type Rule = string*Operation*string


let first (a,_,_) = a
let second (_,b,_) = b
let third (_,_,c) = c

let RMT(rules:List<Rule>, states:array<string>, input:array<char>) =
    let mutable start = states[1]
    let mutable idx = 0

    let write (replace:Replace) = input[idx] <- (snd replace)

    let move (move:Move) =
        match move with 
            | "LEFT" -> idx <- idx - 1
            | "RIGHT" -> idx <- idx + 1
            | _ -> failwith "String wrong"
    
    let check (rule:Operation) =
        match rule with 
            | Move(r) -> true
            | Replace(r) -> input[idx] = (fst r)

    let act (rule:Rule) =
        let R, S2 = second rule, third rule
        match R with 
            | Replace(r) -> write r         
            | Move(r) -> move r
        start <- S2

    let rec search (rules:List<Rule>) =
        match rules with
            | [rule] -> if check(second rule) then act rule
            | rule :: rest -> 
                if (first rule) = start && check (second rule) then act rule
                else search rest
            | _ -> failwith "Shit wrong"

    while not(start = states[2]) do
        search rules
    input

let convert_to_rules(rules:array<string>) =
    let pattern = @"^\((\d+),\(([^)]+)\),\s*(\d+)\)$"
    Array.map(fun (rule:string) -> 
        let matchResult = Regex.Match(rule, pattern)
        let operation = 
            let symbol = matchResult.Groups.[2].Value
            match symbol with 
                | "LEFT" | "RIGHT" -> Move(symbol)
                | _ -> Replace(symbol[0],symbol[2])
        Rule(matchResult.Groups.[1].Value, operation, matchResult.Groups.[3].Value)) rules
    |> Array.toList

let rules, states, input = Read_file.read_file("1_Tape_example.txt")
printfn "%A" (RMT(convert_to_rules(rules), states, input))

let rules_rev, states_rev, input_rev = Read_file.read_file("1_Tape_example_rev.txt")
printfn "%A" (RMT(convert_to_rules(rules_rev), states_rev, input_rev))
