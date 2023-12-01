"""Tool to plot infer some analysis on experiments"""

from dataclasses import dataclass, field
from os import listdir
import matplotlib.pyplot as plt
from pandas import DataFrame, read_csv, concat
import mplcyberpunk


@dataclass
class Material:
    """Material class with name"""

    name: str = ""


@dataclass
class SingleExperiment:
    id_exp: str = ""
    location: str = field(repr=False, default_factory=str)
    data: DataFrame = field(repr=False, init=False, default_factory=DataFrame)

    def __post_init__(self):
        self.data = self.ReadData()

    def ReadData(self, *args, **kwargs):
        """Read the data from the file"""
        if self.id_exp.endswith(".txt"):
            return read_csv(
                self.location + "/" + self.id_exp, sep="\t", header=0, skiprows=2
            )
        elif self.id_exp.endswith(".csv"):
            return read_csv(
                self.location + "/" + self.id_exp, sep=",", header=0, skiprows=2
            )
        else:
            raise ValueError("File not supported")

    @property
    def display(self):
        """Display the data"""
        print(self.data)

    def AddToPlot(self, *args, **kwargs):
        """Add the data to the plot"""
        pass

    @property
    def process_data(self):
        """Process the data"""
        # group by first column
        df = self.data.groupby(self.data.columns[0]).mean()
        df.index = df.index.values
        # rename the columns with id_exp
        df.columns = [self.id_exp]
        return df


@dataclass
class Experiments:
    """Experiment class with name and list of experiments"""

    name: str = field(default_factory=str)
    # heating must be a bool set to True  and not shown in the repr
    list_exps: list = field(default_factory=list, repr=False)
    heating: bool = field(default=True, repr=False)
    groupped_data: DataFrame = field(init=True, default_factory=DataFrame, repr=False)

    def __post_init__(self):
        self.group_data()

    def group_data(self, *args, **kwargs):
        """Group the data"""
        for exp in self.list_exps:
            print("added")
            self.groupped_data = concat([self.groupped_data, exp.process_data], axis=1)

    @property
    def display(self, *args, **kwargs):
        """Display the data"""
        print(self.groupped_data)

    @property
    def clean_data(self, *args, **kwargs):
        """Clean the data using the CleanData function"""
        self.groupped_data = CleanData(self.groupped_data, *args, **kwargs)

    def plot(self, *args, **kwargs):
        """Plot the data"""
        pass


def CleanData(df: DataFrame, **kwargs):
    # drop the rows with NaN values
    df = df.dropna(axis=0, how="any")

    # if in args and kwargs there is a range_T and range_Q use them otherwise use the default
    # if "range_T" in kwargs:
    #    range_T = kwargs["range_T"]
    # else:
    #    range_T = (df.index.min(), df.index.max())
    # if "range_Q" in kwargs:
    #    range_Q = kwargs["range_Q"]
    # else:
    #    range_Q = (df.values.min(), df.values.max())

    ## drop the rows with temperature out of the range
    # df = df.loc[(df.index >= range_T[0]) & (df.index <= range_T[1])]
    ## drop the columns with heat flow out of the range
    # df = df.loc[:, (df.values >= range_Q[0]) & (df.values <= range_Q[1])]
    return df


