"""Tool to plot infer some analysis on TPO"""
from dataclasses import dataclass, field
from os import listdir
import matplotlib.pyplot as plt
from pandas import DataFrame, read_csv, concat
from sklearn.linear_model import LinearRegression

# import display
#
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


def ZeroOfCurve(df, start, end):
    """Return the zero of a curve in a given interval"""
    # create a dataframe with the interval
    df = df[start:end]
    # find the index of the first value that is bigger than 0
    index = df[df > 0].index[0]
    return index


def Integral(df, interval):
    """Calculate the integral of a dataframe in a given interval"""
    # create a dataframe with the interval
    df = df[interval[0]:interval[1]]
    # calculate the integral
    integral = np.trapz(df, df.index)
    return integral


def MaxPoint(df, start_index, end_index):
    """Max point of a dataframe in an interval of the indices"""
    max_value = df[start_index:end_index].max()
    max_index = df[start_index:end_index].idxmax()
    return max_value, max_index

 # define the point F0, F1, F2


def PlotPoints(mean, std):

    plt.plot(MaxPoint(mean, 0, 8,)[1],  MaxPoint(mean, 0, 8,)[0], 'o', color="C8", label=r"F0 : {:.2f} $\pm$ {}".format(
        MaxPoint(mean, 0, 8,)[0], round(std[MaxPoint(mean, 0, 8,)[1]], 2)))
    # same for [35 : 50]#
    plt.plot(MaxPoint(mean, 0, 35,)[1],  MaxPoint(mean, 0, 35,)[0], 'o', color="C1", label=r"F1 : {:.2f} $\pm$ {}".format(
        MaxPoint(mean, 0, 35,)[0], round(std[MaxPoint(mean, 0, 35,)[1]], 2)))
    # same for [35 : 50]
    plt.plot(MaxPoint(mean, 35, 50,)[1],  MaxPoint(mean, 35, 50,)[0], 'o', color="C3", label=r"F2 : {:.2f} $\pm$ {}".format(
        MaxPoint(mean, 35, 50,)[0], round(std[MaxPoint(mean, 35, 50,)[1]], 2)))

    F0_x = MaxPoint(mean, 0, 8,)[1]
    F1_x = MaxPoint(mean, 0, 35,)[1]
    F2_x = MaxPoint(mean, 35, 50,)[1]
    # a0 = first point in mean that is bigger then 1.0
    a0 = mean[mean > 1.0].index[0]
    print("a0", a0)
    # a1 = F1_x
    a1 = F1_x
    # b0 = F0_x
    b0 = F1_x
    # b1 first point after b0 that is smaller than 0
    b1 = mean[mean < 0].index[0]
    c0 = b1
    # c1 is the biggest index in mean such that
    c1 = ZeroOfCurve(mean, b1, 50)
    d0 = c1
    d1 = F2_x
    e0 = F2_x
    A = mean[e0:]
    e1 = A[A < 0].index[0]

    # define the intervals a, b, c, d, e
    a = [a0, a1]
    b = [b0, b1]
    c = [c0, c1]
    d = [d0, d1]
    e = [e0, e1]
    print("a", Integral(mean, a))
    print("b", Integral(mean, b))
    print("c", Integral(mean, c))
    print("d", Integral(mean, d))
    print("e", Integral(mean, e))
    # calculate the integral of the mean

    # add the integrals to the label
    plt.plot([], [], ' ', label="$area\, a$ = {:.3f}".format(
        Integral(mean, a)))
    plt.plot([], [], ' ', label="$area\, b$ = {:.3f}".format(
        Integral(mean, b)))
    plt.plot([], [], ' ', label="$area\, c$ = {:.3f}".format(
        Integral(mean, c)))
    plt.plot([], [], ' ', label="$area\, d$ = {:.3f}".format(
        Integral(mean, d)))
    plt.plot([], [], ' ', label="$area\, e$ = {:.3f}".format(
        Integral(mean, e)))


# Global variables
SHOW_PLOTS = False
TEST_OUT = False


def CriticalPOint(df, a, b):
    """Return the critical point of a curve in a given interval"""
    # from df extract the df in the interval [a, b]
    df = df[a:b]
    max_x = df.idxmax()
    max_y = df.max()
    return max_x, max_y


