"""T19 GLMM, pooled RQ1 (PLANNER spec, COLLAB.md 2026-11-16). Numbers only.

correct ~ condition * content_type + condition * model + (1 | item_id), binomial logit.
Reference levels: A_text, math, Qwen2.5-VL-7B. Primary data: run 1, 5 primary models, 22,500 rows.

Software: the spec prefers R lme4 (bobyqa), then pymer4. Neither R nor pymer4 is installed on the server. The primary fit
is exact maximum likelihood with the item intercept integrated out by Gauss-Hermite quadrature (GHGLMM from glmm.py,
deviation #24; lme4's nAGQ > 1 does the same). The spec's last-resort fallback, statsmodels BinomialBayesMixedGLM
(variational Bayes, NOT maximum likelihood), is fit too and reported in its own file.

Contrasts follow emmeans: on the link scale, random effects at 0, other factors averaged with equal weights.
B-A and C-A per content type (averaged over the 5 models) and per model x content. Holm within each family
(one family = one comparison x one grouping).
Sensitivities: majority-vote outcome (runs 1-3, correct in >= 2 of 3); + (1 | item_id:model) (nested quadrature).
Extension (exploratory): the same model on the 4 extension models, run 1 (reference model Qwen3-VL-8B).
Run: .venv/bin/python -m vmod.glmm_t19
"""
from __future__ import annotations

import importlib.metadata as md
import platform
import time

import numpy as np
import pandas as pd
import patsy
from scipy import optimize, stats
from scipy.special import expit, log_expit, logsumexp

from .analyze import A, B, holm, load_scored, write_csv
from .analyze import C as COND_C
from .config import RESULTS
from .glmm import GHGLMM, prep
from .replication import EXT_RUNS, PRIMARY_RUNS, load_runs, majority_vote

PRIMARY = ["Qwen2.5-VL-3B", "Qwen2.5-VL-7B", "Qwen2.5-VL-32B", "InternVL3-8B", "gemma-3-12b"]
CONDS = [A, B, COND_C]
CT = ["math", "code", "table"]


def terms(ref_model):
    c = "C(condition, Treatment('A_text'))"
    t = "C(content_type, Treatment('math'))"
    m = f"C(model, Treatment('{ref_model}'))"
    return {"full": f"{c} * {t} + {c} * {m}",
            "no condition (and its interactions)": f"{t} + {m}",
            "no condition:content_type": f"{c} * {m} + {t}",
            "no condition:model": f"{c} * {t} + {m}"}


def clean(name, ref_model):
    return (name.replace("C(condition, Treatment('A_text'))", "condition").replace("C(content_type, Treatment('math'))", "content_type")
            .replace(f"C(model, Treatment('{ref_model}'))", "model"))


