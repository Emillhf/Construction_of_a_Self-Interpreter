#load "read_file.fsx"
open System
open System.Text.RegularExpressions

type Replace = char*char
type Move = string

type Operation = Replace of Replace | Move of Move
type Rule = string*(Operation*Operation*Operation)*string


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

let convert_to_rules(rules:array<List<string>>) =
    Array.map(fun (rule:List<string>) -> 
        let s1 = Convert.ToInt32(rule[1],2) |> string
        let s2 = Convert.ToInt32(rule[3] |> Seq.rev |> string,2) |> string
        let operation = 
            match rule[0] with 
                | "M" -> (Move(rule[2][0..2]),Move(rule[2][2..4]),Move(rule[2][4..6]))
                | "S" -> (Replace(rule[2][0..2]),Replace(rule[2][2..4]),Replace(rule[2][4..6]))
                | _ -> failwith "Shits wrong - convert to rules"
        Rule(s1, operation, s2)) rules
    |> Array.toList

let decode_rules(rules:string) = 
    let pattern = @"S#\d+#.{6}#\d+#S|M#\d+#.{6}#\d+#M"
    let matches = Regex.Matches(rules, pattern) |> Seq.map (fun elm -> elm.Value) |> Seq.toArray
    let pattern_single = @"(S|M)#(\d+)#(.{6})#(\d+)#(S|M)$"
    let matchResult = Regex.Match( matches[0], pattern_single)
    
    Array.map(fun (rule:string) -> 
            let matchResult = Regex.Match(rule, pattern_single)
            [matchResult.Groups[1].Value, 
            matchResult.Groups[2].Value, 
            matchResult.Groups[3].Value, 
            matchResult.Groups[4].Value]) matches

let rules, states, input = Read_file.read_file("1_Tape_example.txt")
printfn "%A" (decode_rules(rules[0]))

// let rules_rev, states_rev, input_rev = Read_file.read_file("1_Tape_example_rev.txt")
// printfn "%A" (RMT(convert_to_rules(rules_rev), states_rev, input_rev))
