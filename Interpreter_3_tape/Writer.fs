module writer

open System
open System.IO

let writeCharArrayToFile (filePath: string) (charArrays: char [] * char [] * char []) =
    let (A1, A2, A3) = charArrays
    use writer = new StreamWriter(filePath, false)
    writer.WriteLine(A1)
    writer.WriteLine("!")
    writer.WriteLine(A2)
    writer.WriteLine("$")
    writer.WriteLine(A3)