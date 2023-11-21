import numpy as np
import matplotlib.pyplot as plt
import scipy.fft
import scipy.fftpack

points = 800

def amplitude_modulation_simple(signal, fc, points):
    x = np.linspace(0, 1, points)
    return signal * np.sin(fc * x * 2.0 * np.pi)

#демодуляция (амплитудная)
def demodulate(received_array, fc, t):
    c = np.sin(2 * np.pi * fc * t)

    demod = c * received_array
    return demod


def amplitude_modulation(amp, km, fc, f, points):
    # amp - амплитуда сигнала
    # km - коэффициент модуляции
    # fc - частота несущего сигнала
    # f - частота сигнала
    # points - число точек для отрисовки
    x = np.linspace(0, 1, points)
    return amp * (km * (np.sign(np.sin(f * x * 2.0 * np.pi)) + amp)) * np.sin(fc * x * 2.0 * np.pi)

am_sig = amplitude_modulation(1.0, 0.45, 70, 10, points)  # несущая частота - 70 Гц
spectr_sig_am = np.abs(scipy.fft.fft(am_sig)) / (points * 0.5)


#синтезированный сигнал
plt.title('Синтезированный сигнал (из 4-го номера)')
freq = np.fft.fftfreq(len(am_sig), 1.0 / points)
cutted_spec_signal = spectr_sig_am.copy()
cutted_spec_signal[(freq < 60)] = 0 #обрезание низких частот
cutted_spec_signal[(freq > 80)] = 0 #обрезание высоких частот
cutted_signal = scipy.fftpack.irfft(cutted_spec_signal)
print("cutted_signal: ", len(cutted_signal))


plt.plot(cutted_signal)
plt.xlim([0, points])
plt.tight_layout()
plt.show()


t = np.linspace(0, 1, points)

#частоты
message_freq = 10
carrier_freq = 70


#5й номер
def filter_signal():
    #создание однополярного меандра
    message = np.sign(np.sin((2 * np.pi * t) * message_freq))
    for i in range(len(message)):
        if message[i] < 0:
            message[i] = 0

    demod_cut_signal = demodulate(cutted_signal, carrier_freq, len(cutted_signal))

    # получение точек в меандре, где график растет\падает
    num = points / (message_freq * 2) # для 5гц = 80; для 10гц = 40 значение, являющееся длиной
                                        # одного "прямоугольника" на графике по оси Х
    j_0 = num / points #для 5гц = 0.1; для 10гц = 0.05 #получение коэффициента, на который будет умножаться points
    j = j_0
    array_meandr = []
    for i in range(message_freq * 2):
        granica = points * j
        array_meandr.append(granica)
        j += j_0

    freqs = np.fft.fftfreq(len(demod_cut_signal), 1.0 / points) #массив из значений по оси Х
    old_granica = 0 #начальная граница
    n = np.arange(0, points)
    freqs = n #добавление в массив точек из points (из оси Х)

    count = 0
    #Исходя из информации, полученной из массива array_meandr, изменяем сигнал, согласно точкам в массиве
    for i in array_meandr:
        if (count % 2 == 0):
            demod_cut_signal[freqs > round(old_granica)] = 1
            demod_cut_signal[freqs > round(i)] = 0
        else:
            demod_cut_signal[freqs > round(old_granica)] = 0
            demod_cut_signal[freqs > round(i)] = 1
        old_granica = i
        count += 1

    plt.title("Модулирующий сигнал (Однополярный меандр)")
    plt.plot(message)
    plt.xlim([0, points])
    plt.show()

    plt.title("Окончательный сигнал")
    plt.plot(demod_cut_signal)
    plt.xlim([0, points])
    plt.show()


if __name__ == "__main__":
    filter_signal()