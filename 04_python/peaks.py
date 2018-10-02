from scipy.signal import find_peaks
import numpy as np


def getOptions(opts, vars):

    opts['prominence'] = 0.7
    opts['min_rate'] = 50
    opts['max_rate'] = 200    


def getEventAddress(opts, vars):
    return 'peak,rate@ecg'


def consume_enter(sins, board, opts, vars):

    vars['last_pos'] = None
    vars['counter'] = 0    


def send_rate(pos, last_pos, sr, board, opts, vars):
    
    dist = pos - last_pos           
    rate = 60.0 / (dist / sr)

    if rate >= opts['min_rate'] and rate <= opts['max_rate']:
        time = int(1000 * last_pos/sr)
        dur = int(1000 * dist/sr)
        board.update(time, dur, 'rate@ecg', float(rate))
        board.update(time+dur, 0, 'peak@ecg', float(pos))


def consume(info, sins, board, opts, vars): 

    x = np.asarray(sins[0]).squeeze()
    sr = sins[0].sr
    last_pos = vars['last_pos']
    counter = vars['counter']

    peaks, _ = find_peaks(x, prominence=opts['prominence'])

    for peak in peaks:
        pos = peak + counter
        if last_pos is not None:            
            send_rate(pos, last_pos, sr, board, opts, vars)
        last_pos = pos
    
    vars['last_pos'] = last_pos
    vars['counter'] += len(x)