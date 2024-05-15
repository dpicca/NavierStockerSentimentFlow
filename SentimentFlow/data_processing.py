import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path
from tqdm.notebook import tqdm
import logging
import spacy

# Load the English tokenizer, POS tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")





def process_speeches(input_df: pd.DataFrame, senticnet_path: str) -> pd.DataFrame:
    """
    Process the speeches in the input dataframe and extract the emotions and polarity using SenticNet.

    :param input_df: The input dataframe containing the speeches. Columns should include 'title', 'speaker', and 'speech'.
    :param senticnet_path: The path to the SenticNet data.
    :return: A dataframe containing the processed speeches.
    """
    senticnet_data = pd.read_csv(senticnet_path, delimiter="\t")
    categories = ['INTROSPECTION', 'TEMPER', 'ATTITUDE', 'SENSITIVITY']

    results = []
    for _, row in tqdm(input_df.iterrows(), total=input_df.shape[0]):
        speech_processed = row['speech_processed']
        speaker = row['speaker']
        speech = row['speech']
        title = row['title']

        accumulators = {}
        polaritylist = []
        for sent in speech_processed.sents:
            for token in sent:
                token_text = token.text.lower()
                matching_row = senticnet_data[senticnet_data['CONCEPT'] == token_text]
                if not matching_row.empty:
                    max_category = matching_row[categories].astype(float).idxmax(axis=1).iloc[0]
                    min_category = matching_row[categories].astype(float).idxmin(axis=1).iloc[0]

                    primary_emotion = matching_row['PRIMARY EMOTION'].iloc[0]
                    secondary_emotion = matching_row['SECONDAY EMOTION'].iloc[0]

                    if pd.isna(primary_emotion):
                        max_emotion = max_category
                    else:
                        max_emotion = f"{max_category}{matching_row['PRIMARY EMOTION'].iloc[0]}"

                    if pd.isna(secondary_emotion):
                        min_emotion = min_category
                    else:
                        min_emotion = f"{min_category}{matching_row['SECONDAY EMOTION'].iloc[0]}"

                    if max_emotion not in accumulators:
                        accumulators[max_emotion] = []
                    if min_emotion not in accumulators:
                        accumulators[min_emotion] = []

                    accumulators[max_emotion].append(matching_row[max_category].iloc[0])
                    if max_emotion != min_emotion:
                        accumulators[min_emotion].append(matching_row[min_category].iloc[0])

                    polarity = matching_row["POLARITY INTENSITY"].astype(float).iloc[0]
                    polaritylist.append(polarity)

        emotion_avg = {emotion: sum(values) / len(values) if values else 0 for emotion, values in accumulators.items()}
        polarity_avg = {"POLARITY": sum(polaritylist) / len(polaritylist) if polaritylist else 0}

        result_row = {'title': title, "speaker": speaker, "speech": speech, **emotion_avg, **polarity_avg}
        results.append(result_row)

    results = pd.DataFrame(results).fillna(0)
    results = results.loc[:, (results != 0).any(axis=0)]

    Path("results/speeches_processed.csv").parent.mkdir(parents=True, exist_ok=True)
    results.to_csv('results/speeches_processed.csv', index=False)
    return results
