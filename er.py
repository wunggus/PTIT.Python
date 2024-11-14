with open('DaySoINP.txt', 'r') as f:
    N = int(f.readline().strip())
    a = list(map(int,f.readline().split()))
    p = [n for n in a if n % 2 ==0]
with open('DaySoOUT.txt','w') as f:
    f.write(" ".join(map(str,p)))