#load "read_file.fsx"
open System
open System.Text.RegularExpressions

type Rule = string*(string*string*string)*string

let first (a,_,_) = a
let second (_,b,_) = b
let third (_,_,c) = c

let RMT(rules:List<List<Rule>>,input:array<char>,states:array<string>) =
    let start = states[1]
    let final = states[2]
    let mutable idx1 = 0
    let mutable idx2 = 0
    let mutable idx3 = 0

    let write1(replace:string) = failwith "Something wrong"
    let write2(replace:string) = input[idx2] <- replace[1] 
    let write3(replace:string) = states[idx3] <- replace[1] |> string

    let move1 (move:string, num) = idx1 <- idx1 + num
    let move2 (move:string, num) = idx2 <- idx2 + num
    let move3 (move:string, num) = idx3 <- idx3 + num
    
    let check (rule:String*String*String) =
        let result1= 
            match first rule with
                | "__" -> true
                | "LL" | "RR" -> true
                | _ -> false
        let result2 = 
            match second rule with
                | "__" -> true
                | "LL" | "RR" -> true
                | _ -> (second rule)[0] = input[idx2]
        let result3 =
            match third rule with
                | "__" -> true
                | "LL" | "RR" -> true
                | _ -> ((third rule)[0] |> string) = states[idx3]
        result1 && result2 && result3

    let act (rule:String*String*String) =
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
        match third rule with 
            | "__" -> ()
            | "$$" -> move3(third rule,-1)
            | "€€" -> move3(third rule,1)
            | _ -> write3(third rule)

    let search (rules:List<List<Rule>>) =
        let rec search_rec(rules_state: List<Rule>) = 
            match rules_state with
                | [rule:Rule] -> if check(second rule) then act (second rule)
                | rule :: rest -> 
                    if check (second rule) then act (second rule)
                    else search_rec rest
                | _ -> failwith "Shit wrong"

        search_rec(rules[int(states[0])])

    while not(start = final) do
        search rules
    input

// let convert_to_rules(rules:array<List<string>>) =

let decode_rules(rules:string) = 
    Array.filter(fun (elm:string) -> elm.Length > 0) (rules.Split('#')) 


let rules, input,states = Read_file.read_file("1_Tape_example.txt")
printfn "%A" (decode_rules(rules[0]))

// let rules_rev, states_rev, input_rev = Read_file.read_file("1_Tape_example_rev.txt")
// printfn "%A" (RMT(convert_to_rules(rules_rev), states_rev, input_rev))
