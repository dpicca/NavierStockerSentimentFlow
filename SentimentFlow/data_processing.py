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


def parse_xml_to_dataframe(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extracting play title
    play_title = root.find('TITLE').text

    # Extracting speaker and speech
    data = []
    for speech in root.iter('SPEECH'):
        speaker = speech.find('SPEAKER').text
        lines = [line.text for line in speech.findall('LINE') if line.text]
        speech_text = ' '.join(lines)
        data.append({'title': play_title, 'speaker': speaker, 'speech': speech_text})

    # Creating DataFrame
    df = pd.DataFrame(data, columns=['title', 'speaker', 'speech'])
    return df


def process_speeches(input_df, senticnet_path):
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
