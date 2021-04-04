import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv
import os
import re

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

def read_csv_logs():
    files = [f for f in os.listdir(".") if os.path.isfile(os.path.join(".", f)) and ".csv" in f]
    # files = [files[0]]
    values = dict()
    keys = list()
    for file in files:

        with open(file, "r") as f:
            csv_reader = csv.reader(f, delimiter=";", quotechar="\"")
            lines = []
            for line in csv_reader:
                lines.append(line)
        time_key = datetime.datetime.strptime("-".join(file.split(".")[0].split("_")[-3:]),"%Y-%m-%d")
        lines[0][0] = "time"
        file_keys = [i.split("/")[0].replace(" ","") for i in lines[0]]
        for i in file_keys:
            if i not in keys:
                keys.append(i)

        lines = list(map(list, zip(*lines[1:]))) # transpose


        for i in range(len(lines)):
            if i > 0: # measurement columns
                for j in range(len(lines[i])):
                    lines[i][j] = lines[i][j].replace(" ","")
                    if not lines[i][j]:
                        lines[i][j] = "0"
                    lines[i][j] = float(lines[i][j].replace(".",""))
            else: # time column
                for j in range(len(lines[0])):
                    re_match = re.findall(r"[0-9]{2}:[0-9]{2}",lines[i][j])
                    if re_match:
                        lines[i][j] = re_match[0]
                    time_ = datetime.datetime.strptime(lines[i][j],"%H:%M")
                    if time_.hour == 0 and time_.minute == 0:
                        time_ = datetime.timedelta(hours=24,minutes=time_.minute)
                    else:
                        time_ = datetime.timedelta(hours=time_.hour,minutes=time_.minute)
                    lines[i][j] = time_key + time_
        file_values = dict()

        for i in range(len(lines)):
            file_values[file_keys[i]] = lines[i]

        for _key, _value in file_values.items():
            try:
                values[_key].extend(_value)
            except KeyError:
                values[_key] = _value

    for key, value in values.items():
        values[key] = np.array(value)
    return values

def main():
    cwd = os.path.dirname(__file__)
    os.chdir(cwd)

    samples = 24*3
    inverter = Inverter(samples)
    netz_delta_power = np.array([i for i in inverter.leistung])

    data = read_csv_logs()
    solar_share = 0.5
    netz_delta_power = (data.get('Netzeinspeisung')-data.get('Netzbezug'))/solar_share

    controller = Controller()
    controller_output = [controller.update_controller(i) for i in netz_delta_power]
    begin_date = datetime.datetime(2021,3,26,0)
    time = np.array([begin_date + datetime.timedelta(hours=i) for i in range(samples)])
    time = data.get("time")


    plt.subplot(2,1,1)
    plt.plot(time,netz_delta_power)
    plt.plot(time,data.get("PV-Erzeugung"))
    plt.plot(time,data.get("Direktverbrauch"))
    for i in range(6,20):
        trigger_line = i*690*np.ones(time.size)
        plt.plot(time,trigger_line,"-.")
    plt.title("PV-Erzeugung")
    plt.legend(["Netzeinspeisung","PV-Erzeugung","Direktverbrauch"])
    plt.subplot(2,1,2)
    plt.plot(time,controller_output)
    plt.title("Controller Output")
    plt.show()

if __name__ == '__main__':
    main()
