import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from dataclasses import dataclass
from typing import List
from core.config import AppConfig

@dataclass
class Anomaly:
    index:int
    score:float
    reason:str

class AnomalyEngine:
    def __init__(self,df:pd.DataFrame,config:AppConfig):
        self.df=df
        self.config=config
        self.numeric_df=df.select_dtypes(include=[np.number])

    def detect(self)->List[Anomaly]:
        anomalies=[]
        if self.numeric_df.shape[1]==0:
            return anomalies
        
        scaled=(self.numeric_df-self.numeric_df.mean())/self.numeric_df.std()

        z_scores=np.abs(scaled)
        z_mask=(z_scores>self.config.zscore_threshold).any(axis=1)

        model=IsolationForest(
            contamination=self.config.anomaly_contamination,
            random_state=42
        )
        iso_pred=model.fit_predict(self.numeric_df)
        iso_mask=iso_pred==-1

        combined_mask=z_mask|iso_mask

        for idx in self.numeric_df.index[combined_mask]:
            score=float(model.decision_function([self.numeric_df.loc[idx]])[0])
            anomalies.append(
                Anomaly(
                    index=int(idx),
                    score=round(score,4),
                    reason="IsolationForest and/or Z-score trigger"
                )
            )
        return anomalies