import numpy as np
import matplotlib.pyplot as plt
plt.style.use("dark_background")
plt.rcParams["figure.figsize"] = (4,3)

def get_partner_rank(arr, win, p_accept, p_belated_accept):
    """ You sample the first `win` (# of) suitors without choosing any (search window).
        Then you choose the first suitor from the remainder (leap window) who is better than everyone in the search window.
        That person has a p_accept % chance of saying "yes" to you. If you're rejected, keep trying.
        How great is your final choice partner (i.e. what is his/her global rank? what % of time do you end up with the overall best?)
        
        Return: global rank of your final choice partner, total number of suitors viewed
    """
    look_arr = arr[:win]
    leap_arr = arr[win:]
    rejections = []
    if leap_arr == []:
        raise Exception("search window must be less than len(arr)!")
    if look_arr == []: # don't look, just leap
        index_of_chosen = 1
        accept = np.random.choice([True, False], p=[p_accept, 1-p_accept])
        while not accept:
            index_of_chosen += 1
            accept = np.random.choice([True, False], p=[p_accept, 1-p_accept])
        chosen = leap_arr[index_of_chosen-1]
    else:
        benchmark = max(look_arr)
        chosen = ''
        for _, suitor in enumerate(leap_arr):
            if suitor>benchmark:
                accept = np.random.choice([True, False], p=[p_accept, 1-p_accept])
                if accept:
                    chosen = suitor
                    break
                else:
                    rejections.append(suitor) # you got rejected
            else:
                pass # suitor does not meet benchmark
        index_of_chosen = win + 1 + _
        if chosen == '':  # none chosen/accepted after going through everyone in the leap_arr
            if p_belated_accept == 0:
                chosen = sorted(arr, reverse=True)[-1] # if u can't go back to previous candidates, then assume u end up with the worst
            elif p_belated_accept > 0:
                new_leap_array = arr[:]
                for rej in rejections:
                    new_leap_array.remove(rej)
                sorted_new_leap = sorted(new_leap_array, reverse=True)
                while chosen == '':
                    belated_accept = np.random.choice([True, False], p=[p_belated_accept, 1-p_belated_accept])
                    try:
                        if belated_accept:
                            chosen = sorted_new_leap[0]
                        else:  # rejected
                            sorted_new_leap.remove(sorted_new_leap[0])
                    except:
                        chosen = sorted(arr, reverse=True)[-1]
                        # you've been rejected by everyone; assume u end up with the worst

    sorted_arr = sorted(arr, reverse=True)
    rank_of_chosen = sorted_arr.index(chosen) + 1
    return rank_of_chosen, index_of_chosen


def simulate(N, win, nsims, p_accept, p_belated_accept, show=False):
    """ N: size of the global population
        win: your search window size (# < N)

        Returns: array of size `nsims` showing your partner's ranking on each sim
    """
    rankings = []; time_spent = []
    for _ in range(nsims):
        # arr = np.random.normal(0,1,N)
        arr = np.random.uniform(0,1,N)
        rank, ind = get_partner_rank(arr, win, p_accept, p_belated_accept)
        rankings.append(rank)
        time_spent.append(ind)

    if show:
        plt.hist(rankings)
        plt.show()

    return rankings, time_spent

def probability_of_best_partner(rankings):
    count = rankings.count(1)
    return count/len(rankings)

def probability_of_top_Xth_percentile_partner(x, N, rankings):
    count = sum(map(lambda _ : _ < x/100*N, rankings))
    return count/len(rankings)


