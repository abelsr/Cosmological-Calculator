import numpy as np
from math import sqrt

def get_luminosity_distance(redshift, h0: float = 69.6, omega_lambda: float = 0.714, omega_matter: float = 0.286):
    from math import asin
    h = h0 / 100
    dh = 3000 / h
    cte = ( 2 * asin(1) ) / (18 * 36)
    dc = gauss(lambda x: f_dist(x, omega_lambda, omega_matter, 0.0), 0, redshift, 50)
    dm = dc * dh
    dl = (1 + redshift) * dm
    dd = dl / ((1 + redshift) ** 2 )
    dc = dc * dh
    esc = cte * dd
    res = {'Dist Hubble': float(dh),
           'Dist lum': float(dl), 
           'Dist ang': float(dd), 
           'Diam': float(dm), 
           'kpc/arcseg': float(esc)}
    return res

def gauss(f, a: float, b: float, n: int = 10) -> float:
    mitad = float(b-a)/2.
    mid = (a+b)/2.
    [x,w] = np.polynomial.legendre.leggauss(n)
    result =  0.
    for i in range(n):
        result += w[i] * f(mitad*x[i] + mid)
    result *= mitad
    return result

def f_dist(z, omega_lambda, omega_matter, omega_k):
    return 1./sqrt(omega_matter*(1 + z)**3 + omega_lambda + omega_k*(1 + z)**2)