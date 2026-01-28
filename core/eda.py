import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ColumnProfile:
    name:str
    dtype:str
    missing_count:int
    missing_pct:float
    unique_count:int
    sample_values:List

@dataclass
class NumericProfile(ColumnProfile):
    mean:float
    std:float
    min:float
    max:float
    median:float

class EDAEngine:
    def __init__(self,df:pd.DataFrame):
        self.df=df
        self.numeric_cols=df.select_dtypes(include=np.number).columns.tolist()
        self.categorical_cols=df.select_dtypes(exclude=np.number).columns.tolist()

    def dataset_summary(self)->Dict:
        return{
            "rows":self.df.shape[0],
            "columns":self.df.shape[1],
            "numeric_columns":self.numeric_cols,
            "categorical_columns":self.categorical_cols
        }
    
    def profile_columns(self)->Dict[str,ColumnProfile]:
        profiles={}

        for col in self.df.columns:
            series=self.df[col]
            missing_count=series.isnull().sum()
            missing_pct=missing_count/len(series)*100
            base_profile={
                "name":col,
                "dtype":str(series.dtype),
                "missing_count":missing_count,
                "missing_pct":round(missing_pct,2),
                "unique_count":series.nunique(),
                "sample_values":series.dropna().unique()[:5].tolist()
            }

            if col in self.numeric_cols:
                profiles[col]=NumericProfile(
                    **base_profile,
                    mean=series.mean(),
                    std=series.std(),
                    min=series.min(),
                    max=series.max(),
                    median=series.median()
                )
            else:
                profiles[col]=ColumnProfile(**base_profile)
        return profiles