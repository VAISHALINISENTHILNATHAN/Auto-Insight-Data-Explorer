from dataclasses import dataclass
from typing import List
import numpy as np

@dataclass
class Insight:
    title:str
    description:str
    severity:str
    evidence:str

class InsightEngine:
    def __init__(self,eda_engine):
        self.eda=eda_engine
    
    def generate(self)->List[Insight]:
        insights=[]
        profiles=self.eda.profile_columns()
        summary=self.eda.dataset_summary()

        insights.extend(self._missing_value_insights(profiles))
        insights.extend(self._high_variance_insights(profiles))
        insights.extend(self._dataset_level_insights(summary))

        return insights
    
    def _missing_value_insights(self,profiles):
        insights=[]
        for col,profile in profiles.items():
            if profile.missing_pct>20:
                insights.append(
                    Insight(
                        title=f"High missing values in '{col}'",
                        description=f"{profile.missing_pct}% of values are missing.",
                        severity="HIGH",
                        evidence=f"Missing count: {profile.missing_count}"
                    )
                )
        return insights
    
    def _high_variance_insights(self,profiles):
        insights=[]
        for col,profile in profiles.items():
            if hasattr(profile, "std") and profile.mean!=0:
                cv=profile.std/profile.mean
                if cv>0.8:
                    insights.append(
                        Insight(
                            title=f"High variability in '{col}'",
                            description="Values show high dispersion relative to the mean.",
                            severity="MEDIUM",
                            evidence=f"Std: {round(profile.std,2)}, Mean: {round(profile.mean,2)}"
                        )
                    )
        return insights
    
    def _dataset_level_insights(self,summary):
        insights=[]
        if summary["rows"]<50:
            insights.append(
                Insight(
                    title="Small dataset detected",
                    description="Dataset has fewer than 50 rows; statistical conclusions may be unreliable.",
                    severity="LOW",
                    evidence=f"Row count: {summary['rows']}"
                )
            )
        return insights