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
        f'CurrentFreq {current_freq}, Autoreload {autoreload}, SetFreq {freq}, CalcFreq: {conversionFreq}, Compare: {compare}, Prescaler: {current_prescaler}')
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
    frequency = int(input('Enter freq:\n'))
    scale = prescaler_rough_seacrh(frequency)
    result_freq = conversion(frequency, scale, 50,True)
    accuracy = abs(result_freq - frequency)
    if accuracy < 0.1:
        print(f'Accurate enough, accuracy is {accuracy}')
        sys.exit()
    else:
        print(f'Not accurate enough, accuracy is {accuracy}')
        max_accuracy = 1000
        max_accuracy_scale = scale
        for i in range(1, 65535):
            accuracy = abs(frequency - conversion(frequency, i, 50, False))
            if accuracy < max_accuracy:
                max_accuracy = accuracy
                max_accuracy_scale = i
            if max_accuracy < 0.1:
                break
        conversion(frequency, max_accuracy_scale, 50, True)
