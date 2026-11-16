"""T12 GLMM (OWNER posted `GLMM OK`, 2026-11-16): correct ~ condition * content + condition * model + (1 | item),
binomial logit, primary models, run 1 (primary analysis). Numbers only.

No R on the server and statsmodels has only an approximate (variational Bayes) binomial mixed GLM, so the model is fit
by exact maximum likelihood: the item random intercept is integrated out with Gauss-Hermite quadrature (as lme4 with
nAGQ > 1). Each item's 15 responses (5 models x 3 conditions) share one intercept. SEs from the observed information
(numerical Hessian of the analytic gradient). Checks: quadrature 40 vs 80 nodes, and statsmodels BinomialBayesMixedGLM.
Likelihood-ratio tests for condition:content, condition:model and all condition terms. Runs 2 and 3 repeat the LRTs.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import patsy
from scipy import optimize, stats
from scipy.special import expit, log_expit, logsumexp

from .analyze import A, B, load_scored, write_csv
from .analyze import C as COND_C
from .config import RESULTS

SC = RESULTS / "scored"
RUNS = {1: SC / "main_all.csv.gz", 2: SC / "main_run2_all.csv.gz", 3: SC / "main_run3_all.csv.gz"}
FULL = "C(condition, Treatment('A_text')) * C(content_type, Treatment('code')) + C(condition, Treatment('A_text')) * C(model, Treatment('Qwen2.5-VL-7B'))"
REDUCED = {
    "no condition:model": "C(condition, Treatment('A_text')) * C(content_type, Treatment('code')) + C(model, Treatment('Qwen2.5-VL-7B'))",
    "no condition:content": "C(condition, Treatment('A_text')) * C(model, Treatment('Qwen2.5-VL-7B')) + C(content_type, Treatment('code'))",
    "no condition terms": "C(content_type, Treatment('code')) + C(model, Treatment('Qwen2.5-VL-7B'))",
}


def prep(df):
    d = df[["model_id", "content_type", "item_id", "condition", "correct"]].copy()
    d["model"] = d.model_id.str.split("/").str[-1].str.replace("-Instruct", "").str.replace("-it", "")
    d["y"] = d.correct.astype(str).str.lower().eq("true").astype(float)
    return d.sort_values(["item_id", "model", "condition"]).reset_index(drop=True)


class GHGLMM:
    def __init__(self, X, y, groups, n_nodes=40):
        self.X, self.y = np.asarray(X, float), np.asarray(y, float)
        codes, self.g = np.unique(groups, return_inverse=True)
        self.n_groups = len(codes)
        z, w = np.polynomial.hermite_e.hermegauss(n_nodes)
        self.z, self.logw = z, np.log(w / np.sqrt(2 * np.pi))

    def _parts(self, theta):
        beta, logs = theta[:-1], theta[-1]
        s = np.exp(logs)
        eta = (self.X @ beta)[:, None] + s * self.z[None, :]           # n x K
        ll = self.y[:, None] * log_expit(eta) + (1 - self.y[:, None]) * log_expit(-eta)
        lik = np.zeros((self.n_groups, len(self.z)))
        np.add.at(lik, self.g, ll)                                        # per-item log L_ik
        a = lik + self.logw[None, :]
        li = logsumexp(a, axis=1)
        return eta, a, li, s

    def nll(self, theta):
        return -self._parts(theta)[2].sum()

    def grad(self, theta):
        eta, a, li, s = self._parts(theta)
        post = np.exp(a - li[:, None])                                    # posterior node weights per item
        r = (self.y[:, None] - expit(eta)) * post[self.g]                 # n x K
        gb = self.X.T @ r.sum(axis=1)
        gs = (r * (s * self.z[None, :])).sum()
        return -np.append(gb, gs)

    def fit(self, start=None):
        k = self.X.shape[1]
        th0 = np.zeros(k + 1) if start is None else start
        res = optimize.minimize(self.nll, th0, jac=self.grad, method="L-BFGS-B", options=dict(maxiter=10000, gtol=1e-6, ftol=1e-14))
        self.theta, self.res = res.x, res
        eps = 1e-5
        H = np.zeros((k + 1, k + 1))
        for j in range(k + 1):
            e = np.zeros(k + 1); e[j] = eps
            H[:, j] = (self.grad(res.x + e) - self.grad(res.x - e)) / (2 * eps)
        self.cov = np.linalg.inv((H + H.T) / 2)
        return self


def fit_formula(d, formula, n_nodes=40, start=None):
    X = patsy.dmatrix(formula, d, return_type="dataframe")
    m = GHGLMM(X.values, d.y.values, d.item_id.values, n_nodes).fit(start)
    return m, X.columns


def clean(name):
    return (name.replace("C(condition, Treatment('A_text'))", "condition").replace("C(content_type, Treatment('code'))", "content")
            .replace("C(model, Treatment('Qwen2.5-VL-7B'))", "model"))


def fixed_table(m, cols, run, n_nodes):
    se = np.sqrt(np.diag(m.cov))
    rows = []
    for j, c in enumerate(cols):
        b, s = m.theta[j], se[j]
        rows.append(dict(run=run, term=clean(c), coef=b, se=s, z=b / s, p_value=2 * stats.norm.sf(abs(b / s)),
                         odds_ratio=np.exp(b), or_ci_lo=np.exp(b - 1.96 * s), or_ci_hi=np.exp(b + 1.96 * s)))
    sig = np.exp(m.theta[-1])
    se_logs = se[-1]
    rows.append(dict(run=run, term="sd(item intercept)", coef=sig, se=sig * se_logs, z=np.nan, p_value=np.nan,
                     odds_ratio=np.nan, or_ci_lo=np.exp(m.theta[-1] - 1.96 * se_logs), or_ci_hi=np.exp(m.theta[-1] + 1.96 * se_logs)))
    t = pd.DataFrame(rows)
    t["n_obs"], t["n_items"], t["gh_nodes"] = len(m.y), m.n_groups, n_nodes
    t["loglik"], t["converged"] = -m.res.fun, bool(m.res.success)
    t["icc_latent"] = sig ** 2 / (sig ** 2 + np.pi ** 2 / 3)
    return t


def cell_contrasts(m, X, d, run):
    """A vs B and A vs C log-odds contrast per model x content from the fitted fixed effects (conditional on item = 0)."""
    beta, cov = m.theta[:-1], m.cov[:-1, :-1]
    cells = d[["model", "content_type"]].drop_duplicates()
    rows = []
    for _, r in cells.iterrows():
        xs = {}
        for cond in (A, B, COND_C):
            nd = pd.DataFrame(dict(condition=[cond], content_type=[r.content_type], model=[r.model], y=[0.0]))
            xs[cond] = patsy.build_design_matrices([X.design_info], nd, return_type="dataframe")[0].values[0]
        for c2 in (B, COND_C):
            L = xs[A] - xs[c2]
            est, se = L @ beta, np.sqrt(L @ cov @ L)
            rows.append(dict(run=run, model=r.model, content_type=r.content_type, comparison=f"{A} vs {c2}",
                             log_odds_diff=est, se=se, z=est / se, p_value=2 * stats.norm.sf(abs(est / se)),
                             odds_ratio=np.exp(est), or_ci_lo=np.exp(est - 1.96 * se), or_ci_hi=np.exp(est + 1.96 * se)))
    t = pd.DataFrame(rows)
    from .analyze import holm

    t["p_holm_within_comparison"] = np.nan
    for comp in t.comparison.unique():
        k = t.comparison == comp
        t.loc[k, "p_holm_within_comparison"] = holm(t.loc[k, "p_value"])
    return t


def vb_check(d):
    from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM

    m = BinomialBayesMixedGLM.from_formula("y ~ " + FULL, {"item": "0 + C(item_id)"}, d).fit_vb()
    fe = pd.DataFrame(dict(term=[clean(n) for n in m.model.exog_names], coef_vb=m.fe_mean, sd_vb=m.fe_sd))
    return fe, float(np.exp(m.vcp_mean[0]))


def main():
    fixed, lrts, contr, checks = [], [], [], []
    for run, p in RUNS.items():
        d = prep(load_scored(p))
        d = d[d.model.isin(["Qwen2.5-VL-3B", "Qwen2.5-VL-7B", "Qwen2.5-VL-32B", "InternVL3-8B", "gemma-3-12b"])]
        full, cols = fit_formula(d, FULL, 40)
        X = patsy.dmatrix(FULL, d, return_type="dataframe")
        fixed.append(fixed_table(full, cols, run, 40))
        contr.append(cell_contrasts(full, X, d, run))
        for name, f in REDUCED.items():
            red, rc = fit_formula(d, f, 40)
            lr = 2 * (-full.res.fun - (-red.res.fun))
            df_ = len(cols) - len(rc)
            lrts.append(dict(run=run, test=name, loglik_full=-full.res.fun, loglik_reduced=-red.res.fun, lr_stat=lr, df=df_,
                             p_value=stats.chi2.sf(lr, df_)))
        print(f"run {run}: loglik {-full.res.fun:.2f}, converged {full.res.success}, sd(item) {np.exp(full.theta[-1]):.3f}", flush=True)
        if run == 1:
            f80, _ = fit_formula(d, FULL, 80, start=full.theta)
            ck = pd.DataFrame(dict(term=[clean(c) for c in cols], coef_gh40=full.theta[:-1], coef_gh80=f80.theta[:-1],
                                   se_gh40=np.sqrt(np.diag(full.cov))[:-1], se_gh80=np.sqrt(np.diag(f80.cov))[:-1]))
            try:
                fe, sd_vb = vb_check(d)
                ck = ck.merge(fe, on="term", how="left")
            except Exception as e:  # check only
                sd_vb = np.nan
                print("VB check failed:", repr(e)[:200])
            ck.loc[len(ck)] = dict(term="sd(item intercept)", coef_gh40=np.exp(full.theta[-1]), coef_gh80=np.exp(f80.theta[-1]),
                                   coef_vb=sd_vb)
            ck["loglik_gh40"], ck["loglik_gh80"] = -full.res.fun, -f80.res.fun
            checks.append(ck)
    write_csv(pd.concat(fixed, ignore_index=True), "glmm_fixed_effects.csv")
    write_csv(pd.DataFrame(lrts), "glmm_lrt.csv")
    write_csv(pd.concat(contr, ignore_index=True), "glmm_cell_contrasts.csv")
    write_csv(pd.concat(checks, ignore_index=True), "glmm_checks.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
