module Interpreter
open Types
open Helper
open System.IO

let RMT(rules:Map<int,list<Rule>>, (start1,final1):int*int,tape:tape, startingIdx:int option) =
    let start = start1
    let final = final1
    let mutable idx = defaultArg startingIdx 0
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
        // printfn "%A" rule
        // printfn "%A" tape
        // printfn "%A" idx
        // File.AppendAllText("log.txt", System.String(tape) + "\n")
        // File.AppendAllText("log.txt", "idx: " + idx.ToString() + "\n\n")
        // File.AppendAllText("log.txt", rule.ToString() + "\n")
        
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
        // printfn "%A" (current_state, (tape,idx, tape[idx]))
        search_rec(rules_list[current_state])

    while not(current_state = final) do

        if not(previous_state = current_state) then
            previous_state <- current_state
            search rules
        else 
            
            printfn "%A" rules[current_state]
            printfn "%A" (tape,idx, tape[idx])
            failwith "Rules are wrong in the above state"

    tape