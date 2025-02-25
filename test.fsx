open System.Text.RegularExpressions

let pattern = @"\((\d),\(\((.+)\),\((.+)\),\((.+)\)\),(\d)\)"

let extractGroups input =
    let m = Regex.Match(input, pattern)
    if m.Success then
        [ for i in 1 .. m.Groups.Count - 1 -> m.Groups.[i].Value ]
    else
        []

let test1 = "(1,((0,0),(#,#),(#,b)),2)"
let test2 = "(2,((STAY),(RIGHT),(RIGHT)),3)"

let result1 = extractGroups test1
let result2 = extractGroups test2

printfn "Groups for test1: %A" result1
printfn "Groups for test2: %A" result2
