import pandas as pd
import numpy as np

class DataExpander:
    def __init__(self):
        self.datasets = {
            "Mon": "../data/Monday-WorkingHours.pcap_ISCX.csv",
            "Tue": "../data/Tuesday-WorkingHours.pcap_ISCX.csv",
            "Wed": "../data/Wednesday-workingHours.pcap_ISCX.csv",
            "Thu_1": "../data/Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv",
            "Thu_2": "../data/Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
            "Fri_1": "../data/Friday-WorkingHours-Morning.pcap_ISCX.csv",
            "Fri_2": "../data/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
            "Fri_3": "../data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
        }

    def clean_labels(self, df: pd.DataFrame, label_col="Label") -> pd.DataFrame:
        df[label_col] = df[label_col].str.replace(r'[^\w\s-]', '-', regex=True)
        df[label_col] = df[label_col].str.replace(r'Web Attack -', 'Web Attack -', regex=False)
        return df

    def load_dataset(self, day, encoding="latin1"):
        df = pd.read_csv(self.datasets[day], encoding=encoding)
        df.columns = df.columns.str.strip()
        df = df.dropna(how="any")
        df = self.clean_labels(df)
        return df

    def expand(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Added features only if they do not exist:
        - Bytes per Packet: Total bytes / Total packets
        - SYN Ratio: SYN Flag Count / Total Flags
        - RST Ratio: RST Flag Count / Total Flags
        - FIN Ratio: FIN Flag Count / Total Flags
        - Duration Log: Log-transformed Flow Duration
        """
        if 'Bytes per Packet' not in df.columns:
            total_len = df['Total Length of Fwd Packets'] + df['Total Length of Bwd Packets']
            total_pkts = (df['Total Fwd Packets'] + df['Total Backward Packets']).replace(0, np.nan)
            df['Bytes per Packet'] = (total_len / total_pkts).fillna(0)

        flag_total = (
            df['SYN Flag Count'] +
            df['ACK Flag Count'] +
            df['RST Flag Count'] +
            df['FIN Flag Count']
        ).replace(0, np.nan)

        if 'SYN Ratio' not in df.columns:
            df['SYN Ratio'] = (df['SYN Flag Count'] / flag_total).fillna(0)
        if 'RST Ratio' not in df.columns:
            df['RST Ratio'] = (df['RST Flag Count'] / flag_total).fillna(0)
        if 'FIN Ratio' not in df.columns:
            df['FIN Ratio'] = (df['FIN Flag Count'] / flag_total).fillna(0)

        if 'Duration Log' not in df.columns:
            duration = df['Flow Duration'].copy()
            duration[duration < 0] = 0
            duration = duration.fillna(0)
            df['Duration Log'] = np.log1p(duration)

        return df

    def save_expanded(self, df: pd.DataFrame, out_path: str):
        df.to_csv(out_path, index=False)
        print(f"Saved expanded dataset to {out_path}")


if __name__ == "__main__":
    expander = DataExpander()
    for day, path in expander.datasets.items():
        df = expander.load_dataset(day)
        df_expanded = expander.expand(df)
        out_path = f"../data/{day}-Expanded.csv"
        expander.save_expanded(df_expanded, out_path)

    thu_parts = ['Thu_1', 'Thu_2']
    thu_dfs = [expander.expand(expander.load_dataset(day)) for day in thu_parts]
    thu_full = pd.concat(thu_dfs, ignore_index=True)
    expander.save_expanded(thu_full, "../data/Thu-Expanded.csv")

    fri_parts = ['Fri_1', 'Fri_2', 'Fri_3']
    fri_dfs = [expander.expand(expander.load_dataset(day)) for day in fri_parts]
    fri_full = pd.concat(fri_dfs, ignore_index=True)
    expander.save_expanded(fri_full, "../data/Fri-Expanded.csv")

    # Comine all days into a full dataset
    all_days = ['Mon', 'Tue', 'Wed'] + thu_parts + fri_parts
    all_dfs = [expander.expand(expander.load_dataset(day)) for day in all_days]
    full_dataset = pd.concat(all_dfs, ignore_index=True)
    expander.save_expanded(full_dataset, "../data/Full-Expanded.csv")
