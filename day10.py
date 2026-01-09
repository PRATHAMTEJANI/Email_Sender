# Input: s = "abcabcbb"
# Output: 3
# Explanation: The answer is "abc", with the length of 3. Note that "bca" and "cab" are also correct answers.


arr = [1,2,4,2,3,2,1,2,4,5]

result = []
for i in arr:
    if i not in result:
        result.append(i)
print(len(result))