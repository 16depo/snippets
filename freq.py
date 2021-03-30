import sys

MAIN_FREQ = 84000000


def conversion(freq, current_prescaler, fill_percent, print_result):
    current_freq = MAIN_FREQ / current_prescaler
    autoreload = current_freq // freq
    compare = (autoreload * fill_percent) // 100
    if compare == 0:
        return 0
    try:
        conversionFreq = current_freq / autoreload
    except ZeroDivisionError:
        return 0
    if print_result == True:
        print(
        f'SetFreq {freq}, CalcFreq: {conversionFreq:10f}, CurrentFreq {int(current_freq):11}, Autoreload {int(autoreload):6}, Compare: {compare:7}, Prescaler: {current_prescaler:6}')
    return conversionFreq


def prescaler_rough_seacrh(freq):
    prescaler = 1
    if 10 > freq >= 1:
        prescaler = 7000
    elif 100 > freq > 10:
        prescaler = 700
    elif 1000 > freq > 100:
        prescaler = 70
    elif 10000 > freq > 100:
        prescaler = 7
    else:
        prescaler = 1
    return prescaler


if __name__ == '__main__':
    for i in range(1,10001):
        frequency = i
        target_accuracy = i/10000
        scale = prescaler_rough_seacrh(frequency)
        result_freq = conversion(frequency, scale, 50,False)
        accuracy = abs(result_freq - frequency)
        if accuracy < target_accuracy:
            conversion(frequency, scale, 50, True)
            continue
        else:
            #print(f'Not accurate enough, accuracy is {accuracy}')
            max_accuracy = 1000
            max_accuracy_scale = scale
            for i in range(1, 65535):
                accuracy = abs(frequency - conversion(frequency, i, 50, False))
                if accuracy < max_accuracy:
                    max_accuracy = accuracy
                    max_accuracy_scale = i
                if max_accuracy < target_accuracy:
                    break
            conversion(frequency, max_accuracy_scale, 50, True)
