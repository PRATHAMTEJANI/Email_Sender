class Solution(object):
    def removeElement(self, nums, val):
        k = 0
        for i in nums:
            if i == val:
                k += 1

        b = len(nums) - k

        arr = [] 

        for i in nums:
            if i != val:
                arr.append(i)
        print(k)
        print(arr + ['_'] * k)