class NestedGHGLMM(GHGLMM):
    """(1 | item) + (1 | item:model): u_item and v_item:model both N(0, s^2), integrated by nested GH quadrature."""

    def __init__(self, X, y, item, group, k_outer=25, k_inner=25):
        self.X, self.y = np.asarray(X, float), np.asarray(y, float)
        _, self.gi = np.unique(item, return_inverse=True)                 # obs -> item
        gcodes, self.gg = np.unique(group, return_inverse=True)            # obs -> item:model
        self.n_groups, self.n_sub = self.gi.max() + 1, len(gcodes)
        self.sub_item = np.zeros(self.n_sub, int)
        self.sub_item[self.gg] = self.gi                                   # item:model -> item
        z1, w1 = np.polynomial.hermite_e.hermegauss(k_outer)
        z2, w2 = np.polynomial.hermite_e.hermegauss(k_inner)
        self.z1, self.lw1 = z1, np.log(w1 / np.sqrt(2 * np.pi))
        self.z2, self.lw2 = z2, np.log(w2 / np.sqrt(2 * np.pi))
        self.z = z1  # for fixed_table compatibility

    def _parts(self, theta):
        beta, s1, s2 = theta[:-2], np.exp(theta[-2]), np.exp(theta[-1])
        eta = (self.X @ beta)[:, None, None] + s1 * self.z1[None, :, None] + s2 * self.z2[None, None, :]
        ll = self.y[:, None, None] * log_expit(eta) + (1 - self.y[:, None, None]) * log_expit(-eta)
        lg = np.zeros((self.n_sub, len(self.z1), len(self.z2)))
        np.add.at(lg, self.gg, ll)
        b = lg + self.lw2[None, None, :]
        lgk = logsumexp(b, axis=2)                                         # sub x K1
        li_k = np.zeros((self.n_groups, len(self.z1)))
        np.add.at(li_k, self.sub_item, lgk)
        a = li_k + self.lw1[None, :]
        li = logsumexp(a, axis=1)
        return eta, a, li, b, lgk, s1, s2

    def nll(self, theta):
        return -self._parts(theta)[2].sum()

    def grad(self, theta):
        eta, a, li, b, lgk, s1, s2 = self._parts(theta)
        P = np.exp(a - li[:, None])                                        # item x K1
        Q = np.exp(b - lgk[:, :, None])                                    # sub x K1 x K2
        W = P[self.sub_item][:, :, None] * Q                               # sub x K1 x K2
        r = (self.y[:, None, None] - expit(eta)) * W[self.gg]              # n x K1 x K2
        gb = self.X.T @ r.sum(axis=(1, 2))
        g1 = (r * (s1 * self.z1[None, :, None])).sum()
        g2 = (r * (s2 * self.z2[None, None, :])).sum()
        return -np.append(gb, [g1, g2])

    def fit(self, start=None):
        k = self.X.shape[1]
        th0 = np.zeros(k + 2) if start is None else start
        res = optimize.minimize(self.nll, th0, jac=self.grad, method="L-BFGS-B",
                                options=dict(maxiter=10000, gtol=1e-6, ftol=1e-14))
        self.theta, self.res = res.x, res
        self.cov = hessian_cov(self.grad, res.x)
        return self


def hessian_cov(grad, x, eps=1e-5):
    k = len(x)
    H = np.zeros((k, k))
    for j in range(k):
        e = np.zeros(k); e[j] = eps
        H[:, j] = (grad(x + e) - grad(x - e)) / (2 * eps)
    H = (H + H.T) / 2
    return np.linalg.inv(H), np.linalg.eigvalsh(H)


def fit(d, formula, n_nodes=40, nested=False, start=None):
    X = patsy.dmatrix(formula, d, return_type="dataframe")
    t0 = time.time()
    if nested:
        m = NestedGHGLMM(X.values, d.y.values, d.item_id.values, (d.item_id + "|" + d.model).values)
        m.fit(start)
    else:
        m = GHGLMM(X.values, d.y.values, d.item_id.values, n_nodes)
        k = X.shape[1]
        res = optimize.minimize(m.nll, np.zeros(k + 1) if start is None else start, jac=m.grad, method="L-BFGS-B",
                                options=dict(maxiter=10000, gtol=1e-6, ftol=1e-14))
        m.theta, m.res = res.x, res
        m.cov = hessian_cov(m.grad, res.x)
    m.cov, m.hess_eig = m.cov
    m.X_info, m.cols, m.seconds = X.design_info, list(X.columns), time.time() - t0
    m.n_obs, m.n_re = len(d), (2 if nested else 1)
    m.n_par = X.shape[1] + m.n_re
    m.loglik = -m.res.fun
    m.aic = 2 * m.n_par - 2 * m.loglik
    m.bic = m.n_par * np.log(m.n_obs) - 2 * m.loglik
    g = m.grad(m.res.x)
    m.max_abs_grad = float(np.abs(g).max())
    m.max_rel_grad = float(np.abs(m.cov @ g).max())                       # lme4-style scaled gradient
    return m


