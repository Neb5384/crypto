import random

def Prime():
    n = 0
    var = False
    while var == False:
        var = True
        n = random.randint(2, 100)
        for i in range(2, 100):
            if i != n and n % i == 0:
                var = False
    return n
def Rsa():
    p1 = Prime()
    p2 = Prime()
    while p2 == p1:
        p2 = Prime()
    N = p1 * p2
    T = (p1-1) * (p2 - 1)
    E = Prime()
    var = False
    while var == False:
        if E < T and T % E != 0:
            var = True
        else :
            E = Prime()
    while var == True :
        D = random.randint(2, 100)
        Product = D * E
        if Product % T == 1 :
            var = False

