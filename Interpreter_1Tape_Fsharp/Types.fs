module Types

type Symbol = char*char
type Move = string

type Operation = Symbol of Symbol | Move of Move
type Rule = int*Operation*int

type tape = array<char>