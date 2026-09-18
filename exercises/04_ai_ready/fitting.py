import numpy as np
import os
from math import *


def weighted_linear_fit(x, y, sigma=None, result={}):
    x = np.asarray(x)
    y = np.asarray(y)
    if sigma is None:
        w = np.ones_like(x)
    else:
        w = 1 / np.asarray(sigma)**2
    S = np.sum(w)
    Sx = np.sum(w * x)
    Sy = np.sum(w * y)
    Sxx = np.sum(w * x * x)
    Sxy = np.sum(w * x * y)
    D = S * Sxx - Sx**2
    slope = (S * Sxy - Sx * Sy) / D
    intercept = (Sxx * Sy - Sx * Sxy) / D
    slope_err = sqrt(S / D)
    intercept_err = sqrt(Sxx / D)
    result["slope"] = slope
    result["intercept"] = intercept
    return slope, intercept, slope_err, intercept_err


def chi_squared(x, y, sigma, slope, intercept):
    try:
        return np.sum(((y - (slope * x + intercept)) / sigma)**2)
    except:
        return None


def pendulum_g(lengths, periods, period_errors):
    periods = np.asarray(periods)
    t2 = periods**2
    t2_err = 2 * periods * np.asarray(period_errors)
    slope, intercept, slope_err, intercept_err = weighted_linear_fit(lengths, t2, t2_err)
    g = 4 * pi**2 / slope
    g_err = 4 * pi**2 * slope_err / slope**2
    return g, g_err
