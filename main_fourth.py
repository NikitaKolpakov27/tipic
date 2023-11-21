import numpy
import numpy as np
import matplotlib.pyplot as plt
import scipy.fft


def amplitude_modulation(amp, km, fc, f, points):
    # amp - амплитуда сигнала
    # km - коэффициент модуляции
    # fc - частота несущего сигнала
    # f - частота сигнала
    # points - число точек для отрисовки
    x = np.linspace(0, 1, points)
    return amp * (km * (np.sign(np.sin(f * x * 2.0 * np.pi)) + amp)) * np.sin(fc * x * 2.0 * np.pi)


if __name__ == '__main__':
    points = 800
    # графики амплитудной модуляции
    am_sig = amplitude_modulation(1.0, 0.45, 70, 10, points)  # несущая частота - 70 Гц
    plt.subplot(2, 1, 1)
    plt.plot(am_sig)
    plt.title('Амплитудная модуляция')
    plt.xlim([0, (points) - 1])

    plt.subplot(2, 1, 2)
    spectr_sig_am = np.abs(scipy.fft.fft(am_sig)) / (points * 0.5)

    plt.plot(spectr_sig_am)
    plt.xlim([0, 400])  # ограничение. Отсекается ненужная правая часть
    plt.tight_layout()
    plt.show()


#синтезированный сигнал
    plt.title('Синтез сигнала амплитудной модуляции')
    freq = numpy.fft.fftfreq(len(am_sig), 1.0 / points)
    cutted_spec_signal = spectr_sig_am.copy()
    cutted_spec_signal[(freq < 60)] = 0 #обрезание низких частот
    cutted_spec_signal[(freq > 80)] = 0 #обрезание высоких частот
    cutted_signal = scipy.fft.irfft(cutted_spec_signal)


    plt.plot(cutted_signal)
    plt.xlim([0, points])
    plt.tight_layout()
    plt.show()
