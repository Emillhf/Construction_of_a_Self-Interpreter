open System.IO

type Replace = char*char
type Move = string

type Operation = Replace of Replace | Move of Move
type Rule = string*Operation*string

let read_file(filename:string) =
    let lines = File.ReadAllLines(filename)
    let theta = Array.findIndex(fun elm -> elm = "Φ") lines
    let hashtag = Array.findIndex(fun elm -> elm = "#") lines
    let pi = Array.findIndex(fun elm -> elm = "π") lines

    let rules = lines[theta+1..hashtag-1] |> Array.filter(fun elm -> elm <> "€")
    let states = lines[hashtag+1..pi-1]
    let input = lines[pi+1..][0] |> Seq.toArray |> Array.filter(fun elm -> elm <> '$')
    (rules,states,input)