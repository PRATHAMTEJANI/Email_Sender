arr  = [1,2,4,6,5,8,2,1]
tar  = 4

for i in range(len(arr)):
    if i == tar:
        add = arr[i-1] + arr[i] + arr[i+1]
        print(add)
    