@dataclass
class Measurment:
    """Class to represent a measurment"""
    filename: str
    data: DataFrame = field(init=False)

    def __post_init__(self):
        self.data = read_csv(self.filename, sep=';', header=0, skiprows=10)
        self.data = self.data.apply(lambda x: x.str.replace(',', '.'))
        #
        self.data = self.data.astype(float)
        self.data.columns = ["Time", 'Displacement', "Force"]

        self.data = self.data.drop(columns=['Time'])
        # use displacement as index

        self.data = self.data.set_index('Displacement')

        # split the data in 4ths
        d1 = self.data.iloc[:int(len(self.data)/4)]

        # index of d1 / 1000
        d1.index = d1.index/1000
        # d2 = self.data.iloc[int(len(self.data)/4):int(len(self.data)/2)]

        # take the derivative wrt the index

        force = np.array(d1["Force"])
        displacement = np.array(d1.index)

        # calculate the derivative
        diff = np.diff(force)/np.diff(displacement)

        diff = DataFrame(diff, index=d1.index[1:])

        # f0 is the first critical point of the curve

        maxx, maxy = CriticalPOint(d1, 0.0075, 0.015)

        # take the mean = mean of the first 10 values of diff

        # first index where the difference is bigger than 500
        start0 = d1[d1["Force"] > 0.5].index[0]
        # what numebr is start in the index
        start = d1.index.get_loc(start0)

        # first id where force is max
        end0 = d1[d1["Force"] == d1["Force"].max()].index[0]
        # F0 is the number of the index where force maxy

        # what numebr is end in the index
        end = d1.index.get_loc(end0)
        plt.plot(d1*1000, label="d1")
        plt.plot(diff, label="diff")
        plt.plot(maxx, maxy*1000, 'o', color="C8")

        # put a vertical bar at force
        plt.axvline(x=start0, color="black", linestyle="--")
        plt.axvline(x=end0, color="black", linestyle="--")

        print("start", start)
        print("end", end)

        diff = diff.dropna()
        # new index from start to maxx
        mean = diff.loc[start:end]
        print("mean", mean)
        # print("integral", np.trapz(
        #    diff[new_index], new_index))

        plt.legend()

    def clean(self, **kwargs):
        """Remove all rows with NaN"""
        # take only the first half of the data wrt the indexx

        # self.data = self.data[:int(len(self.data)*0.7)]
        # self.data = self.data.astype(float)
        # self.data = self.data[self.data["Displacement"] > 0]
        # self.data = self.data[self.data["Displacement"] < 85]
        # self.data = self.data.dropna()
        # self.data = self.data.groupby(by='Displacement').mean()
        # self.data = shift(self.data,  **kwargs)
        pass  # elf.data = smooth(self.data, **kwargs)

    def plot(self, **kwargs):
        """Plot the data"""
        plt.plot(self.data, label=self.filename, **kwargs)


def shift(df, **kwargs):
    """Shift the data to the right"""
    N = df.where(df > 200).first_valid_index()
    index = np.array(df.index)
    index = index + 10 - N
    df.index = index

    return df


def smooth(df, **kwargs):
    # take the min in index and max in index
    min_index = df.index.min()
    max_index = df.index.max()
    # create a new index
    new_index = np.arange(round(min_index, 1), round(max_index, 1), 0.1)
    # create a new dataframe
    new_df = DataFrame(index=new_index)
    # interpolate the data
    new_df = new_df.interpolate(method='linear', axis=0)
    # merge the dataframes
    new_df = new_df.merge(df, left_index=True, right_index=True, how='outer')
    # interpolate the data
    new_df = new_df.interpolate(method='linear', axis=0)
    return new_df


def PlotterSingle(namedir, N, **kwargs):

    measurments = []
    exp = DataFrame()
    plt.figure(figsize=(10, 5))
    for filename in listdir(namedir):
        measurments.append(Measurment(namedir+"/"+filename))
        measurments[-1].clean(**kwargs)
        # measurments[-1].plot()

    # check the min-max index in the dataframes
    t_min = max([i.data.index.min() for i in measurments])
    t_max = min([i.data.index.max() for i in measurments])
    # print(round(t_min, 1), print(t_max, 1))
    # add to exp dataframe the index that goes from tmin to tmax with increments of 0.1
    exp = DataFrame(index=np.arange(round(t_min, 1), round(t_max, 1), 0.1))
    for m in measurments:
        exp = concat([exp, m.data], axis=1)

    # if only nans in a row, drop it
    exp = smooth(exp)
    # sprint(exp)
    # fill with mean nans
    # exp = exp.fillna(exp.mean(axis=1))
#
    #
    # exp.plot( color = "C0",legend=False, style=".",
    # linewidth=0.4, figsize=(7, 4), alpha=0.1)
    #
    mean = exp.mean(axis=1)
    # calculate the integral of the mean
    integral = np.trapz(mean, mean.index)
    print("integral", integral)

    # for i in mean : print(i)
    mean.plot(color="black", legend=False, linewidth=1.5,
              figsize=(7, 4), label="mean")
    # display(mean)
    plt.grid()
    std = exp.std(axis=1)
    plt.fill_between(mean.index, mean-std, mean+std,
                     color="C0", alpha=0.5, label="std")
    plt.xlabel("Time [s]")
    plt.ylabel("Force [N]")
    plt.xlim(0, 40)
    plt.ylim(-150, 550)
    plt.title("TPA vegan Lyoner sausage - oleogel RBX/RSO "+str(N)+"% (-20 C)")
    plt.tight_layout()

    PlotPoints(mean, std)
#
    plt.legend()
    if kwargs.get("save_plots", True):
        plt.savefig(namedir+".png", dpi=2000)

    # save the data as a csv file
    exp.to_csv(str(N)+"test.csv", sep=';')


def PlotterMultiple(namedir, displacement,  **kwargs):
    # use single plotter to plot multiple plots
    plt.figure(figsize=(7, 4))
    for N in [2, 4, 6, 8]:
        namedir = str(N)+"perc/csv"
        PlotterSingle(namedir, N, **kwargs)


def PlotterDeriv(namedir, N, **kwargs):

    measurments = []
    exp = DataFrame()
    plt.figure(figsize=(10, 5))
    for filename in listdir(namedir):
        measurments.append(Measurment(namedir+"/"+filename))
        measurments[-1].clean(**kwargs)


p = 0.9
lam = 10**12
niter = 10
kwargs = {"p": p, "lam": lam, "niter": niter}

SHOW_PLOTS = False

N = 2
namedir = str(N)+"perc/.csv"
namedir = "TPA/SAUSAGES/RSO_FREEZ/6perc/csv"
# PlotterSingle(namedir, N, **kwargs)
plt.show()

PlotterDeriv(namedir, N, **kwargs)
plt.show()


2.65*10**(4)
