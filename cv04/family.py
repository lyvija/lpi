import os
import sys
sys.path[0:0] = [os.path.join(sys.path[0], '../examples/sat')]
import sat

Howard = 0
George = 1
Virginia = 2
Doroty = 3
mena = ["Howard","George","Virginia","Doroty"]
Ludia = [Howard,George,Virginia,Doroty]
Zeny = [Virginia,Doroty]
Muzi = [Howard,George]

def O(x):
    return 0+x+1
def M(x):
    return 4+x+1
def S(x):
    return 8+x+1
def D(x):
    return 12+x+1
def pp(x,y):
    return 16+4*x+y+1
def st(x,y):
    return 32+4*x+y+1
def ml(x,y):
    return 48+4*x+y+1
a = pp(George, Doroty)
b = st(Howard, George)
c = ml(Virginia, Howard)
d = st(Virginia, Doroty)

def odkoduj(x):
    if(x-1<4):
        return "otec", mena[x-1]
    if(x-1<8 and x-1>3):
        return "matka", mena[x-5]
    if(x-1<12 and x-1>7):
        return "syn", mena[x-9]
    if(x-1<16 and x-1>11):
        return "dcera", mena[x-13]

def hadanka():
    solver = sat.SatSolver()
    w = sat.DimacsWriter("vstup.txt")
    for x in Ludia:
        for y in Ludia:
            if x!=y:
                w.writeImpl(pp(x,y), -O(x))
                w.writeImpl(pp(x,y), -M(y))
                w.writeImpl(pp(x,y), pp(y,x))
            
            #pokrvni pribuzni nie su rodicia pp(x,y) --> -O(x) a -M(y), pp(x,y)-->pp(y,x)
    

    for x in Ludia:
        for y in Ludia:
            if x!=y:
                w.writeImpl(st(x,y), -O(y))
                w.writeImpl(st(x,y), -S(x))
                w.writeImpl(st(x,y), -O(y))
                w.writeImpl(st(x,y), -D(x))
                w.writeImpl(st(x,y), -M(y))
                w.writeImpl(st(x,y), -S(x))
                w.writeImpl(st(x,y), -M(y))
                w.writeImpl(st(x,y), -D(x))
    
#kto je starsi nemoze byt dieta a naopak mladsi nemoze byt rodic st(x,y) --> -O(y) a -S(x)
    for x in Ludia:
        for y in Ludia:
            if x!=y:
                w.writeImpl(ml(x,y), -O(x))
                w.writeImpl(ml(x,y), -S(y))
                w.writeImpl(ml(x,y), -O(x))
                w.writeImpl(ml(x,y), -D(y))
                w.writeImpl(ml(x,y), -M(x))
                w.writeImpl(ml(x,y), -S(y))
                w.writeImpl(ml(x,y), -M(x))
                w.writeImpl(ml(x,y), -D(y))
#kto je starsi nemoze byt dieta a naopak mladsi nemoze byt rodic ml(x,y) --> -O(x) a -S(y)

    for x in Zeny:#zeny nemaju muzsku rolu -O(x) a -S(x)
        w.writeLiteral(-O(x))
        w.writeLiteral(-S(x))
    w.finishClause()
    for y in Muzi:#muzi nemaju zensku rolu -M(y) a -D(y)
        w.writeLiteral(-M(y))
        w.writeLiteral(-D(y))
    w.finishClause()

    for x in Zeny:#kazda zena ma len jednu rolu M(x) --> -D(x) a M(x) v D(x)
        for y in Zeny:
            if x!=y:
                w.writeImpl(M(x), -D(x))
                w.writeImpl(D(x), -M(x))
                w.writeClause([M(y),M(x)])
                w.writeClause([D(y), D(x)])
    for y in Muzi:#kazdy muz ma len jednu rolu O(x) --> -S(x) a O(x) v S(x)
        for x in Muzi:
            if x!=y:
                w.writeImpl(O(y), -S(y))
                w.writeImpl(S(y), -O(y))
                w.writeClause([O(y),O(x)])
                w.writeClause([S(y), S(x)])

    for x in Ludia:#kazdy niekym musi byt O(x) v M(x) v S(x) v D(x)
        w.writeClause([O(x), M(x), S(x), D(x)])
        
    

    w.writeClause([-a, -b, -c])
    w.writeClause([-a, -b, -d])
    w.writeClause([-a, -c, -d])
    w.writeClause([-b, -c, -d])  
    #aspon dve pravdive a najviac dve pravdive
    w.writeClause([a, b, c])
    w.writeClause([a, b, d])
    w.writeClause([a, c, d])
    w.writeClause([b, c, d])

    w.close()
    ok, sol = solver.solve(w,'family_cnf_out.txt')
    pole = []
    i=0
    if ok:
        for x in sol:
            if x > 0 and x<17:
                rola, meno = odkoduj(x)
                pole.append((rola,meno))
                
    return pole

    

a = hadanka()
for dvojica in a:
    print(dvojica[0]+":"+dvojica[1])
    





















        
