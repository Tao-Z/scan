import numpy as np
import pandas as pd
import seaborn as sns
import math
import matplotlib.pyplot as plt

def stat(Points):
    theta = [[math.atan2(point[3], point[4]), math.atan2(point[3], point[5])] for point in Points]
    df = pd.DataFrame(theta, columns=["x", "y"])
    sns.jointplot(x="x", y="y", data=df, kind="hex")
    plt.show()


if __name__ == '__main__':
    import ReadData as RD

    Points = RD.vertices('data/output/sh f.obj')
    stat(Points)
