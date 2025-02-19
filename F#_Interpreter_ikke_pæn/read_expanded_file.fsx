open System.IO
open System.Text.RegularExpressions

type Symbol = (char*char)*(char*char)*(char*char)
type Move = string*string*string

type Operation = Symbol of Symbol | Move of Move
type Rule = int*Operation*int

type tape = array<char>

let first (a,_,_) = a

let seperate_rules_into_states(rules:List<Rule>) = 
    List.sortBy(fun (elm:Rule) -> first elm) rules
    |> List.groupBy(fun (elm:Rule) -> first elm)
    |> List.map(fun elm -> snd elm)

let read_file(filename:string) =
    File.ReadAllLines(filename) |> List.ofArray

let extract_info(rules:List<string>) =
    let pattern = @"\((\d),\(\((.+)\),\((.+)\),\((.+)\)\),(\d)\)"
    List.map(fun rule -> 
        let matches = Regex.Match(rule, pattern)
        let s1 = int(matches.Groups[1].Value)
        let s2 = int(matches.Groups[5].Value)
        let operation =
            match matches.Groups[2].Value.Contains(',') with
                | true -> Symbol((matches.Groups[2].Value[0],matches.Groups[2].Value[2]),
                            (matches.Groups[3].Value[0],matches.Groups[3].Value[2]),
                            (matches.Groups[4].Value[0],matches.Groups[4].Value[2]))
                | false -> Move(matches.Groups[2].Value, matches.Groups[3].Value, matches.Groups[4].Value)
        (s1,operation,s2)
        ) rules

let read_rules(filename:string) =
    read_file(filename)
    |> extract_info
    |> seperate_rules_into_states

//printfn "%A" (read_rules("../Expanded_clear_state.txt"))