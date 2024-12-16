module Interpreter

open tuple_3D

type Replace = char*char
type Move = string

type Operation = Replace of Replace | Move of Move
type Rule = int*Operation*int

// type tapes = string*List<Rule>*int
type tapes = string*unit*unit

let RMT(rules:List<Rule>, (start,final):int*int, tapes:tapes) =
    let mutable S = start
    let mutable idx = 0
    let mutable t1 = (first tapes) |> Seq.toArray

    let write (replace:Replace) = t1[idx] <- (snd replace)

    let move (move:Move) =
        match move with 
            | "LEFT" -> idx <- idx - 1
            | "RIGHT" -> idx <- idx + 1
            | _ -> failwith "String wrong"
    
    let check (rule:Operation) =
        match rule with 
            | Move(r) -> true
            | Replace(r) -> t1[idx] = (fst r)

    let act (rule:Rule) =
        let R, S2 = second rule, third rule
        match R with 
            | Replace(r) -> write r         
            | Move(r) -> move r
        S <- S2

    let rec search (rules:List<Rule>) =
        match rules with
            | [rule] -> if check(second rule) then act rule
            | rule :: rest -> 
                if (first rule) = S && check (second rule) then act rule
                else search rest
            | _ -> failwith "Shit wrong"

    while not(S = final) do
        search rules
    t1

