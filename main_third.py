import numpy as np
import matplotlib.pyplot as plt
import scipy.fft
from scipy.fftpack import rfft

def amplitude_modulation(amp, km, fc, f, points):
    # amp - амплитуда сигнала
    # km - коэффициент модуляции
    # fc - частота несущего сигнала
    # f - частота сигнала
    # points - число точек для отрисовки
    x = np.linspace(0, 1, points)
    return amp * (km * (np.sign(np.sin(f * x * 2.0 * np.pi)) + amp)) * np.sin(fc * x * 2.0 * np.pi)

def frequency_modulation(amp, f, points):
    # amp - амплитуда сигнала
    # f - частота сигнала
    # points - число точек для отрисовки
    x = np.linspace(0, 1, points)
    mod_fsk = (np.sign(np.sin(f * x * 2.0 * np.pi)) + amp)
    mod_frq = np.zeros(points)
    mod_frq[mod_fsk == 0] = 10 #минимальное значение - 10
    mod_frq[mod_fsk == 2] = 50 #максимальное значение - 50

    return amp * np.sin(mod_frq * x * 2.0 * np.pi)

def phase_modulation(amp=1.0, kd=0.25, fc=10.0, f=2.0, points=100):
    # amp - амплитуда сигнала
    # kd - отклонение фазы
    # fc - частота несущего сигнала
    # f - частота сигнала
    # points - число точек для отрисовки
    x = np.linspace(0, 1, points)
    return amp * np.sin(fc * x * 2.0 * np.pi + kd * amp * (np.sign(np.sin(f * x * 2.0 * np.pi)) + amp))


if __name__ == '__main__':
    points = 800
#графики амплитудной модуляции
    am_sig = amplitude_modulation(1.0, 0.45, 70, 10, points) #несущая частота - 70 Гц
    plt.subplot(2, 1, 1)
    plt.plot(am_sig)
    plt.title('Амплитудная модуляция')
    plt.xlim([0, (points) - 1])

    plt.subplot(2, 1, 2)
    spectr_sig_am = np.abs(scipy.fft.fft(am_sig)) / (points * 0.5)

    plt.plot(spectr_sig_am)
    plt.xlim([0, 400]) #ограничение. Отсекается ненужная правая часть
    plt.tight_layout()
    plt.show()

#графики частотной модуляции
    fm_sig = frequency_modulation(1.0, 5, points)
    plt.subplot(2, 1, 1)
    plt.plot(fm_sig)
    plt.title('Частотная модуляция')
    plt.xlim([0, (points) - 1])

    plt.subplot(2, 1, 2)

    spectr_sig_fm = np.abs(scipy.fft.fft(fm_sig)) / (points * 0.5)
    plt.plot(spectr_sig_fm)
    plt.xlim([0, 400]) #ограничение. Отсекается ненужная правая часть
    plt.tight_layout()
    plt.show()

#графики фазовой модуляции
    pm_sig = phase_modulation(1.0, 9, 30, 15, points) #несущая частота - 30 Гц
    plt.subplot(2, 1, 1)
    plt.plot(pm_sig)
    plt.title('Фазовая модуляция')
    plt.xlim([0, (points) - 1])

    plt.subplot(2, 1, 2)

    spectr_sig_pm = np.abs(scipy.fft.fft(pm_sig)) / (points * 0.5)
    plt.plot(spectr_sig_pm)
    plt.xlim([0, 400]) #ограничение. Отсекается ненужная правая часть
    plt.tight_layout()
    plt.show()
