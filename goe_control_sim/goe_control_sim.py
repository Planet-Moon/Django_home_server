import numpy as np
import matplotlib.pyplot as plt
import datetime

class Leistung:
    def __init__(self, values=0):
        self.max_values = values
        self.returned_values = 0

    def __iter__(self):
        self._leistung_list = np.array([-0.3,-0.2,-0.1,-0.1,-0.1,-0.1,0,1,2,3,4,5,6,7,7.5,8,7.5,7,6,4,3,2,1,0])*1000
        self._iter_index = 0
        return self

    def __next__(self):
        result = self._leistung_list[self.returned_values % self._leistung_list.size]
        self.returned_values += 1
        if self.max_values <= 0 or self.returned_values <= self.max_values:
            return result
        else:
            raise StopIteration

class Inverter:
    def __init__(self, values=0):
        self.leistung = Leistung(values)

class Controller:
    def __init__(self):
        self.alw = False
        self.amp = 0
        self.min_amp = 6

    def update_controller(self, input:float):
        input = input - self.amp * 3*230 # aktuell genutzte leistung
        input_amp = self.amp + (input/(3*230))
        if input_amp > self.min_amp:
            self.amp = input_amp
            self.alw = True
        else:
            self.amp = 0
            self.alw = False
        return self.amp


def main():
    samples = 24*3
    inverter = Inverter(samples)
    leistungen = np.array([i for i in inverter.leistung])
    controller = Controller()
    controller_output = [controller.update_controller(i) for i in leistungen]
    begin_date = datetime.datetime(2021,3,26,0)
    time = np.array([begin_date + datetime.timedelta(hours=i) for i in range(samples)])

    plt.subplot(2,1,1)
    plt.plot(time,leistungen)
    plt.title("Leistungen")
    plt.subplot(2,1,2)
    plt.plot(time,controller_output)
    plt.title("Controller Output")
    plt.show()

if __name__ == '__main__':
    main()
