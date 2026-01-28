from core.config import AppConfig
from core.loader import DataLoader

def main():
    config=AppConfig()
    loader=DataLoader(config)

    df=loader.load_csv("data/sample.csv")
    print("Loaded shape:",df.shape)

    print("\nPreview:")
    print(loader.preview(df))

if __name__=="__main__":
    main()