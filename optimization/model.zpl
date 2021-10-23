param N := 64241; # total number of words
set words := {1 .. N};
set letters := {1 .. 26};
param value[words] := read "..\data\values.txt" as "<1n> 3n";
param o[words*letters] := read "..\data\masks.txt" as "n+";
param b[words*letters] := read "..\data\initials.txt" as "n+";
param a[letters] := read "excerpt_vector.txt" as "<1n> 2n";
param c[letters] := read "title_vector.txt" as "<1n> 2n";

var x[words] binary;
var z;

maximize score: sum<i> in words: value[i] * x[i];
#maximize feasibility: z;

#subto constant: z == 1;

subto excerpt: forall<l> in letters: sum<i> in words: x[i] * o[i,l] == a[l];

subto initials: forall<l> in letters: sum<i> in words: x[i] * b[i,l] == c[l];