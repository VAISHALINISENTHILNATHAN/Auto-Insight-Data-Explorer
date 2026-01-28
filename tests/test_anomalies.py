from core.config import AppConfig
from core.loader import DataLoader
from core.anomalies import AnomalyEngine

def main():
    config=AppConfig()
    loader=DataLoader(config)

    df=loader.load_csv("data/sample.csv")
    
    engine=AnomalyEngine(df,config)
    anomalies=engine.detect()

    print("\nDETECTED ANOMALIES\n")

    if not anomalies:
        print("No anomalies detected.")
    else:
        for a in anomalies:
            print(f"Row index: {a.index}")
            print(f"Score: {a.score}")
            print(f"Reason: {a.reason}\n")

if __name__=="__main__":
    main()