import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from kmeans import kmeans_clustering
from maxmin import maxmin_clustering
from common import *


def change_max_states(slider, states):
    slider.valmax = len(states)
    slider.ax.set_xlim(slider.valmin, slider.valmax)
    if slider.val > slider.valmax:
        slider.set_val(slider.valmax)


def main():
    matplotlib.use('TkAgg')

    max_points_num = 100000

    plot = plt.subplot(111)
    plt.subplots_adjust(bottom=0.35)

    ax_points = plt.axes([0.1, 0.2, 0.8, 0.05])
    ax_maxmin_states = plt.axes([0.1, 0.15, 0.8, 0.05])
    ax_kmeans_states = plt.axes([0.1, 0.1, 0.8, 0.05])
    ax_button = plt.axes([0.1, 0.05, 0.8, 0.05])

    slider_points = Slider(ax_points, 'Points', 1000, max_points_num, valinit=1000, valstep=1)
    slider_minmax_states = Slider(ax_maxmin_states, 'MaxMin States', 1, 2, valinit=1, valstep=1)
    slider_kmeans_states = Slider(ax_kmeans_states, 'KMeans States', 1, 2, valinit=1, valstep=1)
    evaluate = Button(ax_button, 'Evaluate')

    maxmin_states = []
    kmeans_states = []

    def draw_state(current_state):
        plot.clear()
        current_state.show(plot)
        plt.draw()

    def update_maxmin_states(val):
        if val < slider_minmax_states.valmax:
            slider_kmeans_states.set_val(1)
        current_state = maxmin_states[val - 1]
        draw_state(current_state)

    def update_kmeans_states(val):
        if val > 1:
            slider_minmax_states.set_val(slider_minmax_states.valmax)
        current_state = kmeans_states[val - 1]
        draw_state(current_state)

    def update(val):
        nonlocal maxmin_states, kmeans_states
        points_num = int(slider_points.val)
        points = generate_points(points_num)
        maxmin_states = maxmin_clustering(points)
        kmeans_states = kmeans_clustering(maxmin_states[-1])
        change_max_states(slider_minmax_states, maxmin_states)
        change_max_states(slider_kmeans_states, kmeans_states)
        slider_minmax_states.set_val(1)

    slider_minmax_states.on_changed(update_maxmin_states)
    slider_kmeans_states.on_changed(update_kmeans_states)
    evaluate.on_clicked(update)

    update(None)
    plt.show()


if __name__ == '__main__':
    main()
