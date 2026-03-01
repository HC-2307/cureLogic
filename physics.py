import math

T_DATUM = -10
HOURS = list(range(73))

def temp_profile(ambient, steam_temp, steam_dur, total=72):
    out = []
    for h in range(total + 1):
        if h < 2:
            T = ambient + (steam_temp - ambient) * (h / 2)
        elif h < steam_dur:
            exo = 10 * math.sin(math.pi * (h - 2) / max(steam_dur - 2, 1))
            T = steam_temp + exo
        else:
            T = ambient + (steam_temp - ambient) * math.exp(-(h - steam_dur) / 10)
        out.append(T)
    return out

def maturity(temps):
    M, arr = 0, []
    for T in temps:
        M += max(T - T_DATUM, 0)
        arr.append(M)
    return arr

def physics_strength(M, fc28, k=0.0048):
    return min(fc28 * (1 - math.exp(-k * M)), fc28 * 1.01)

def physics_curve(temps_list, mats, fc28):
    return [round(physics_strength(mats[h], fc28), 2) for h in HOURS]

def estimate_fc28(wc, scm, admix):
    return float(__import__("numpy").clip(55 - 60 * (wc - 0.30) + 0.3 * scm + admix * 1.1, 20, 70))