#hurlde challenge complete.
#indetation in python.
#learn "WHILE-LOOP"   
import random

words = ["pypthppon"]
var   = random.choice(words)

place = ""
for pos in range(1,len(var)):
    place += "_"
print(place)


display = ""
print("enter a worlds tocheck you are win or not")
num = input("Guess the word").lower()

display = ""

for let in var:
    if let == num:
        display += let
    else:
        display += "_"

print(display)