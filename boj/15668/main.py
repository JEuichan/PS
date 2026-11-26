import sys

input = sys.stdin.readline

n = int(input())

def condition(a,b):
    s = str(a) + str(b)
    if len(set(s)) == len(s): return True
    return False 

result = [-1, -1]
for i in range(1, 100000):
    if n < i or n-i <= i: 
        break
    a = n - i
    b = i
    if condition(a,b): 
        result = [a,b]
        break

if sum(result) < 0: 
    print(-1)
else:
    print(str(result[0]) + " + " + str(result[1]))