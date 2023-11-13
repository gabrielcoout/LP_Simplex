# LP_Simplex
Simplex implementation in Python (using Numpy) for Linear Optimization class 2023.

$ curl -O https://netlib.org/lp/data/emps.c
$ cc -O -o emps emps.c
$ curl -O "https://netlib.org/lp/infeas/{bgdbg1,bgetam,bgindy,bgprtr,box1,\
ceria3d,chemcom,cplex1,cplex2,ex72a,ex73a,forest6,galenet,gosh,gran,greenbea,\
itest2,itest6,klein1,klein2,klein3,mondou2,pang,pilot4i,qual,reactor,refinery,\
vol1,woodinfe}".
$ for f in bgdbg1 bgetam bgindy bgprtr box1 ceria3d chemcom cplex1 cplex2 \
   ex72a ex73a forest6 galenet gosh gran greenbea itest2 itest6 klein1 klein2 \
   klein3 mondou2 pang pilot4i qual reactor refinery vol1 woodinfe; do
   ./emps "${f}" > "${f}.mps"
done