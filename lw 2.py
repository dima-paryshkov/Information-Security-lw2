from turtle import goto
from Crypto.Util import number 
from math import gcd, sqrt
import random
import numpy as np
import PySimpleGUI as sg


def seq_to_str(gen):
    new_gen = str(gen).replace(',','')
    return new_gen[1:len(new_gen)-1]

def concl_str(S):
    if S <= 1.82138636:
        return 'S < 1.821 => Тест пройден'
    else:
        return 'S > 1.821 => Тест не пройден'

class RSA:
    def __init__(self):
        self.t1 = { 'step1': '',
                    'step2': '',
                    'step3': '',
                    'result': '',
                    'is_passed': None }

        self.t2 = { 'step1': '',
                    'step2': '',
                    'step3': '',
                    'result': '',
                    'is_passed': None }

        self.t3 = { 'step1': '',
                    'step2': '',
                    'step3': '',
                    'step4': '',
                    'tabl': { 'j': [],
                              'etta': [],
                              'Y': [],
                              'is_passed': [] },
                    'result': '',
                    'is_passed': None }
       
        self.seq = None
    
    def alg(self, m):
        n1, n2 = number.getPrime(160), number.getPrime(160)

        N = n1 * n2
        fi = (n1 - 1) * (n2 - 1)

        K = 0
        for k in range(3, fi, 2):
            if gcd(k, fi) == 1:
                K = k
                break
        xi = []
        for i in range(m):
            ui = random.randint(2, N-1)
            ui = (ui ** K) % N
            xi.append(ui % 2)

        return xi

    def genRSA(self, m):
        xi = self.alg(m)
        # Исключа-ем случаи, когда последовательность целиком состоит из 1 или 0
        # (возникает при малых n)
        while sum(xi) == m or sum(xi) == 0:
            xi = self.alg(m)
        
        self.seq = xi
        self.test1()
        self.test2()
        self.test3()
        return seq_to_str(xi)
    
    def test1(self):
        gen = self.seq
        g1 = list(map(lambda x: 1 if x==1 else -1, gen))
        self.t1['step1'] = seq_to_str(g1)
        self.t1['step2'] = str(sum(g1))
        
        S = abs(sum(g1)) / len(g1)
        self.t1['step3'] = str(round(S, 3))
        self.t1['result'] = concl_str(S)
        self.t1['is_passed'] = S <= 1.82138636

    def test2(self):
        gen = self.seq
        n = len(gen)
        pi = sum(gen) / n
        self.t2['step1'] = str(round(pi, 3))

        V = 1
        for i in range(n - 1):
            V += int(gen[i] != gen[i + 1])
        self.t2['step2'] = str(V)
        
        S = abs(V - 2*n*pi*(1-pi)) / (2*sqrt(2*n)*pi*(1-pi))
        self.t2['step3'] = str(round(S, 3))
        self.t2['result'] = concl_str(S)
        
        self.t2['is_passed'] = S <= 1.82138636

    def test3(self):
        gen = self.seq

        n = len(gen)
        gen_ = list(map(lambda x: 1 if x==1 else -1, gen))
        self.t3['step1'] = seq_to_str(gen_)

        S_ = []
        for i in range(n):
            S_.append(sum(gen[:i]))
            
        self.t3['step2'] = seq_to_str(S_[1:])
        S_.append(0)
        self.t3['step3'] = seq_to_str(S_)

        L = S_.count(0) - 1
        self.t3['step4'] = str(L)

        etta = []
        Y = []
        J = list(range(-9, 0)) + list(range(1, 10))
        for j in J:
            etta_i = S_.count(j)
            etta.append(etta_i)
            Y_i = abs(etta_i - L) / sqrt(2 * L * (4*abs(j) - 2))
            Y.append(Y_i)

        self.t3['tabl']['j'] = J
        self.t3['tabl']['etta'] = etta
        self.t3['tabl']['Y'] = [round(l, 3) for l in Y]
        self.t3['tabl']['is_passed'] = list(map(lambda x: '+' if x < 1.82138636 else '-', Y))
        self.t3['is_passed'] = sum(list(map(lambda x: x > 1.82138636, Y))) == 0
        self.t3['result'] = self.bool_to_ans(self.t3['is_passed'])
        #re-turn sum(list(map(lambda x: x > 1.82138636, Y))) == 0 # np.array(Y) <= 1.82138636

    def bool_to_ans(self, res_bool):
        return 'Пройден' if res_bool else 'Не пройден'

    def get_tests_res(self):
        return [self.bool_to_ans(self.t1['is_passed']), 
                self.bool_to_ans(self.t2['is_passed']),
                self.bool_to_ans(self.t3['is_passed'])]

    def get_test1(self):
        return self.t1

    def get_test2(self):
        return self.t2

    def get_test3(self):
        return self.t3

a = RSA()
m = RSA.genRSA(a, 10)

#sg.theme('DarkAmber')
#sg.theme('Topanga')
layout = [
    [sg.Text('Sequence length:'), sg.InputText(), sg.Button('Generate', expand_x=100)],
    [sg.Text('Generated sequence:')],
    [sg.MLine(key='-ML1-'+sg.WRITE_ONLY_KEY, size=(88,10))],
    [sg.Text('Test results:'), sg.Button('Run tests', expand_x=100)],
    [sg.MLine(key='-ML2-'+sg.WRITE_ONLY_KEY, size=(88,10))]
]
window = sg.Window('RSA', layout, grab_anywhere=True)
while True:                             # The Event Loop
    event, values = window.read()
    # print(event, values) #debug-
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'Generate':
        event, values = window.read()
        
        if values[0]=='':
            window['-ML1-'+sg.WRITE_ONLY_KEY].Update('')
            window['-ML1-'+sg.WRITE_ONLY_KEY].print('Incorrect sequence length')
        else:
            m = int(values[0])
            Sequence = RSA.genRSA(a, m)
            Sequence.replace(' ', '')
            window['-ML1-'+sg.WRITE_ONLY_KEY].Update('')
            window['-ML1-'+sg.WRITE_ONLY_KEY].print(Sequence)
            f = open('result.txt', 'w')
            f.write(Sequence)
            f.close()
    if event == 'Run tests':
        event, values = window.read()
        if values[0]=='':
            window['-ML2-'+sg.WRITE_ONLY_KEY].Update('')
            window['-ML2-'+sg.WRITE_ONLY_KEY].print('Incorrect sequence length')
        else:
            m = int(values[0])
            Sequence = RSA.genRSA(a, m)
            window['-ML2-'+sg.WRITE_ONLY_KEY].Update('')
            t1 = a.get_test1()
            t2 = a.get_test2()
            t3 = a.get_test3()
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"Test 1: {t1['result']}")
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"Test 2: {t2['result']}")
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"Test 3: {t3['result']}")

            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f'Test 1 info:')
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"step1: {t1['step1']}")
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"step2: {t1['step2']}")
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"step3: {t1['step3']}")
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(t1['result'])

            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f'Test 2 info:')
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"step1: {t2['step1']}")
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"step2: {t2['step2']}")
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"step3: {t2['step3']}")
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(t2['result'])

            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f'Test 3 info:')
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"step1: {t3['step1']}")
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"step2: {t3['step2']}")
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"step3: {t3['step3']}")
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"j = {t3['tabl']['j']}")
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"etta = {t3['tabl']['etta']}")
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"is_passed = {t3['tabl']['is_passed']}")
            window['-ML2-'+sg.WRITE_ONLY_KEY].print(t3['result'])
            f = open('result.txt', 'w')
            f.write(Sequence)
            f.close()
