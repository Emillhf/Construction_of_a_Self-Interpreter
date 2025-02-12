open System.IO

let read_file(filename:string) =
    let lines = File.ReadAllLines(filename)
    let exclamationmark = Array.findIndex(fun elm -> elm = "!") lines
    let pi = Array.findIndex(fun elm -> elm = "π") lines

    let rules = lines[0..exclamationmark-1][0] |> Seq.toArray
    let states = lines[exclamationmark+1..pi-1][0] |> Seq.toArray
    let input = lines[pi+1..][0] |> Seq.toArray
    (rules,input,states)