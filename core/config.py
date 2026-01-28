from dataclasses import dataclass
@dataclass(frozen=True)
class AppConfig:
    max_rows_preview:int=10
    min_numeric_cols:int=1
    csv_encoding:str="utf-8"
    anomaly_contamination:float=0.05
    zscore_threshold:float=3.0
    