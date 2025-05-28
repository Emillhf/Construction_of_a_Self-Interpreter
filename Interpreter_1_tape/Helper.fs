module Helper
open Types
open System.IO
open System.Text.RegularExpressions


let first (a,_,_) = a
let second (_,b,_) = b
let third (_,_,c) = c


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

let read_tape(filename:string) = 
    let x = File.ReadAllLines(filename) |> List.ofArray
    x[0] |> Seq.toArray

