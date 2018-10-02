from scipy.misc import electrocardiogram

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.misc.electrocardiogram.html

def getOptions(opts, vars):
    
    pass

def getChannelNames(opts, vars):
    
    return { 'ecg' : 'An electrocardiogram signal' }


def initChannel(name, channel, types, opts, vars):

    if name == 'ecg':
        channel.dim =  1
        channel.type = types.FLOAT
        channel.sr = 360
    else:
        print('unkown channel name')


def connect(opts, vars):
    
    vars['ecg'] = electrocardiogram()    
    vars['pos'] = 0

        
def read(name, sout, reset, board, opts, vars):    

    pos = vars['pos']
    ecg = vars['ecg']

    if name == 'ecg':
        for n in range(sout.num):
            sout[n] = ecg[pos%len(ecg)]
            pos += 1

    else:
        print('unkown channel name')

    vars['pos'] = pos


def disconnect(opts, vars):
    pass
