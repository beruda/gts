#!/usr/bin/env wolframscript

x[{u_,v_}] = ToExpression[$ScriptCommandLine[[2]]]
U = ToExpression[$ScriptCommandLine[[3]]]
V = ToExpression[$ScriptCommandLine[[4]]]
div = ToExpression[$ScriptCommandLine[[5]]]

uSplit = Subdivide[U[[1]], U[[2]], div]
vSplit = Subdivide[V[[1]], V[[2]], div]
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

Print[split]
Print[" "]
Print[x /@ split //N]
Print[" "]
Print[xN /@ split //N]