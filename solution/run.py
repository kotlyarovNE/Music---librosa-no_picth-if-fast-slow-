#!/usr/bin/python 

import numpy as np
import librosa as lb
from IPython.display import Audio
from sys import argv
import soundfile as sf
import warnings
import os
import sys

def record_stretch(sound_array, r, N):
    """ Растягиваем/сокращаем звук звук в r раз!!!
        N - размер окна Ханнинга
    """
    #определяем окна ханнинга:
    Hann_win = np.hanning(N)
    #Перекрытие 75% или скачок
    hop_a = N//4
    delta_t = hop_a/22050.
    #Инициализируем начальную фазу для Frame 0 (первого окна)
    phi  = np.zeros(N)
    #Инициализируем вектор ответов нужной длинны:
    result = np.zeros( int(len(sound_array) * r)+N, dtype = 'complex')
    #Идем по окнам с шагом hop_a
    for i in np.arange(0, len(sound_array)-N-hop_a, hop_a):
        #начало окна для выхода:
        start = int(i*r)
        #Запоминаем два подрят идущих окна
        x, x_next = sound_array[i:i+N], sound_array[i+hop_a:i+hop_a+N]

        # Делаем БПФ (быстрое преобрю Фурье) для обоих окон помноженных окно Ханнинга
        X =  np.fft.fft(Hann_win*x)
        X_next =  np.fft.fft(Hann_win*x_next)

        #Написал как в статье, правда не очень понял, зачем именно так делать по сути
        #Ведь мы просто можем сразу узнать разность фаз через np.angle
        #тогда мы не делим на delta_t, и погрешность вычислений будет меньше
        #phi = (phi + np.angle(X_next)-np.angle(X)) % 2*np.pi

        w_bin = np.fft.fftfreq(N, 1/(2 * np.pi))

        delta_w = (np.angle(X_next/X))/delta_t - w_bin

        delta_w_wrapt = np.mod(delta_w,2*np.pi)-np.pi

        w_true = w_bin + delta_w_wrapt

        phi += delta_t*(w_true)

        #Делаю ОБПФ, доворачивая на нужный угол next окно, не меняя модуль т.е. умножение на экспоненту
        x_next_new = np.fft.ifft(X_next*np.exp(phi*1j))
        #Умножем на окно Ханнинга
        #X_next_new*=Hann_win
        # Теперь осталось только растянуть равномерно перекрытия окон, чтобы выход был нужного размера
        result[start : start + N] += x_next_new*Hann_win

    # В конце отнормируем выход аудио, чтобы он стал похож на вход 
    #result = np.max(np.abs(x))*result/np.max(np.abs(result))
    return np.real(result)

def main(argv):
    warnings.filterwarnings("ignore")
    if(len(argv)!=4):
        print('incorrect data input, pleas input: path, patch, r')
        return -1
    input_path, output_patch, r = argv[1:]
    if(float(r)<=0):
        print('Incorrect parametr r!')
        return -1
    #Ширина окна
    N = 2024
    try:
        x, sample_rate = lb.load(input_path)
        xx = record_stretch(x, float(r), 2024)
        a = ''
        for i in output_patch.split('/')[:-1]:
            a+=i
            a+="\\"
        if(a!=''):
            os.makedirs(a,  exist_ok=True)
        sf.write(output_patch, xx, sample_rate)
    except:
        print('No such file or directory! or Incorrect output format!')


if __name__ == "__main__":
    try:
        argv = sys.argv
        main(argv)
    except (EOFError):
        print('error!')
