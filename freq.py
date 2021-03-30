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
    input_accuracy = float(input('Введите желаемую точность(например 0.0001, по умолчанию динамическая)\n') or '-1')
    target_compare = int(input('Введите процент заполнения (compare, от 1% до 99%, по умолчанию 50%)\n') or '50')
    for i in range(1, 10001):
        frequency = i
        if input_accuracy == -1:
            target_accuracy = frequency / 10000
        else:
            target_accuracy = input_accuracy
        scale = prescaler_rough_seacrh(frequency)
        result_freq = conversion(frequency, scale, target_compare, False)
        accuracy = abs(result_freq - frequency)
        if accuracy < target_accuracy:
            conversion(frequency, scale, target_compare, True)
            continue
        else:
            # print(f'Not accurate enough, accuracy is {accuracy}')
            max_accuracy = 1000
            max_accuracy_scale = scale
            for i in range(1, 65535):
                accuracy = abs(frequency - conversion(frequency, i, target_compare, False))
                if accuracy < max_accuracy:
                    max_accuracy = accuracy
                    max_accuracy_scale = i
                if max_accuracy < target_accuracy:
                    break
            conversion(frequency, max_accuracy_scale, target_compare, True)
