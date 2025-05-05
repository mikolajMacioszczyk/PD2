import math

def round_to_significant_figures(num, sig_figs):
    if num == 0:
        return 0
    else:
        return round(num, -int(math.floor(math.log10(abs(num)))) + (sig_figs - 1))