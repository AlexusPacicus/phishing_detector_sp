import pandas as pd
from features_v3 import extract_features_v3, FEATURES_V3
from features.loaders_v3 import initialize_v3

def extract_features_dataset_v3(input_csv, output_csv):
    whitelist, constants = initialize_v3()
    df = pd.read_csv(input_csv)
    feats = df["url"].apply(lambda url: extract_features_v3(url, whitelist, constants))
    feats_df = pd.DataFrame(feats.tolist(), columns=FEATURES_V3)
    df = pd.concat([df, feats_df], axis=1)
    df.to_csv(output_csv, index=False)
  