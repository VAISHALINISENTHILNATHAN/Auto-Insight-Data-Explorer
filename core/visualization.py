import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List

class VisualizationEngine:
    def __init__(self,df:pd.DataFrame):
        self.df=df
        sns.set(style="whitegrid")

    def numeric_histograms(self,columns:List[str]=None):
        cols=columns or self.df.select_dtypes(include='number').columns
        for col in cols:
            plt.figure(figsize=(6,4))
            sns.histplot(self.df[col],kde=True)
            plt.title(f'Histogram of {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.tight_layout()
            plt.show()
    
    def categorical_counts(self,columns:List[str]=None):
        cols = columns or self.df.select_dtypes(exclude='number').columns
        for col in cols:
            plt.figure(figsize=(6,4))
            sns.countplot(x=self.df[col])
            plt.title(f'Counts of {col}')
            plt.xlabel(col)
            plt.ylabel('Count')
            plt.tight_layout()
            plt.show()
    