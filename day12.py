num = [2,2,2,2]
tar = 8

for i in num:
        for j in num:
            for k in num:
                for l in num:
                    add = num[i] + num[j] + num[k] + num[l]
                    if tar == add:
                        print([num[i] , num[j] , num[k], num[l]])
        break   


