import os, sys

import io
import hessian

if __name__ == "__main__":
    if(len(sys.argv)==3):
        txt = sys.argv[1]
        h = float(sys.argv[2])
    else:
        txt = raw_input("What's the file name? >>> ")
        h = input("What's the finite differences constant, h? >>> ")
    folder = txt[:5] + str(h)[1:]
    os.system("mkdir "+folder)
    io.run(txt, h)
    hessian.run(folder)
