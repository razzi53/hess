import re

def energy(text, state):
    if(state[0]=="d"):
        sre = re.compile("xxDiabaticxx: .*")
        try:
            s = re.search(sre, text).group(0)
        except:
            print(text, state)
        if(state[1]=="0"):
            return float(s.split()[1][:-4])*10
        if(state[1]=="1"):
            return float(s.split()[2][:-4])*10
    else:
        sre = re.compile("Total energy for state   "+str(state)+":    -\d\d\.\d+")
        s = re.search(sre, text).group(0)
        return float(s[31:])
    assert False
    
def run(folder):
    h = float("."+folder[6:])
    doc = "Centered finite-difference hessian with h "+str(h)+":\nS0:\n"
    doc2 = "Centered finite-difference hessian with h "+str(h)+":\nS1:\n"
    #get the diagonal elements
    diagonals = []
    diagonals2 = []
    for i in range(12):
        #starting with negative, then 0, then positive
        trial = folder+"/x"+str(i)+"n_x"+str(i)+"n.out"
        file = open(trial, "r")
        text = file.read()
        ds0n = energy(text, "d0")
        ds1n = energy(text, "d1")
        file.close()
        #zero
        trial = folder+"/x"+str(i)+"z_x"+str(i)+"z.out"
        file = open(trial, "r")
        text = file.read()
        ds0z = energy(text, "d0")
        ds1z = energy(text, "d1")
        file.close()
        #pos
        trial = folder+"/x"+str(i)+"p_x"+str(i)+"p.out"
        file = open(trial, "r")
        text = file.read()
        ds0p = energy(text, "d0")
        ds1p = energy(text, "d1")
        file.close()
        hess = (ds0n - 2*ds0z + ds0p) / (h*h)
        hess2 = (ds1p - 2*ds1z + ds1p) / (h*h)
        diagonals.append(hess)
        diagonals2.append(hess2)
    #the rest: 12*11 = 132
    #pattern:
    #0,1 0,2 0,...
    #1,0, 1,2, 1...    
    rest = []
    rest2 = []
    for i in range(12):
        for j in range(11):
            if(j==i):
                j += 1
            #calculate the relevant value
            #d0pd1p - d0pd1n - d0nd1p + d1nd1n / 4h*h
            trial = folder+"/x"+str(i)+"n_x"+str(j)+"n.out"
            file = open(trial, "r")
            text = file.read()
            ds0nn = energy(text, "d0")
            ds1nn = energy(text, "d1")
            file.close()
            trial = folder+"/x"+str(i)+"p_x"+str(j)+"n.out"
            file = open(trial, "r")
            text = file.read()
            ds0pn = energy(text, "d0")
            ds1pn = energy(text, "d1")
            file.close()
            trial = folder+"/x"+str(i)+"n_x"+str(j)+"p.out"
            file = open(trial, "r")
            text = file.read()
            ds0np = energy(text, "d0")
            ds1np = energy(text, "d1")
            file.close()
            trial = folder+"/x"+str(i)+"p_x"+str(j)+"p.out"
            file = open(trial, "r")
            text = file.read()
            ds0pp = energy(text, "d0")
            ds1pp = energy(text, "d1")
            file.close()
            hess = (ds0nn - ds0pn - ds0np + ds0pp) / (4*h*h)
            hess2 = (ds1nn - ds1pn - ds1np + ds1pp) / (4*h*h)
            rest.append(hess)
            rest2.append(hess2)
    #collect all the data into a 12*12
    for i in range(12):
        for j in range(12):
            if(i==j):
                doc += str(diagonals[i])
                doc2 += str(diagonals2[i])
            else:
                if(j>i):
                    j -= 1
                doc += str(rest[i*11+j])
                doc2 += str(rest2[i*11+j])
            doc += " "
            doc2 += " "
        doc += "\n"
        doc2 += "\n"
    doc += doc2
    file = open("hessian.txt", "w")
    file.write(doc)
    file.close()

print("Name is {}".format(__name__))
if(__name__ == "__main__"):
    run("conic.005")
