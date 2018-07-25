import pandas as pd


class DF:

    def __init__(self, cleaned_data):
        self.df = pd.DataFrame(cleaned_data, columns=list(cleaned_data.keys()))
        self.df = self.df.set_index('Time Stamp')

    def __getitem__(self, column):
        return self.df[column]

    def get_latest(self, n):
        return self.df.tail(n)

    def to_string(self):
        return self.df.to_string()
