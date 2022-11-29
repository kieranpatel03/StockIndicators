import numpy as np

def TR(closes, highs, lows):
    TR = [max([abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]), highs[i]-lows[i]]) for i in range(1, len(closes))]
    return TR


def SMA(closes, period):
    if period > len(closes):
        raise Exception('Period is higher than number of items in list')
    if not isinstance(closes, list):
        raise Exception('Closes needs to be a 1 dimensional list of integers')
    try:
        map(float, closes)
    except:
        raise Exception('Closes needs to be a 1 dimensional list of integers')
    SMA = [(sum(closes[max(i-period, 0):i])/(len(closes[max(i-period, 0):i]))) for i in range(1, len(closes) + 1)]
    return SMA

def EMA(closes, period):
    if period > len(closes):
        raise Exception('Period is higher than number of items in list')
    EMAs = [closes[0]]
    for i in range(1, len(closes)):
        EMAs.append((closes[i] * (2/(period + 1)) + (EMAs[-1] * (1-(2/(period + 1))))))
    return EMAs

def MACD(closes):
    MA_12 = EMA(closes, 12)
    MA_26 = EMA(closes, 26)
    fast_MACD = [MA_12[i] - MA_26[i] for i in range(len(MA_12))]
    signal_line = EMA(fast_MACD, 9)
    return fast_MACD, signal_line

def ADX(closes, highs, lows, period):
    if period > len(closes):
        raise Exception('Period is higher than number of items in list')
    TR = EMA(TR(closes, highs, lows), period)
    def DM(high, low, yday_high, yday_low, type):
        h = high - yday_high
        l = low - yday_low
        if (h + l) < 0:
            if type == '-':
                return abs(l)
            else:
                return 0
        elif (h + l) > 0:
            if type == '+':
                return h
            else:
                return 0
        else:
            return 0
    DM_plus = EMA([DM(highs[i], lows[i], highs[i-1], lows[i-1], '+') for i in range(1, len(closes))], period)
    DM_minus = EMA([DM(highs[i], lows[i], highs[i-1], lows[i-1], '-') for i in range(1, len(closes))], period)
    DI_plus_period =  [DM_plus[i]*100/TR[i] for i in range(len(DM_plus))][period:]
    DI_minus_period = [DM_minus[i]*100/TR[i] for i in range(len(DM_minus))][period:]
    DX = [(100 * abs(DI_plus_period[i] - DI_minus_period[i])/(DI_plus_period[i] + DI_minus_period[i])) for i in range(len(DI_plus_period))]
    ADX = [None for i in range(period)] + EMA(DX, period)
    return ADX, [None for i in range(period)] + DI_plus_period, [None for i in range(period)] + DI_minus_period


def Stochastic(closes, highs, lows, period):
    if period > len(closes):
        raise Exception('Period is higher than number of items in list')
    if len(closes) != len(highs) or len(highs) != len(lows):
        raise Exception('Length of closes, highs, and lows are not the same.')
    def K(close, highs, lows):
        low = min(lows)
        high = max(highs)
        return (100 * (close - low)/(high - low))
    fast_line = [K(closes[i - 1], highs[max(i-period, 0):i], lows[max(i-period, 0):i]) for i in range(1, len(closes) + 1)]
    slow_line = SMA(fast_line, 3)
    return fast_line, slow_line

def RSI(closes, period):
    if period > len(closes):
        raise Exception('Period is higher than number of items in list')
    changes = [(100*(closes[i + 1] - closes[i])/closes[i]) for i in range(len(closes) - 1)]
    RS = [[(max(changes[0], 0)), abs(min(changes[0], 0))]]
    for i in range(1, len(changes)):
        if i < 15:
            RS.append([sum([i for i in changes[max(i-period, 0): i] if i > 0])/min(i, period), sum([abs(i) for i in changes[max(i-period, 0): i] if i < 0])/min(i, period)])
        else:
            RS.append([(((RS[-1][0]) * (period-1)) + max(changes[i], 0))/period, (((RS[-1][1]) * (period-1)) + abs(min(changes[i], 0)))/period])
    relative_strength_index = [(100 - (100/(1 + i[0]/i[1]))) if i[1] > 0 else None for i in RS]
    return [None] + relative_strength_index

def OBV(closes, volume):
    if len(closes) != len(volume):
        raise Exception('Closes and volume have different lengths.')
    on_bal_vol = [0]
    for i in range(1, len(closes)):
        if (closes[i] - closes[i-1]) > 0:
            on_bal_vol.append(on_bal_vol[-1] + volume[i])
        elif (closes[i] - closes[i-1]) < 0:
            on_bal_vol.append(on_bal_vol[-1] - volume[i])
        else:
            on_bal_vol.append(on_bal_vol[-1])
    return on_bal_vol

def AD(closes, opens, highs, lows, volume):
    if not all(i == len(closes) for i in [len(closes), len(opens), len(highs), len(lows), len(volume)]):
        raise Exception('Closes, opens, highs, lows, and volume have different lengths.')
    return np.cumsum([volume[i] * ((closes[i]) - opens[i])/(highs[i] - lows[i]) for i in range(len(closes))]).tolist()

def force_index(closes, volume):
    FI =  [(volume[i] * (closes[i] - closes[i-1])) for i in range(1, len(closes))]
    return [None] + EMA(FI, 13)

relative_strength_index = RSI
on_balance_volume = OBV
exponential_moving_average = EMA
simple_moving_average = SMA
true_range = TR
on_balance_volume = OBV
accumulation_distribution = AD
