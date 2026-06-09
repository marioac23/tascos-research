import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Arguments for running code",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-i", "--input", default=None, type = str, help="input list of restaurants/tascas")
parser.add_argument("-o", "--output", default=None, type = str, help="output file")


args = vars(parser.parse_args())


input    = args["input"]
output      = args["output"]

# Load your merged data
df = pd.read_csv(input)


def plot(df, param, labels, output):
    plt.figure()
    plt.scatter(df[param[0]], df[param[1]])
    plt.xaxis(labels[0])
    plt.yaxis(labels[1])
    plt.savefig(output)

def hist(df, param, output):
    plt.figure()
    plt.hist(df[param], bins=100, histtype='step')
    plt.savefig(output)

hist(df=df, param='price_level', output=output+"hist_price_level.png")