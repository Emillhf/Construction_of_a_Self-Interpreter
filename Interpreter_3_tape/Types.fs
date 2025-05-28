module Types

type Symbol = (char*char)*(char*char)*(char*char)
type Move = string*string*string

type Operation = Symbol of Symbol | Move of Move
type Rule = int*Operation*int

type tape = array<char>