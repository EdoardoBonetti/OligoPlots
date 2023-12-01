"""Tool to plot infer some analysis on experiments"""
from dataclasses import dataclass, field
from os import listdir
import matplotlib.pyplot as plt
from pandas import DataFrame, read_csv, concat
import mplcyberpunk
from sklearn.linear_model import LinearRegression
import numpy as np


# @dataclass
# class Material:
#    """Material class with name"""
#
#    name: str = ""


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


def plot_data(df: DataFrame, *args, **kwargs):
    mean = df.mean(axis=1)
    std = df.std(axis=1)
    startin_point = kwargs.get("starting_point", 0)
    plt.plot(mean + startin_point, linewidth=1)

    plt.fill_between(
        mean.index, startin_point + mean - std, startin_point + mean + std, alpha=0.2
    )
    for column in df.columns:
        plt.plot(df[column] + startin_point, linewidth=0.4, label=column)

    plt.legend()
    plt.xlabel("Temperature")
    plt.ylabel("Heat Flow")
    plt.title("Heating vs Temperature")


def collect_files(location: str, extension: str):
    """Collect all the files in a directory"""
    files = listdir(location)
    return [file for file in files if file.endswith(extension)]
