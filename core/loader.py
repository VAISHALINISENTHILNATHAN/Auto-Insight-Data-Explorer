import pandas as pd
from core.config import AppConfig

class DataLoader:
    def __init__(self,config:AppConfig):
        self.config=config
    
    def load_csv(self,path:str)->pd.DataFrame:
        try:
            df=pd.read_csv(path,encoding=self.config.csv_encoding)
        except Exception as e:
            raise ValueError(f"Failed to load CSV file: {e}")
        
        if df.empty:
            raise ValueError("CSV file is empty!")
        
        return df
    
    def preview(self,df:pd.DataFrame)->pd.DataFrame:
        return df.head(self.config.max_rows_preview)