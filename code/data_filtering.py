import pandas as pd
import numpy as np
import os

class DataSampler:
    def __init__(self, max_samples=1000):
        self.max_samples = max_samples
        self.datasets = {
            "Mon": "../data/Mon-Expanded.csv",
            "Tue": "../data/Tue-Expanded.csv",
            "Wed": "../data/Wed-Expanded.csv",
            "Thu": "../data/Thu-Expanded.csv",
            "Fri": "../data/Fri-Expanded.csv"
        }

    def _find_densest_region(self, indices: np.ndarray) -> np.ndarray:
        if len(indices) <= self.max_samples:
            return indices

        min_span = float('inf')
        best_start_index = 0

        for i in range(len(indices) - self.max_samples + 1):
            span = indices[i + self.max_samples - 1] - indices[i]
            if span < min_span:
                min_span = span
                best_start_index = i

        return indices[best_start_index : best_start_index + self.max_samples]

    def cherry_pick(self, df: pd.DataFrame) -> pd.DataFrame:
        sampled_dfs = []
        for label in df['Label'].unique():
            label_df = df[df['Label'] == label]
            if len(label_df) <= self.max_samples:
                sampled_dfs.append(label_df)
            else:
                original_indices = label_df.index.to_numpy()
                densest_indices_subset = self._find_densest_region(original_indices)
                sampled_dfs.append(df.loc[densest_indices_subset])
        if not sampled_dfs:
            return pd.DataFrame()
        result_df = pd.concat(sampled_dfs).sort_index()
        return result_df

    def load_dataset(self, day, encoding="latin1"):
        path = self.datasets[day]
        df = pd.read_csv(path, encoding=encoding)
        df.columns = df.columns.str.strip()
        df.dropna(subset=['Label'], inplace=True)
        # Remove benign samples for days other than Monday
        if day != "Mon":
            df = df[df['Label'] != 'BENIGN']
        return df

    def filter_and_combine(self):
        filtered_dfs = []
        for day in self.datasets:
            try:
                df = self.load_dataset(day)
                filtered_df = self.cherry_pick(df)
                filtered_dfs.append(filtered_df)
                print(f"Processed {day}-Expanded.csv")
            except Exception as e:
                print(f"Could not process {day}-Expanded.csv. Error: {e}")
        if filtered_dfs:
            combined_df = pd.concat(filtered_dfs, ignore_index=True)
            combined_df['Label'] = combined_df['Label'].str.strip()
            out_path = "../data/Combined-Filtered.csv"
            combined_df.to_csv(out_path, index=False)
            print(f"Successfully saved combined filtered data to {out_path}")
            print("\nFinal label distribution:")
            print(combined_df['Label'].value_counts())
        else:
            print("No data was filtered.")

if __name__ == "__main__":
    sampler = DataSampler(max_samples=1000)
    sampler.filter_and_combine()