from itertools import groupby

import matplotlib
import matplotlib.pylab as plt
import seaborn as sns

from mapping import all_clean


def get_year_splits(trimmed):
    groups = groupby(trimmed.index, lambda x: str(x)[3])

    year_indexes = [0]

    for year, group in groups:
        year_indexes.append(year_indexes[-1] + len(list(group)))

    return year_indexes


def make_setlist_heatmap(trimmed):
    fig, ax = plt.subplots(figsize=(100, 70))

    output = sns.heatmap(trimmed.T, ax=ax, cbar=False, cmap='Blues',
                         linewidths=2, color='white')

    output.set_ylim(len(trimmed.T)+0.5, -5)
    fig.suptitle('A Decade of Streetlight Manifesto Setlists', x=.5, y=.92, fontsize=124);

    # remove x axis tick clutter
    loc = matplotlib.ticker.NullLocator()
    output.xaxis.set_major_locator(loc)

    output.set_xlabel('Shows', fontsize=96)

    # increase y axis readability
    output.yaxis.set_ticklabels((y for y in output.yaxis.get_majorticklabels()),
                                fontsize=20)

    output.annotate('(Oldest)', (-10, -1), fontsize=52, annotation_clip=False)
    output.annotate('(Newest)', (-10, 58), fontsize=52, annotation_clip=False)
    
    # annotate by year
    year_indexes = get_year_splits(trimmed)
    for idx in year_indexes[1:]:
        output.axvline(idx, lw=3, c='k')
    
    output.annotate('2010', (17, -3), fontsize=72)
    output.annotate('2011', (50, -3), fontsize=72)
    output.annotate('2012', (78, -3), fontsize=72)
    output.annotate('2013', (110, -3), fontsize=72)
    output.annotate('2014', (136.5, -3), fontsize=72)        
    output.annotate('2015', (152, -3), fontsize=72)
    output.annotate('2016', (170, -3), fontsize=72)
    output.annotate('2017', (183, -3), fontsize=72)
    output.annotate('2018', (204, -3), fontsize=72)
    output.annotate('2019', (228, -3), fontsize=72)

    # divide albums
    output.axhline(12, lw=3, c='r')
    output.axhline(26, lw=3, c='r')
    output.axhline(36, lw=3, c='r')
    output.axhline(47, lw=3, c='r')
    
    # make album legend
    elem = [Line2D([0], [0], lw=3, c='r', label='Album')]
    output.legend(handles=elem, loc=(.1, .05), fontsize=96, framealpha=1,
              frameon=True, edgecolor='k', facecolor='.9')
    
    return ax

def plot_all_time_plays(trimmed):
    song_counts = trimmed.sum()

    loc = matplotlib.ticker.IndexLocator(base=1, offset=0.5)
    fmtr = matplotlib.ticker.IndexFormatter(all_clean)

    fig, ax = plt.subplots(figsize=(10, 15))

    ax.barh(range(len(song_counts)), song_counts,
            color=((8/255, 48/255, 107/255, 255/255)))


    ax.axhline(11.5, lw=2, c='r')
    ax.axhline(25.5, lw=2, c='r')
    ax.axhline(35.5, lw=2, c='r')
    ax.axhline(46.5, lw=2, c='r')

    ax.set_ylim(57, -1)
    ax.yaxis.set_major_locator(loc)
    ax.yaxis.set_major_formatter(fmtr)

    return ax


def cooccurrence_heatmap(trimmed, play_weighted=False):
    if play_weighted:
        mat = trimmed.corr().dropna(how='all')
    else:
        mat = trimmed.T.dot(trimmed)
        
    mat = mat[mat.index]

    mask = np.zeros_like(mat, dtype=np.bool)
    mask[np.triu_indices_from(mat)] = True
    
    # plot
    fig, ax = plt.subplots(figsize=(20, 15))

    sns.heatmap(mat, ax=ax, mask=mask, cmap='Reds',
                cbar=False);
    if play_weighted:
        fig.suptitle('Song Co-occurrence (Weighted by Plays)',
                     x=.5, y=.92, fontsize=24);
    else:
        fig.suptitle('Song Co-occurrence', x=.45, y=.92, fontsize=24);

    indexes = [12, 26, 36, 43]

    for idx in indexes:
        ax.axhline(idx, xmax=idx/len(mat), c='b', alpha=.5)
        ax.axvline(idx, ymax=(1 - idx/len(mat)), c='b', alpha=.5)
        
    return ax