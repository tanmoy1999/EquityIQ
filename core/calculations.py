
class Col:
    def __init__(self, df, colName, col1, col2):
        self.df = df
        self.colName = colName
        self.col1 = col1
        self.col2 = col2

    def perc_diff(self):
        self.df[self.colName] = ((self.df[self.col2] - self.df[self.col1])/self.df[self.col1]) * 100
        return self.df
        