from typing import TypedDict
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


class PlotterConfig(TypedDict):
    x_axis_label: str
    y_axis_label: str
    window_title: str


class Plotter:
    def __init__(self, config):
        self.x_axis_label = config["x_axis_label"]
        self.y_axis_label = config["y_axis_label"]
        self.title = config["window_title"]

        self.x_data = []
        self.y_data = []
        self.mean_y = []

        self.figure, subplots = plt.subplots()
        self.line, = subplots.plot(self.x_data, self.y_data, '-')
        self.mean_line, = subplots.plot(self.x_data, self.mean_y, '-')

        plt.xlabel(self.x_axis_label)
        plt.ylabel(self.y_axis_label)
        plt.title(self.title)

        self.animation = FuncAnimation(
            self.figure,
            self.__update,
            interval=1000,
            cache_frame_data=False
        )
        plt.ion()
        plt.show(block=False)

    def append(self, x, y):
        self.x_data.append(x)
        self.y_data.append(y)

        self.mean_y.append(sum(self.y_data) / len(self.y_data))

    def __update(self, frame):
        self.line.set_data(self.x_data, self.y_data)
        self.mean_line.set_data(self.x_data, self.mean_y)

        self.figure.gca().relim()
        self.figure.gca().autoscale_view()
        return self.figure,

    def exit(self):
        plt.close()