def conv_row(m, label):
    warn = []
    if not m.res.success:
        warn.append(f"optimizer: {m.res.message}")
    if m.hess_eig.min() <= 0:
        warn.append("Hessian not positive definite")
    if m.max_rel_grad > 2e-3:
        warn.append(f"scaled gradient {m.max_rel_grad:.2g} > 0.002")
    sds = np.exp(m.theta[-m.n_re:])
    if (sds < 1e-3).any():
        warn.append("random-effect SD at boundary (~0)")
    return dict(fit=label, n_obs=m.n_obs, n_items=m.n_groups, n_fixed=len(m.cols), n_par=m.n_par, loglik=m.loglik,
                aic=m.aic, bic=m.bic, converged=bool(m.res.success) and not warn, optimizer="scipy L-BFGS-B (analytic gradient)",
                optimizer_message=str(m.res.message), n_iter=int(m.res.nit), max_abs_gradient=m.max_abs_grad,
                max_scaled_gradient=m.max_rel_grad, min_hessian_eigenvalue=float(m.hess_eig.min()),
                warnings="; ".join(warn) if warn else "none", seconds=round(m.seconds, 1))


def fixed_table(m, label, ref_model):
    se = np.sqrt(np.diag(m.cov))
    rows = []
    for j, c in enumerate(m.cols):
        b, s = m.theta[j], se[j]
        rows.append(dict(fit=label, term=clean(c, ref_model), estimate=b, se=s, z=b / s, p_value=2 * stats.norm.sf(abs(b / s)),
                         odds_ratio=np.exp(b), or_ci_lo=np.exp(b - 1.959964 * s), or_ci_hi=np.exp(b + 1.959964 * s)))
    return pd.DataFrame(rows)


def re_table(m, label):
    names = ["item_id"] if m.n_re == 1 else ["item_id", "item_id:model"]
    se = np.sqrt(np.diag(m.cov))
    rows = []
    for i, nm in enumerate(names):
        j = len(m.cols) + i
        ls, sl = m.theta[j], se[j]
        rows.append(dict(fit=label, group=nm, sd=np.exp(ls), variance=np.exp(2 * ls), sd_ci_lo=np.exp(ls - 1.959964 * sl),
                         sd_ci_hi=np.exp(ls + 1.959964 * sl), var_ci_lo=np.exp(2 * (ls - 1.959964 * sl)),
                         var_ci_hi=np.exp(2 * (ls + 1.959964 * sl)), ci_method="Wald on log(sd)"))
    tot = sum(r["variance"] for r in rows)
    for r in rows:
        r["icc_latent_total"] = tot / (tot + np.pi ** 2 / 3)
    return pd.DataFrame(rows)


def contrasts(m, d, label):
    """emmeans-style: link scale, random effects 0, models averaged with equal weights for the per-content family."""
    beta, cov = m.theta[:len(m.cols)], m.cov[:len(m.cols), :len(m.cols)]
    models = sorted(d.model.unique())

    def xrow(cond, ct, mod):
        nd = pd.DataFrame(dict(condition=[cond], content_type=[ct], model=[mod], y=[0.0], item_id=["x"]))
        return patsy.build_design_matrices([m.X_info], nd, return_type="dataframe")[0].values[0]

    X = {(c, ct, mo): xrow(c, ct, mo) for c in CONDS for ct in CT for mo in models}
    rows = []
    for c2 in (B, COND_C):
        cname = f"{c2} - {A}"
        for ct in CT:
            L = np.mean([X[(c2, ct, mo)] - X[(A, ct, mo)] for mo in models], axis=0)
            rows.append(dict(family=f"{cname} | content_type", model="(average of models)", content_type=ct, L=L))
        for mo in models:
            for ct in CT:
                rows.append(dict(family=f"{cname} | model x content_type", model=mo, content_type=ct,
                                 L=X[(c2, ct, mo)] - X[(A, ct, mo)]))
    out = []
    for r in rows:
        L = r.pop("L")
        est, se = float(L @ beta), float(np.sqrt(L @ cov @ L))
        out.append(dict(fit=label, **r, contrast=r["family"].split(" | ")[0], log_odds_ratio=est, se=se, z=est / se,
                        p_value=2 * stats.norm.sf(abs(est / se)), odds_ratio=np.exp(est),
                        or_ci_lo=np.exp(est - 1.959964 * se), or_ci_hi=np.exp(est + 1.959964 * se)))
    t = pd.DataFrame(out)
    t["p_holm"] = np.nan
    for f in t.family.unique():
        k = t.family == f
        t.loc[k, "p_holm"] = holm(t.loc[k, "p_value"])
    t["holm_family_size"] = t.groupby("family").family.transform("size")
    return t


