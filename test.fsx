

let func(input:array<char>) =
    let input = Array.append [|'b'|] input
    let x = -1
    let func2() =
        let input = Array.append [|'b'|] input
        input
    if x < 0 
    then let input = func2()
         input
    else input

printfn "%A" (func([||]))