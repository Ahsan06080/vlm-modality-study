"""T19 check: nested GLMM (+ (1 | item_id:model)) quadrature accuracy, 25 x 25 vs 35 x 35 nodes, run 1.
Output: results/analysis/glmm_t19_nested_quadrature_check.csv. Run: .venv/bin/python scripts/analysis/glmm_t19_quadcheck.py"""
import numpy as np
import pandas as pd
import patsy
from scipy import optimize

from vmod.analyze import load_scored, write_csv
from vmod.glmm_t19 import PRIMARY, PRIMARY_RUNS, NestedGHGLMM, clean, prep, terms

d = prep(load_scored(PRIMARY_RUNS[1]))
d = d[d.model.isin(PRIMARY)].reset_index(drop=True)
X = patsy.dmatrix(terms("Qwen2.5-VL-7B")["full"], d, return_type="dataframe")
grp = (d.item_id + "|" + d.model).values
fits = {}
for k in (25, 35):
    m = NestedGHGLMM(X.values, d.y.values, d.item_id.values, grp, k, k)
    start = np.zeros(X.shape[1] + 2) if k == 25 else fits[25].x
    fits[k] = optimize.minimize(m.nll, start, jac=m.grad, method="L-BFGS-B", options=dict(maxiter=10000, gtol=1e-6, ftol=1e-14))
names = [clean(c, "Qwen2.5-VL-7B") for c in X.columns] + ["sd(item_id)", "sd(item_id:model)"]
t = pd.DataFrame(dict(term=names, est_25x25=fits[25].x, est_35x35=fits[35].x))
t.loc[t.term.str.startswith("sd("), ["est_25x25", "est_35x35"]] = np.exp(t.loc[t.term.str.startswith("sd("), ["est_25x25", "est_35x35"]])
t["abs_diff"] = (t.est_25x25 - t.est_35x35).abs()
t["loglik_25x25"], t["loglik_35x35"] = -fits[25].fun, -fits[35].fun
write_csv(t, "glmm_t19_nested_quadrature_check.csv")
print(t.abs_diff.max(), -fits[25].fun, -fits[35].fun)
