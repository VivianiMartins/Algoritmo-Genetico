import numpy as np

def _to_int_safe(x):
    try:
        if x is None:
            return 0
        if isinstance(x, (int, np.integer)):
            return int(x)
        if isinstance(x, float) and np.isnan(x):
            return 0
        return int(float(x))
    except Exception:
        return 0