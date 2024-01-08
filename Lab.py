"""Tool to plot infer some analysis on DSC thermograms and TPA"""

from dataclasses import dataclass, field
from pandas import DataFrame, read_csv, concat
from os import listdir
from icecream import ic
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression


def collect_files(location: str, extension: str):
    """Collect all the files in a directory"""
    filenames = listdir(location)
    return [file for file in filenames if file.endswith(extension)]


def read_data(id_exp: str, location: str):
    """Read the data from the file"""
    return read_csv(
        location + "/" + id_exp, sep="\t", header=0, skiprows=0,
        # names=["Temperature", "Heat Flow"]
        names=["Temperature", id_exp]
    )


def baseline_correction(df):
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


def smooth(df, window):
    return df.rolling(window=window, center=True).mean()


@dataclass
class Measurment:
    """Measurment class with id, location and data"""

    id_exp: str = ""
    location: str = field(repr=True, default_factory=str)
    data: DataFrame = field(repr=True, init=False, default_factory=DataFrame)

    def __post_init__(self):
        self.data = read_data(self.id_exp, self.location)
        self.clean_data

    @property
    def clean_data(self):
        """Clean the data"""
        t_min = 25
        t_max = 85
        self.data = self.data[self.data["Temperature"] >= t_min]
        self.data = self.data[self.data["Temperature"] <= t_max]
        self.data = self.data.dropna()
        self.data = self.data.groupby(self.data.columns[0])
        self.data = self.data.mean()
        self.data.columns = [self.id_exp]
        self.data = baseline_correction(self.data)
        # self.data = smooth(self.data, 4)


def Experiment(location: str, title: str):
    # location = "DSC/4perc/cooling"

    list_ids = collect_files(location, extension=".txt")
    measm = [Measurment(i, location) for i in list_ids]

    df = DataFrame()
    for m in measm:
        df = concat([df, m.data], axis=1)
        # plt.plot(m.data, color="black", linewidth=0.1)
        # print(m.data)

    # plt.show()
    print(df)
    # eliminate nans
    df = df.dropna()
    # df.plot(color="black", linewidth=0.1)
    mean = df.mean(axis=1)
    plt.plot(mean, color="red", linewidth=1)
    std = df.std(axis=1)
    # plt.plot(mean + std, color="blue", linewidth=1)
    # plt.plot(mean - std, color="blue", linewidth=1)
    plt.fill_between(mean.index, mean + std, mean -
                     std, color="blue", alpha=0.2)
    plt.legend(["mean", "std"])
    title.replace("\",  )
    plt.title(title)
    # plt.show()
    # save plot in same location
    title.replace(" ", "_").replace("%", "perc")
    plt.grid()
    plt.savefig(location + "/" + title+".png", dpi=300)
    plt.close()


def main():
    """Main function"""
    Experiment("DSC/2perc/cooling",
               "DSC thermogram oleogel RBX\RSO cooling 2%")
    Experiment("DSC/2perc/heating",
               "DSC thermogram oleogel RBX\RSO heating 2%")
    Experiment("DSC/4perc/cooling",
               "DSC thermogram oleogel RBX\RSO cooling 4%")
    Experiment("DSC/4perc/heating",
               "DSC thermogram oleogel RBX\RSO heating 4%")
    Experiment("DSC/6perc/cooling",
               "DSC thermogram oleogel RBX\RSO cooling 6%")
    Experiment("DSC/6perc/heating",
               "DSC thermogram oleogel RBX\RSO heating 6%")
    Experiment("DSC/8perc/cooling",
               "DSC thermogram oleogel RBX\RSO cooling 8%")
    Experiment("DSC/8perc/heating",
               "DSC thermogram oleogel RBX\RSO heating 8%")


if __name__ == "__main__":
    main()
