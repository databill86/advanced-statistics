import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc3 as pm
from scipy.stats import norm, uniform
import seaborn as sns

# Config
os.chdir("/home/jovyan/work")
%config InlineBackend.figure_format = 'retina'
%matplotlib inline
plt.rcParams["figure.figsize"] = (10, 5)
np.random.seed(42)

# Prepare the data
x = uniform(0, 20).rvs(30)
eps = norm(0, 4).rvs(30)
y = 11 + 3*x + eps

# Sampling
with pm.Model() as model:
    b_0 = pm.Normal("b_0", mu=0, sd=10)
    b_1 = pm.Normal("b_1", mu=0, sd=2)
    e = pm.HalfCauchy("e", 2)
    mu = pm.Deterministic("mu", b_0 + b_1*x)
    Y = pm.Normal("Y", mu=mu, sd=e, observed=y)
    trace = pm.sample(10000)

# Plotting
plt.scatter(x, y)
pm.plot_posterior_predictive_glm(
    trace=trace,
    samples=200,
    eval=np.linspace(0, 20, 100),
    lm=lambda x, sample: sample["b_0"] + sample["b_1"]*x,
    alpha=.1,
    color="red"
)
plt.savefig("./results/4-14-posterior-hpd.png")