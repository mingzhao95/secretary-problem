import itertools

import numpy as np
import matplotlib.pyplot as plt
plt.style.use("dark_background")
plt.rcParams["figure.figsize"] = (9,7)
import matplotlib.animation as animation
from secretary import simulate
import time



# histogram our rankings with numpy
N = 200
nsims = 1000
p_accept = 1
p_belated_accept = 0
rankings, time_spent = simulate(N, win=1, nsims=nsims, p_accept=p_accept, p_belated_accept=p_belated_accept)
HIST_BINS = 200  # <= N
xmax = min(N,int(N/HIST_BINS*20))  # the worst ranking partner to display


def init():
    start_pctl = 1-xmax/N;
    xticks = np.linspace(0,xmax,11).round(1);
    ax.set_xlim(xmax, 0)  # flipped l-r
    ax.set_xticks(xticks)
    xticklabels = list(map(lambda _: str(int(100*_))+"th", xticks/N+start_pctl))
    ax.set_xticklabels(xticklabels[::-1], rotation=60)
    ax.set_ylim(0, nsims)
    ax.set_yticks(nsims*np.arange(0,1.1,.1).round(1))
    ax.set_yticklabels(np.arange(0,1.1,.1).round(1))
    ax.set_title("How Great of a Secretary Do You End Up With If ... ", fontweight="bold")
    ax.set_xlabel("Secretary's Rank (Percentile)", fontweight="bold")
    ax.set_ylabel("Probability", fontweight="bold")



def run(bar_containers, annot_tsearch, annot_bars):

    def animate(frame_number):
        # simulate new rankings coming in
        rankings, time_spent = simulate(N, win=frame_number%N, nsims=nsims, p_accept=p_accept, p_belated_accept=p_belated_accept)
        n, _ = np.histogram(rankings, bins=HIST_BINS)
        for _, (count, rect) in enumerate(zip(n, bar_containers.patches)):
            rect.set_height(count)
            annot_bars[_].set_text('{:.2f}'.format(count/nsims))
            annot_bars[_].set_position((bin_centers[_],count))
        annot_tsearch.set_text(f"{int((frame_number % N)/N*100)}%")
        return bar_containers.patches

    return animate


fig, ax = plt.subplots(1,1)
init()
counts, bins, bar_containers = ax.hist(rankings, bins=HIST_BINS, lw=2,
                              ec="yellow", fc="#13f2c2", alpha=1)
bin_centers = 0.5 * np.diff(bins) + bins[:-1]
_, annot_tsearch = ax.annotate(text="Time Spent Searching is: ", xy=(.5*xmax,915), fontsize=12, fontweight="bold"), \
                    ax.annotate(text="0%", xy=(.1*xmax,915), fontsize=12, fontweight="bold", color="#f10d7a")
annot_bars = []
for count, x in zip(counts, bin_centers):
    annot_bars.append(ax.annotate('{:.2f}'.format(count/nsims), xy=(x, count), va='bottom', ha='center', color="yellow"))

ani = animation.FuncAnimation(fig, run(bar_containers, annot_tsearch, annot_bars), interval=50, repeat=True, init_func=init)
plt.show()