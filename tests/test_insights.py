from core.config import AppConfig
from core.loader import DataLoader
from core.eda import EDAEngine
from core.insights import InsightEngine

def main():
    loader=DataLoader(AppConfig())
    df=loader.load_csv("data/sample.csv")
    
    eda=EDAEngine(df)
    insight_engine=InsightEngine(eda)

    insights=insight_engine.generate()

    print("\nGENERATE INSIGHTS\n")
    for i,ins in enumerate(insights,1):
        print(f"{i}. [{ins.severity}] {ins.title}")
        print(f"  {ins.description}")
        print(f"  Evidence: {ins.evidence}\n")

if __name__=="__main__":
    main()