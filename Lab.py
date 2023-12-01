"""Tool to plot infer some analysis on experiments"""
from dataclasses import dataclass, field
from os import listdir
import matplotlib.pyplot as plt
from pandas import DataFrame, read_csv, concat
import mplcyberpunk
from sklearn.linear_model import LinearRegression
import numpy as np


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

        df = self.data.groupby(self.data.columns[0]).mean()
        df.index = df.index.values
        df.columns = [self.id_exp]
        return df


@dataclass
class Experiments:
    """Experiment class with name and list of experiments"""

    # name: str = field(default_factory=str)
    list_exps: list = field(default_factory=list, repr=False)
    groupped_data: DataFrame = field(init=True, default_factory=DataFrame, repr=False)

    def __post_init__(self):
        self.group_data()

    def group_data(self, *args, **kwargs):
        """Group the data"""
        for exp in self.list_exps:
            # print("Processing: ", exp.id_exp)
            self.groupped_data = concat([self.groupped_data, exp.process_data], axis=1)

    @property
    def display(self, *args, **kwargs):
        """Display the data"""
        print(self.groupped_data)

    @property
    def clean(self, *args, **kwargs):
        """Clean the data using the CleanData function"""
        self.groupped_data = clean_data(self.groupped_data, *args, **kwargs)

    @property
    def plot(self, *args, **kwargs):
        """Plot the data"""

        plot_data(self.groupped_data, *args, **kwargs)

    def filter(self, words: list):
        """Filter the data using the words in the list and returns a dataframe with the filtered data"""
        df = DataFrame(self.groupped_data)
        for word in words:
            df = df.filter(regex=word)
        return df

    @property
    def flat_out(self):
        """Flatten the data"""
        self.groupped_data = baseline_correction(self.groupped_data, degree=1)


def baseline_correction(df, degree=1):
    # Assume df is your DataFrame with temperature as the index
    # and columns representing different measurements

    corrected_df = df.copy()

    for column in df.columns:
        # Extract temperature and measurement values
        temperature = df.index.values.reshape(-1, 1)
        measurement = df[column].values

        # Fit a polynomial of degree 'degree' to the baseline
        model = LinearRegression()
        model.fit(temperature, measurement)

        # Subtract the baseline from the original measurement
        baseline = model.predict(temperature)
        corrected_measurement = measurement - baseline

        # Update the DataFrame with the corrected measurement
        corrected_df[column] = corrected_measurement

    return corrected_df


def clean_data(df: DataFrame, **kwargs):
    df = df.dropna(axis=0, how="any")
    return df


CYBERPUNK = True


def plot_data(df: DataFrame, *args, **kwargs):
    # if make it cyberpunk is in kwargs use it otherwise use the default

    # use the global variable CYBERPUNK to decide if make it cyberpunk or not

    if CYBERPUNK:
        plt.style.use("cyberpunk")

    # take the mean and the standard deviation of the data
    mean = df.mean(axis=1)
    std = df.std(axis=1)

    # figure must be contained in the range_T and range_Q
    # range_T = (df.index.min(), df.index.max())
    # range_Q = (df.values.min(), df.values.max())
    #
    ## set the range of the plot
    # plt.xlim(range_T)
    # plt.ylim(range_Q)

    # plot the mean and the standard deviation
    startin_point = kwargs.get("starting_point", 0)
    plt.plot(mean + startin_point, linewidth=1)

    plt.fill_between(
        mean.index, startin_point + mean - std, startin_point + mean + std, alpha=0.2
    )

    # plot the data with a very thin line and same color as above plot
    for column in df.columns:
        plt.plot(df[column] + startin_point, linewidth=0.4, label=column)

    # add the legend
    plt.legend()
    # add the labels
    plt.xlabel("Temperature")
    plt.ylabel("Heat Flow")
    plt.title("Heating vs Temperature")

    # add the cyberpunk style
    # mplcyberpunk.add_glow_effects()

    # show the plot


# dataA = all.filter(regex="heating").filter(regex="2perc").filter(regex="A")
# dataB = all.filter(regex="heating").filter(regex="2perc").filter(regex="B")
## plot A and B with a very thin line and same color of the corresponding plot
# plt.plot(dataA, color="C0", linewidth=0.1)
# plt.plot(dataB, color="C0", linewidth=0.1)


def collect_files(location: str, extension: str):
    """Collect all the files in a directory"""
    files = listdir(location)
    return [file for file in files if file.endswith(extension)]


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