def lrts(d, label, ref_model, full):
    rows = []
    for name, f in terms(ref_model).items():
        if name == "full":
            continue
        red = fit(d, f, start=None)
        lr = 2 * (full.loglik - red.loglik)
        df_ = len(full.cols) - len(red.cols)
        rows.append(dict(fit=label, test=f"full vs {name}", loglik_full=full.loglik, loglik_reduced=red.loglik,
                         aic_full=full.aic, aic_reduced=red.aic, bic_full=full.bic, bic_reduced=red.bic,
                         chisq=lr, df=df_, p_value=stats.chi2.sf(lr, df_), reduced_converged=bool(red.res.success)))
    return rows


def vb_fallback(d, ref_model):
    from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM

    t0 = time.time()
    m = BinomialBayesMixedGLM.from_formula("y ~ " + terms(ref_model)["full"], {"item_id": "0 + C(item_id)"}, d).fit_vb()
    fe = pd.DataFrame(dict(term=[clean(n, ref_model) for n in m.model.exog_names], posterior_mean=m.fe_mean, posterior_sd=m.fe_sd))
    fe["z"] = fe.posterior_mean / fe.posterior_sd
    fe["p_value_approx"] = 2 * stats.norm.sf(fe.z.abs())
    fe["odds_ratio"] = np.exp(fe.posterior_mean)
    fe["or_ci_lo"] = np.exp(fe.posterior_mean - 1.959964 * fe.posterior_sd)
    fe["or_ci_hi"] = np.exp(fe.posterior_mean + 1.959964 * fe.posterior_sd)
    fe["sd_item_intercept"] = float(np.exp(m.vcp_mean[0]))
    fe["method"] = f"statsmodels {md.version('statsmodels')} BinomialBayesMixedGLM.fit_vb (variational Bayes, not ML)"
    fe["seconds"] = round(time.time() - t0, 1)
    return fe


def summary_text(m, label, ref_model, fe, re, conv):
    lines = [f"=== {label} ===",
             "Generalized linear mixed model fit by maximum likelihood (Gauss-Hermite quadrature)",
             f"  Family: binomial ( logit )",
             f"  Formula: correct ~ condition * content_type + condition * model + "
             + ("(1 | item_id)" if m.n_re == 1 else "(1 | item_id) + (1 | item_id:model)"),
             f"  Reference levels: condition=A_text, content_type=math, model={ref_model}",
             f"  Quadrature: " + ("40 nodes" if m.n_re == 1 else "nested 25 x 25 nodes"),
             f"  Observations: {m.n_obs}; items: {m.n_groups}",
             f"       AIC        BIC     logLik   deviance",
             f"  {m.aic:9.2f}  {m.bic:9.2f}  {m.loglik:9.2f}  {-2 * m.loglik:9.2f}",
             "Random effects:"]
    for _, r in re.iterrows():
        lines.append(f"  {r.group:<16} (Intercept)  Variance {r.variance:.4f}  Std.Dev. {r.sd:.4f}")
    lines.append("Fixed effects:")
    lines.append(f"  {'term':<58}{'Estimate':>10}{'Std.Err':>10}{'z':>9}{'Pr(>|z|)':>11}")
    for _, r in fe.iterrows():
        lines.append(f"  {r.term:<58}{r.estimate:>10.4f}{r.se:>10.4f}{r.z:>9.3f}{r.p_value:>11.3g}")
    lines.append(f"Convergence: {conv['optimizer_message']}; iterations {conv['n_iter']}; max |gradient| {conv['max_abs_gradient']:.2g}; "
                 f"max scaled gradient {conv['max_scaled_gradient']:.2g}; min Hessian eigenvalue {conv['min_hessian_eigenvalue']:.3g}")
    lines.append(f"Convergence warnings: {conv['warnings']}")
    return "\n".join(lines) + "\n\n"