#
# maxs_T = []
# mins_T = []
## find the max and min temperature for every dataframe
# for key in df_dict.keys():
#    maxs_T.append(df_dict[key].index.max())
#    mins_T.append(df_dict[key].index.min())
#
# print(maxs_T)
# print(mins_T)
#
# range_T = (max(mins_T), min(maxs_T))
## for all the dataframes in the dictionary delete the rows with temperature out of the range
# df_dict2 = {}
# for key in df_dict.keys():
#    df_dict2[key] = df_dict[key].loc[
#        (df_dict[key].index >= range_T[0]) & (df_dict[key].index <= range_T[1])
#    ]
#
## now create a dataframe all that contains all the dataframes in the dictionary
# all = DataFrame()
# for key in df_dict2.keys():
#    all = concat([all, df_dict2[key]], axis=1)
#
#
## erase the rows with NaN values
# all = all.dropna(axis=0, how="any")
#
#
## plot the data
#
## set dpi
# plt.style.use("cyberpunk")
#
#
# plt.rcParams["figure.dpi"] = 100
#
## create a seaborn plot the mean and the standard deviation of the data that contain in the name "heating" and "2perc"
# mean = all.filter(regex="heating").filter(regex="2perc").mean(axis=1)
# std = all.filter(regex="heating").filter(regex="2perc").std(axis=1)
# plt.plot(mean, label="2%")
# plt.fill_between(mean.index, mean - std, mean + std, alpha=0.2)
# dataA = all.filter(regex="heating").filter(regex="2perc").filter(regex="A")
# dataB = all.filter(regex="heating").filter(regex="2perc").filter(regex="B")
## plot A and B with a very thin line and same color of the corresponding plot
# plt.plot(dataA, color="C0", linewidth=0.1)
# plt.plot(dataB, color="C0", linewidth=0.1)
#
#
## create a seaborn plot the mean and the standard deviation of the data that contain in the name "heating" and "4perc"
# mean = all.filter(regex="heating").filter(regex="4perc").mean(axis=1)
# std = all.filter(regex="heating").filter(regex="4perc").std(axis=1)
# plt.plot(mean, label="4%")
# plt.fill_between(mean.index, mean - std, mean + std, alpha=0.2)
# dataA = all.filter(regex="heating").filter(regex="4perc").filter(regex="A")
# dataB = all.filter(regex="heating").filter(regex="4perc").filter(regex="B")
## plot A and B with a very thin line and same color of the corresponding plot
# plt.plot(dataA, color="C1", linewidth=0.1)
# plt.plot(dataB, color="C1", linewidth=0.1)
#
#
## create a seaborn plot the mean and the standard deviation of the data that contain in the name "heating" and "4perc"
# mean = all.filter(regex="heating").filter(regex="6perc").mean(axis=1)
# std = all.filter(regex="heating").filter(regex="6perc").std(axis=1)
# plt.plot(mean, label="6%")
# plt.fill_between(mean.index, mean - std, mean + std, alpha=0.2)
# dataA = all.filter(regex="heating").filter(regex="6perc").filter(regex="A")
# dataB = all.filter(regex="heating").filter(regex="6perc").filter(regex="B")
## plot A and B with a very thin line and same color of the corresponding plot
# plt.plot(dataA, color="C2", linewidth=0.1)
# plt.plot(dataB, color="C2", linewidth=0.1)
#
#
## create a seaborn plot the mean and the standard deviation of the data that contain in the name "heating" and "8perc"
# mean = all.filter(regex="heating").filter(regex="8perc").mean(axis=1)
# std = all.filter(regex="heating").filter(regex="8perc").std(axis=1)
# plt.plot(mean, label="8%")
# plt.fill_between(mean.index, mean - std, mean + std, alpha=0.2)
# dataA = all.filter(regex="heating").filter(regex="8perc").filter(regex="A")
# dataB = all.filter(regex="heating").filter(regex="8perc").filter(regex="B")
## plot A and B with a very thin line and same color of the corresponding plot
# plt.plot(dataA, color="C3", linewidth=0.1)
# plt.plot(dataB, color="C3", linewidth=0.1)
#
#
# plt.legend()
# plt.xlabel("Temperature")
# plt.ylabel("Heat Flow")
# plt.title("Heating vs Temperature")
#
# mplcyberpunk.add_glow_effects()
## mplcyberpunk.make_lines_glow()
## mplcyberpunk.add_underglow()
#
# plt.show()
#
#
## same as above but for the cooling
# mean = all.filter(regex="cooling").filter(regex="2perc").mean(axis=1)
# std = all.filter(regex="cooling").filter(regex="2perc").std(axis=1)
# plt.plot(mean, label="2%")
# plt.fill_between(mean.index, mean - std, mean + std, alpha=0.2)
# dataA = all.filter(regex="cooling").filter(regex="2perc").filter(regex="A")
# dataB = all.filter(regex="cooling").filter(regex="2perc").filter(regex="B")
# plt.plot(dataA, color="C0", linewidth=0.1)
# plt.plot(dataB, color="C0", linewidth=0.1)
#
# mean = all.filter(regex="cooling").filter(regex="4perc").mean(axis=1)
# std = all.filter(regex="cooling").filter(regex="4perc").std(axis=1)
# plt.plot(mean, label="4%")
# plt.fill_between(mean.index, mean - std, mean + std, alpha=0.2)
# dataA = all.filter(regex="cooling").filter(regex="4perc").filter(regex="A")
# dataB = all.filter(regex="cooling").filter(regex="4perc").filter(regex="B")
# plt.plot(dataA, color="C1", linewidth=0.1)
# plt.plot(dataB, color="C1", linewidth=0.1)
#
#
# mean = all.filter(regex="cooling").filter(regex="6perc").mean(axis=1)
# std = all.filter(regex="cooling").filter(regex="6perc").std(axis=1)
# plt.plot(mean, label="6%")
# plt.fill_between(mean.index, mean - std, mean + std, alpha=0.2)
# dataA = all.filter(regex="cooling").filter(regex="6perc").filter(regex="A")
# dataB = all.filter(regex="cooling").filter(regex="6perc").filter(regex="B")
# plt.plot(dataA, color="C2", linewidth=0.1)
# plt.plot(dataB, color="C2", linewidth=0.1)
#
#
# mean = all.filter(regex="cooling").filter(regex="8perc").mean(axis=1)
# std = all.filter(regex="cooling").filter(regex="8perc").std(axis=1)
# plt.plot(mean, label="8%")
# plt.fill_between(mean.index, mean - std, mean + std, alpha=0.2)
# dataA = all.filter(regex="cooling").filter(regex="8perc").filter(regex="A")
# dataB = all.filter(regex="cooling").filter(regex="8perc").filter(regex="B")
# plt.plot(dataA, color="C3", linewidth=0.1)
# plt.plot(dataB, color="C3", linewidth=0.1)
#
#
# plt.legend()
# plt.xlabel("Temperature")
# plt.ylabel("Heat Flow")
# plt.title("Cooling vs Temperature")
# plt.show()
#