if __name__=='__main__':

    p_best_vs_win = []
    p_top5_vs_win = []
    p_top10_vs_win = []

    p_best_vs_win_wrej = []
    p_top5_vs_win_wrej = []
    p_top10_vs_win_wrej = []

    N=200
    p_accept = 1
    p_belated_accept = 0
    for search_window in range(1, N):
        rankings, time_spent = simulate(N, search_window, nsims=2000, p_accept=p_accept, p_belated_accept=p_belated_accept)
        print(f"Population: {N}, Searching Window: {search_window}\n")
        print(f"Probability of finding best: {probability_of_best_partner(rankings)}")
        print(f"Probability of finding top 10%: {probability_of_top_Xth_percentile_partner(10, N, rankings)}")
        print(f"Avg. # of suitors evaluated: {np.mean(time_spent)}")
        print("============================\n")
        
        p_best_vs_win.append(probability_of_best_partner(rankings))
        p_top5_vs_win.append(probability_of_top_Xth_percentile_partner(5, N, rankings))
        p_top10_vs_win.append(probability_of_top_Xth_percentile_partner(10, N, rankings))

        rankings_wrej, time_spent_wrej = simulate(N, search_window, nsims=2000, p_accept=0.5, p_belated_accept=p_belated_accept)
        p_best_vs_win_wrej.append(probability_of_best_partner(rankings_wrej))
        p_top5_vs_win_wrej.append(probability_of_top_Xth_percentile_partner(5, N, rankings_wrej))
        p_top10_vs_win_wrej.append(probability_of_top_Xth_percentile_partner(10, N, rankings_wrej))
    

    fig, ax = plt.subplots(2,1)
    plt.tight_layout()
    fig.suptitle("Optimum Search Window Depends on Your Standards + THEIR STANDARDS!!!", color="#13f2c2", fontweight="bold")
    fig.supylabel('Probability')
    fig.supxlabel('Search Window Size (% of candidates)')

    shared_x = (np.arange(1, N)/N*100).round(0)
    
    ax[0].set_title("Probability of Finding the Best Partner", loc="right")
    paccept100, = ax[0].plot(shared_x, p_best_vs_win, color="#f10d7a")
    opt_win_best = shared_x[np.argmax(p_best_vs_win)]
    ax[0].vlines(x=opt_win_best, ymin=0, ymax=1, colors="#f10d7a", linestyles="dashed")
    ax[0].annotate(text=f"  optimum search size: {opt_win_best}\n  probability: {max(p_best_vs_win)}", xy=(opt_win_best, .8), color="#f10d7a")
    paccept50,  = ax[0].plot(shared_x, p_best_vs_win_wrej, color="yellow")
    opt_win_best_wrej = shared_x[np.argmax(p_best_vs_win_wrej)]
    ax[0].vlines(x=opt_win_best_wrej, ymin=0, ymax=1, colors="yellow", linestyles="dashed")
    ax[0].annotate(text=f"  optimum search size: {opt_win_best_wrej}\n  probability: {max(p_best_vs_win_wrej)}", xy=(opt_win_best_wrej, .6), color="yellow")
    ax[0].legend([paccept100,paccept50],
        ['100% chance of acceptance', '50% chance of acceptance'])

    ax[1].set_title("Probability of Finding a Top 5% Partner", loc="right")
    paccept100_top5, = ax[1].plot(shared_x, p_top5_vs_win, color="#f10d7a")
    opt_win_top5 = shared_x[np.argmax(p_top5_vs_win)]
    ax[1].vlines(x=opt_win_top5, ymin=0, ymax=1, colors="#f10d7a", linestyles="dashed")
    ax[1].annotate(text=f"  optimum search size: {opt_win_top5}\n  probability: {max(p_top5_vs_win)}", xy=(opt_win_top5, .1), color="#f10d7a")
    paccept50_top5,  = ax[1].plot(shared_x, p_top5_vs_win_wrej, color="yellow")
    opt_win_top5_wrej = shared_x[np.argmax(p_top5_vs_win_wrej)]
    ax[1].vlines(x=opt_win_top5_wrej, ymin=0, ymax=1, colors="yellow", linestyles="dashed")
    ax[1].annotate(text=f"  optimum search size: {opt_win_top5_wrej}\n  probability: {max(p_top5_vs_win_wrej)}", xy=(opt_win_top5_wrej, .6), color="yellow")
    ax[1].legend([paccept100_top5,paccept50_top5],
        ['100% chance of acceptance', '50% chance of acceptance'])

    # ax[2].plot(shared_x, p_top10_vs_win)
    # ax[2].set_title("Probability of Finding a Top 10% Partner", loc="right")
    # opt_win_top10 = shared_x[np.argmax(p_top10_vs_win)]
    # ax[2].vlines(x=opt_win_top10, ymin=0, ymax=1, colors="#f10d7a", linestyles="dashed")
    # ax[2].annotate(text=f"  optimum search size: {opt_win_top10}\n  probability: {max(p_top10_vs_win)}", xy=(opt_win_top10, .1), color="#f10d7a")

    plt.show()
    


