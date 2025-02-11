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
let RMT(rules:List<list<Rule>>,input:array<char>,states:array<string>) =
    let start = states[1]
    let final = states[2]
    let mutable idx1 = 0
    let mutable idx2 = 0
    let mutable current_state = int(states[0])

    let write1(replace:string) = failwith "Something wrong"
    let write2(replace:string) = input[idx2] <- replace[1] 
    let write3(replace:int) = current_state <- replace

    let move1 (move:string, num) = idx1 <- idx1 + num
    let move2 (move:string, num) = idx2 <- idx2 + num
    //let move3 (move:string, num) = idx3  <- idx3 + num
    
    let check (operation:Operation) =
        match operation with
                | Move(_,_,_) -> true
                | Symbol(a,b,c) -> b[0] = input[idx2]

    let act (rules:Rule) =
        let rule  = second(rules)
        printfn "%A" rule
        match rule with 
            | Move(t1,t2,t3) -> 
                match t1 with
                    | "__" -> ()
                    | "01" -> move1(t1,1)
                    | "10" -> move1(t1,-1)
                match t2 with
                    | "__" -> ()
                    | "01" -> move2(t2,1)
                    | "10" -> move2(t2,-1)
                // match t3 with               
                //     | "__" -> ()
                //     | "$$" -> move3(t3,1)
                //     | "€€" -> move3(t3,-1)
            | Symbol(a,b,c) -> 
                match a with
                    | "__" -> ()
                    | _-> write1(a)
                match b with
                    | "__" -> ()
                    | _-> write2(b)
                // match c with         Perhaps not nessesary
                //     | "__" -> ()
                //     | _-> write3(c) 
            // | "__" -> () 
            // | "$$" -> move1(first rule,-1)
            // | "€€" -> move1(first rule,1)
            // | _ -> write1(first rule)
        // match second rule with 
        //     | "__" -> ()
        //     | "$$" -> move2(second rule,-1)
        //     | "€€" -> move2(second rule,1)
        //     | _ -> write2(second rule)
        write3(BinToDec (reverse (third (rules)))) //Update current_state
        

    let search (rules:List<List<Rule>>) =
        let rec search_rec(rules_state: List<Rule>) = 
            match rules_state with
                | [rule:Rule] -> 
                    printfn "%A" rule
                    if check(second rule) then act rule
                | rule :: rest -> 
                    if check (second rule) then act rule
                    else search_rec rest
                | _ -> failwith "Shit wrong"
        search_rec(rules[current_state - 1]) // -1 due to 0 indexing

    while not(current_state = int(final)) do
        search rules
    input

let decode_rules(rules:string) = 
    let string_to_rule (rule:string) = 
        let pattern = @"(S|M)#(\d+)#([^#]+)#(\d+)#(S|M)"
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
        let pattern = @"[MS][^MS]+[MS]"
        let matches = Regex.Matches(input, pattern)
        matches |> Seq.cast<Match> |> Seq.map (fun m -> string_to_rule m.Value )  
        |> Seq.toList
    splitString rules

let seperate_rules_into_states(rules:List<Rule>) = 
    List.groupBy(fun (elm:Rule) -> first elm) rules 
    |> List.map(fun elm -> snd elm)

let rules, input,states = Read_file.read_file("1_Tape_example.txt")
printfn "%A" (RMT (seperate_rules_into_states (decode_rules(rules[0])), input, states))


