#!/bin/bash

# "A": 85, "B": 20, "C": 45, "D": 34, "E": 112, "F": 18, "G": 25, "H": 30, "I": 75, "J": 2,
#         "K": 11, "L": 55, "M": 30, "N": 67, "O": 72, "P": 32, "Q": 2, "R": 76, "S": 57, "T": 69,
#         "U": 36, "V": 10, "W": 13, "X": 2, "Y": 18, "Z": 2,

string=""

for i in {1..85}; do string="${string}A"; done
for i in {1..20}; do string="${string}B"; done
for i in {1..45}; do string="${string}C"; done
for i in {1..34}; do string="${string}D"; done
for i in {1..112}; do string="${string}E"; done
for i in {1..18}; do string="${string}F"; done
for i in {1..25}; do string="${string}G"; done
for i in {1..30}; do string="${string}H"; done
for i in {1..75}; do string="${string}I"; done
for i in {1..2}; do string="${string}J"; done
for i in {1..11}; do string="${string}K"; done
for i in {1..55}; do string="${string}L"; done
for i in {1..30}; do string="${string}M"; done
for i in {1..67}; do string="${string}N"; done
for i in {1..72}; do string="${string}O"; done
for i in {1..32}; do string="${string}P"; done
for i in {1..2}; do string="${string}Q"; done
for i in {1..76}; do string="${string}R"; done
for i in {1..57}; do string="${string}S"; done
for i in {1..69}; do string="${string}T"; done
for i in {1..36}; do string="${string}U"; done
for i in {1..10}; do string="${string}V"; done
for i in {1..13}; do string="${string}W"; done
for i in {1..2}; do string="${string}X"; done
for i in {1..18}; do string="${string}Y"; done
for i in {1..2}; do string="${string}Z"; done

echo $string