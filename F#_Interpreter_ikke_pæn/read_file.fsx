open System.IO

let read_file(filename:string) =
    let lines = File.ReadAllLines(filename)
    let exclamationmark = Array.findIndex(fun elm -> elm = "!") lines
    let dollar = Array.findIndex(fun elm -> elm = "$") lines

    let input = lines[0..exclamationmark-1][0] |> Seq.toArray
    let rules = lines[exclamationmark+1..dollar-1][0] |> Seq.toArray
    let states = lines[dollar+1..][0] |> Seq.toArray
    (input,rules,states)