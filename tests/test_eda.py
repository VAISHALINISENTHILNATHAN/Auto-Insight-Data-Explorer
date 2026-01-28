import pandas as pd
from core.config import AppConfig
from core.loader import DataLoader
from core.eda import EDAEngine

def main():
    loader=DataLoader(AppConfig())
    df=loader.load_csv("data/sample.csv")

    eda=EDAEngine(df)

    print("\nDATASET SUMMARY")
    print(eda.dataset_summary())

    print("\nCOLUMN PROFILES")
    profiles=eda.profile_columns()

    for col, profile in profiles.items():
        print(f"\nColumn: {col}")
        for k,v in profile.__dict__.items():
            print(f"  {k}: {v}")

if __name__=="__main__":
    main()