from core.loader import DataLoader
from core.config import AppConfig
from core.visualization import VisualizationEngine

def main():
    loader=DataLoader(AppConfig())
    df=loader.load_csv("data/sample.csv")

    viz=VisualizationEngine(df)
    viz.numeric_histograms()
    viz.categorical_counts()

if __name__=="__main__":
    main()