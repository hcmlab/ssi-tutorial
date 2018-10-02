from scipy import signal
import numpy as np


def transform(info, sin, sout, sxtra, board, opts, vars): 

    x = np.asarray(sin)
    y = np.asarray(sout)

    np.copyto(y, signal.detrend(x, axis=0))

    