def run_fit(d, label, ref_model, nested=False, do_lrt=True):
    full = fit(d, terms(ref_model)["full"], nested=nested)
    conv = conv_row(full, label)
    fe, re = fixed_table(full, label, ref_model), re_table(full, label)
    ct = contrasts(full, d, label)
    lr = lrts(d, label, ref_model, full) if do_lrt else []
    txt = summary_text(full, label, ref_model, fe, re, conv)
    print(f"{label}: loglik {full.loglik:.2f}, sd {np.exp(full.theta[-full.n_re:]).round(3)}, warnings: {conv['warnings']}, "
          f"{full.seconds:.0f}s", flush=True)
    return full, conv, fe, re, ct, lr, txt


def main():
    d1 = prep(load_scored(PRIMARY_RUNS[1]))
    d1 = d1[d1.model.isin(PRIMARY)].reset_index(drop=True)
    assert len(d1) == 22500 and d1.item_id.nunique() == 1500, (len(d1), d1.item_id.nunique())

    runs = load_runs(PRIMARY_RUNS)
    mv = majority_vote(runs[runs.model_id.map(lambda s: s.split("/")[-1].replace("-Instruct", "").replace("-it", "")).isin(PRIMARY)])
    dmv = prep(mv)

    de = prep(load_scored(EXT_RUNS[1]))
    ext_ref = "Qwen3-VL-8B"
    assert ext_ref in set(de.model), sorted(de.model.unique())

    fits = [("primary run 1", d1, "Qwen2.5-VL-7B", False, True),
            ("sensitivity: majority vote (runs 1-3)", dmv, "Qwen2.5-VL-7B", False, True),
            ("sensitivity: + (1 | item_id:model), run 1", d1, "Qwen2.5-VL-7B", True, False),
            ("extension (exploratory) run 1", de, ext_ref, False, True)]
    conv, fe, re, ct, lr, txt = [], [], [], [], [], []
    for label, d, ref, nested, do_lrt in fits:
        _, c, f, r, k, l, t = run_fit(d, label, ref, nested, do_lrt)
        conv.append(c); fe.append(f); re.append(r); ct.append(k); lr += l; txt.append(t)

    vb = vb_fallback(d1, "Qwen2.5-VL-7B")
    print(f"VB fallback done, {vb.seconds.iloc[0]}s", flush=True)

    sw = (f"Software: Python {platform.python_version()}, numpy {md.version('numpy')}, scipy {md.version('scipy')}, "
          f"patsy {md.version('patsy')}, statsmodels {md.version('statsmodels')}. In-house exact-ML GLMM "
          f"(src/vmod/glmm.py GHGLMM, src/vmod/glmm_t19.py NestedGHGLMM). R/lme4 and pymer4 not installed on the server.\n"
          f"Contrasts: emmeans-style, link scale, random effects at 0; per-content-type contrasts average the models with "
          f"equal weights; odds ratio = odds(B or C) / odds(A). Holm within each family (contrast x grouping).\n"
          f"AIC/BIC: k = fixed effects + random-effect SDs; BIC uses n = number of observations (as lme4).\n\n")
    (RESULTS / "analysis" / "glmm_model_summary.txt").write_text(sw + "".join(txt), encoding="utf-8")
    write_csv(pd.DataFrame(conv), "glmm_t19_fit_info.csv")
    write_csv(pd.concat(fe, ignore_index=True), "glmm_t19_fixed_effects.csv")
    write_csv(pd.concat(re, ignore_index=True), "glmm_t19_random_effects.csv")
    write_csv(pd.concat(ct, ignore_index=True), "glmm_t19_emm_contrasts.csv")
    write_csv(pd.DataFrame(lr), "glmm_t19_lrt.csv")
    write_csv(vb, "glmm_t19_vb_fallback_fixed_effects.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
