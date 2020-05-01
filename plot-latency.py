# Copyright 2020 Matt Fleming
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import sys
import seaborn as sns
import argparse

parser = argparse.ArgumentParser(description='Print scheduler stats')
parser.add_argument("--cdf", action='store_true',
        help="Plot the latency as a cummulative distribution frequency")
parser.add_argument("--title", metavar='t', type=str, nargs=1,
        help="Set the graph title")
parser.add_argument("--subtitle", type=str, nargs=1,
        help="Set the subplot title")
parser.add_argument("--xlim", type=int, nargs=1,
        help="Set the x-axis limits")
parser.add_argument("--ylim", type=int, nargs=1,
        help="Set the y-axis limits")
parser.add_argument("--output", type=str, nargs=1,
        help="Save the figure to output")
parser.add_argument("file", metavar='f', type=str, nargs=1,
        help="read this perf.data file")
parser.add_argument("pids", metavar='p', type=int, nargs='+',
        help="create a chart for this pid")

args = parser.parse_args()

#server_pid = 7648
#client_pid = 7653
data = pd.read_csv(args.file[0], index_col=0, parse_dates=True)
#server = data.loc[data["pid"] == server_pid, "delay"]
#client = data.loc[data["pid"] == client_pid, "delay"]
#print(server.describe())
#print(client.describe())
pid_data = {}
pids = args.pids
for p in pids:
    print(p)
    pid_data[p] = data.loc[data["pid"] == p, "delay"]
    print(pid_data[p].describe())

# Use seaborn style defaults and set the default figure size
#sns.set(rc={'figure.figsize':(11, 4)})

if len(pids) == 4:
    fig, ax = plt.subplots(2, 2)
else:
    fig, ax = plt.subplots(len(pids), 1)

# make a little extra space between the subplots
fig.subplots_adjust(hspace=0.5)

#client_ax = data[data["pid"] == client_pid].plot(marker='.',
#        linestyle='None', ax=ax[0])
# Set y-ticks for known values we want to see
#client_ax.set_yticks([0, 4, max(client)])

#server_ax = data[data["pid"] == server_pid].plot(marker='.',
#        linestyle='None', ax=ax[1])
#server_ax.set_yticks([0, 4, max(server)])

if args.title:
    fig.suptitle(args.title[0])

def plot_cdf(p, a):
    #ser = pd.Series(pid_data[p])
    stats_df = data.loc[data["pid"] == p].groupby('delay')['delay'] \
            .agg('count').pipe(pd.DataFrame) \
            .rename(columns = {'delay': 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])
    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()
    stats_df = stats_df.reset_index()
    # Plot
    p_ax = stats_df.plot(x = 'delay', y = 'cdf', legend=None, ax=a)
    p_ax.set_xlabel("latency (µs)")
    #p_ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    # manipulate
    vals = p_ax.get_yticks()
    p_ax.set_yticklabels(['{:,.2%}'.format(x) for x in vals])

    if args.xlim:
        p_ax.set_xlim(0, args.xlim[0])
    if args.ylim:
        p_ax.set_ylim(0, args.ylim[0])


def plot_plot(a):
    p_ax = pid_data[p].plot(marker='.',
            linestyle='None', ax=a, legend=None)
    #p_ax.set_yticks(0, max(pid_data[p]))
    p_ax.set_ylabel("latency (µs)")
    p_ax.set_xlabel("Time")
    if args.subtitle:
        p_ax.set_title(args.subtitle[0])
    else:
        p_ax.set_title("pid=" + str(p))
    if args.xlim:
        p_ax.set_xlim(0, args.xlim[0])
    if args.ylim:
        p_ax.set_ylim(0, args.ylim[0])

col = 0
row = 0

def do_plot(p, a):
    if args.cdf:
        plot_cdf(p, a)
    else:
        plot_plot(a)

for p in pids:
    if len(pids) == 4:
        a = ax[row][col]
        col = (col+1)%2
        # New row?
        if col == 0:
            row += 1
    elif len(pids) > 1:
        a = ax[row]
        row += 1
    else:
        a = ax
        row += 1

    do_plot(p, a)

if args.output:
    fig.savefig(args.output[0])

plt.show()
