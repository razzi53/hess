import cartesian
import os

def create(molecule, trial, h, x1, x1s, x2, x2s):
    temp = """$molecule
0 3
C 0.0 0.0 0.0
C {0} 0.0 0.0
H {1} {2} 0.0
H {3} {4} {5}
H {6} {7} {8}
H {9} {10} {11}
$end

$rem
exchange hf
basis 6-31G*
unrestricted false
spin_flip true
spin_flip_xcis true
cis_triplets false
cis_n_roots 2
boys_cis_numstate 2
cis_loc_state1 1
cis_loc_state2 2
sym_ignore true
max_scf_cycles 300
max_cis_cycles 300
$end
"""
    if(x1==x2 and x1s==2 and x2s==2):
        x1s, x2s = "z", "z"
    else:
        x1s = "n" if x1s==0 else "p"
        x2s = "n" if x2s==0 else "p"
    h = str(h)[1:]
    x1 = "x"+str(x1)
    x2 = "x"+str(x2)
    name = trial[:5]+h+"/"+x1+x1s+"_"+x2+x2s+".in"
    file = open(name, "w")
    file.write(temp.format(*molecule))
    file.close()
    return name[:-3]

def shrink(molecule):
    reduced = []
    reduced.append(molecule[1][0])
    reduced.append(molecule[2][0])
    reduced.append(molecule[2][1])
    for i in range(3, len(molecule)):
        for j in range(3):
            reduced.append(molecule[i][j])
    return reduced

def submit(trial):
    os.system("did.csh -in "+trial+".in -out "+trial+".out")

def run(trial, h):
    molecule = cartesian.intake(trial)
    molecule = shrink(molecule)
    # hessians will be centered
    ##second derivatives of single variables
    for i in range(12):
        mute = molecule
        mute[i] -= h
        trial = create(mute, trial, h, i, 0, i, 0)
        submit(trial)
        mute = molecule
        trial = create(mute, trial, h, i, 2, i, 2)
        submit(trial)
        mute = molecule
        mute[i] += h
        trial = create(mute, trial, h, i, 1, i, 1)
        submit(trial)
    ##moving across the 12 x 11 grid that contains the mixed partial derivatives
    for i in range(12):
        for j in range(11):
            if(j>=i):
                j += 1
            mute = molecule
            mute[i] -= h/4
            mute[j] -= h/4
            trial = create(mute, trial, h, i, 0, j, 0)
            submit(trial)
            mute = molecule
            mute[i] += h/4
            mute[j] -= h/4
            trial = create(mute, trial, h, i, 1, j, 0)
            submit(trial)
            mute = molecule
            mute[i] -= h/4
            mute[j] += h/4
            trial = create(mute, trial, h, i, 0, j, 1)
            submit(trial)
            mute = molecule
            mute[i] += h/4
            mute[i] += h/4
            trial = create(mute, trial, h, i, 1, j, 1)
            submit(trial)
