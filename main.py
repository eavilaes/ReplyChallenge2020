import sys
import copy

class Developer:
    def __init__(self, id, company, bonus, skills):
        self.id = id
        self.company = company
        self.bonus = bonus
        self.skills = skills
        self.dev1 = None
        self.dev2 = None
        self.dev1aff = 0
        self.dev2aff = 0
        self.r=-1
        self.c=-1
    def workPotential(self, dev2):
        wp=0
        for s in self.skills:
            for n in dev2.skills:
                if s==n:
                    wp+=1
        return ((len(self.skills)+len(dev2.skills))-wp*2)*wp
    def bonusPoints(self, dev2):
        if self.company==dev2.company:
            return self.bonus*dev2.bonus
        return 0

class Manager:
    def __init__(self, id, company, bonus):
        self.id = id
        self.company = company
        self.bonus = bonus
        self.r=-1
        self.c=-1

def calculateAffinity(devs):
    t=1
    for d in devs:
        for n in devs:
            if d != n:
                saved = False
                aff = d.workPotential(n)+d.bonusPoints(n)
                if aff >= d.dev1aff:
                    d.dev2 = d.dev1
                    d.dev2aff = d.dev1aff
                    
                    d.dev1 = n
                    d.dev1aff = aff
                    saved = True
                if not saved and aff >= d.dev2aff:
                    d.dev2 = n
                    d.dev2aff = aff
                    saved = True
        print("a {}/{}".format(t,len(devs)))
        t+=1

#Main code
_in = open(str(sys.argv[1]), "r")
out = open(str(sys.argv[1])[:-4]+".out", "w")

W, H = _in.readline().split(" ")
W = int(W)
H = int(H)

# office = [[]*W for _ in (H)]
office = [[0 for x in range(W)] for y in range(H)]
for y in range(0,H):
    line = _in.readline()
    for x in range(0,W):
        office[y][x] = line[x]


nDevelopers = int(_in.readline())
developers = []
for i in range(0,nDevelopers):
    line = _in.readline().split(" ")
    skills = []
    for n in range(0, int(line[2])):
        skills.append(line[3+n])
    d = Developer(i, line[0], int(line[1]), skills)
    developers.append(d)

nManagers = int(_in.readline())
managers = []
for i in range(0, nManagers):
    line = _in.readline().split(" ")
    m = Manager(i, line[0], int(line[1]))
    managers.append(m)

## algorithms
calculateAffinity(developers)
developers.sort(key=lambda p: p.dev1aff+p.dev2aff, reverse=True)

# for d in developers:
#     print("Id:{} - Dev1:{} ({}) - Dev2:{} ({})".format(d.id,d.dev1.id,d.dev1aff,d.dev2.id,d.dev2aff))

otrosDevs = copy.copy(developers)
otrosDevs.sort(key=lambda s: s.id)
otrosManagers = copy.copy(managers)
otrosManagers.sort(key=lambda n: n.id)

print("aqui")
result = [[0 for x in range(W)] for y in range(H)]
for r in range(len(office)):
    for c in range(len(office[0])):
        if(office[r][c]=="_"):
            idx = otrosDevs.index(developers[0])
            otrosDevs[idx].r=r
            otrosDevs[idx].c=c
            result [r][c] = developers.pop(0)
            inserted=False
            if c<W-1 and result [r][c+1] == "" and office [r][c+1] == "_":
                result[r][c+1]=result[r][c].dev1
                idx = otrosDevs.index(result[r][c].dev1)
                otrosDevs[idx].r=r
                otrosDevs[idx].c=c+1
                developers.remove(result[r][c].dev1)
                inserted=True
            elif c<W-1 and result[r][c+1] == "" and office [r][c+1] == "M":
                for m in managers:
                    if m.company == result[r][c].company:
                        result[r][c+1]=m
                        idx = otrosManagers.index(m)
                        otrosManagers[idx].r=r
                        otrosManagers[idx].c=c+1
                        managers.remove(m)
                        break
            if r<H-1 and result [r+1][c] == "" and office [r][c+1] == "_":
                if not inserted:
                    result[r+1][c] = result[r][c].dev1
                    idx = otrosDevs.index(result[r][c].dev1)
                    otrosDevs[idx].r=r+1
                    otrosDevs[idx].c=c
                    developers.remove(result[r][c].dev1)
                else:
                    result[r+1][c] = result[r][c].dev2
                    idx = otrosDevs.index(result[r][c].dev2)
                    otrosDevs[idx].r=r+1
                    otrosDevs[idx].c=c
                    developers.remove(result[r][c].dev2)
            elif r<H-1 and result[r+1][c] == "" and office [r+1][c] == "M":
                for m in managers:
                    if m.company == result[r][c].company:
                        result[r+1][c]=m
                        idx = otrosManagers.index(m)
                        otrosManagers[idx].r=r+1
                        otrosManagers[idx].c=c
                        managers.remove(m)
                        break
            #calculateAffinity(developers)
        print("     Dc {}/{}".format(c,len(office[0])))
    print("Dr {}/{}".format(r,len(office)))

for r in range(len(office)):
    for c in range(len(office[0])):
        if office[r][c] == "M" and len(managers)>0:
            idx = otrosManagers.index(managers[0])
            otrosManagers[idx].r=r
            otrosManagers[idx].c=c
            result[r][c] = managers.pop(0)
        print("     Mc {}/{}".format(c,len(office[0])))
    print("Mr {}/{}".format(r,len(office)))


for d in otrosDevs:
    if(d.c != -1 and d.r != -1):
        out.write("{} {}\n".format(d.c, d.r))
    else:
        out.write("X\n")
for m in otrosManagers:
    if(m.c != -1 and m.r != -1):
        out.write("{} {}\n".format(m.c, m.r))
    else:
        out.write("X\n")

out.close()
_in.close()
