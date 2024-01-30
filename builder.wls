#!/usr/bin/env wolframscript

x[{u_,v_}] = ToExpression[$ScriptCommandLine[[2]]]
U = ToExpression[$ScriptCommandLine[[3]]]
V = ToExpression[$ScriptCommandLine[[4]]]
div = ToExpression[$ScriptCommandLine[[5]]]

uSplit = Subdivide[U[[1]], U[[2]], div]
vSplit = Subdivide[V[[1]], V[[2]], div]
indices = Subdivide[1, (div+1)^2, (div+1)^2 - 1]
split = Tuples[{uSplit, vSplit}]

unitnormal[x_][u_, v_] = 
    Module[
        {U, V, xu, xv},
        xu = D[x[{U, V}], U];
        xv = D[x[{U, V}], V];
        Nx = Cross[xu, xv] /. {U -> u, V -> v};
        Simplify[ Nx / Norm[Nx] ]
    ]
xN[{u_,v_}] = unitnormal[x][u,v]

pLine[prefix_, {a_,b_,c_}] := 
    Print[
        prefix,
        ToString[ DecimalForm[a] ],
        " ",
        ToString[ DecimalForm[b] ],
        " ",
        ToString[ DecimalForm[c] ]
    ]
vertexLine[{a_,b_,c_}] := pLine["v ", {a,b,c}]
vertexNormalLine[{a_,b_,c_}] := pLine["vn ", {a,b,c}]

(* change? *)
Print["mtllib solids.mtl"]

output := x /@ split //N
vertexLine /@ output

output := xN /@ split //N
vertexNormalLine /@ output

n := div + 1
For[ i=1, i<n, i++,
    For[ j=1, j<n, j++,
        x := j + n (i-1);
        Print["f ", 
            x,"//",x," ",
            x+n,"//",x+n," ",
            x+n+1,"//",x+n+1," ",
            x+1,"//",x+1," "
        ]
    ]
]
