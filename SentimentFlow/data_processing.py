import pandas as pd
from pathlib import Path
from tqdm.auto import tqdm
import spacy
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# Load the English tokenizer, POS tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

class SpeechProcessor:
    def __init__(self, senticnet_path: str):
        """
        Initialize the SpeechProcessor.

        Args:
            senticnet_path (str): The path to the SenticNet data.
        """
        self.senticnet_path = senticnet_path
        self.senticnet_data = pd.read_csv(senticnet_path, delimiter="\t")
        self.categories = ['INTROSPECTION', 'TEMPER', 'ATTITUDE', 'SENSITIVITY']

    def process_speeches(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """
        Process the speeches in the input dataframe and extract the emotions and polarity using SenticNet.

        Args:
            input_df (pd.DataFrame): The input dataframe containing the speeches. Columns should include 'title', 'speaker', and 'speech'.

        Returns:
            pd.DataFrame: A dataframe containing the processed speeches.

        Example:
            >>> input_df = pd.DataFrame({'title': ['Title 1', 'Title 2'], 'speaker': ['Speaker 1', 'Speaker 2'], 'speech': ['I am happy', 'I am sad']})
            >>> processor = SpeechProcessor('data/SenticNet4.txt')
            >>> processor.process_speeches(input_df)
                 title    speaker       speech  JOY  POLARITY
            0  Title 1  Speaker 1  I am happy  0.0  0.500000
            1  Title 2  Speaker 2    I am sad  0.0 -0.333333
        """
        results = []
        logging.info("Starting to process")
        for _, row in tqdm(input_df.iterrows(), total=input_df.shape[0], desc="Processing speeches"):
            speech_processed = nlp(row['speech'])
            speaker = row['speaker']
            speech = row['speech']
            title = row['title']

            accumulators = {}
            polaritylist = []
            for sent in speech_processed.sents:
                for token in sent:
                    token_text = token.text.lower()
                    matching_row = self.senticnet_data[self.senticnet_data['CONCEPT'] == token_text]
                    if not matching_row.empty:
                        max_category = matching_row[self.categories].astype(float).idxmax(axis=1).iloc[0]
                        min_category = matching_row[self.categories].astype(float).idxmin(axis=1).iloc[0]

                        primary_emotion = matching_row['PRIMARY EMOTION'].iloc[0]
                        secondary_emotion = matching_row['SECONDARY EMOTION'].iloc[0]

                        if pd.isna(primary_emotion):
                            max_emotion = max_category
                        else:
                            max_emotion = f"{max_category}{matching_row['PRIMARY EMOTION'].iloc[0]}"

                        if pd.isna(secondary_emotion):
                            min_emotion = min_category
                        else:
                            min_emotion = f"{min_category}{matching_row['SECONDARY EMOTION'].iloc[0]}"

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

        results_df = pd.DataFrame(results).fillna(0)
        results_df = results_df.loc[:, (results_df != 0).any(axis=0)]

        logging.info("Saving results to results/speeches_processed.csv")
        Path("results/speeches_processed.csv").parent.mkdir(parents=True, exist_ok=True)
        results_df.to_csv('results/speeches_processed.csv', index=False)
        return results_df

    def process_texts(self, input_series: pd.Series) -> pd.DataFrame:
        """
        Process the texts in the input series and extract the emotions and polarity using SenticNet.

        Args:
            input_series (pd.Series): The input series containing the texts.

        Returns:
            pd.DataFrame: A dataframe containing the processed texts with extracted emotions and polarity.

        Example:
            >>> input_series = pd.Series(['I am happy', 'I am sad'])
            >>> processor = SpeechProcessor('data/SenticNet4.txt')
            >>> processor.process_texts(input_series)
                       text  JOY  POLARITY
            0  I am happy  0.0  0.500000
            1    I am sad  0.0 -0.333333
        """
        results = []
        logging.info("Starting to process")
        for text in tqdm(input_series,total=len(input_series) , desc="Processing texts"):
            text_processed = nlp(text)

            accumulators = {}
            polaritylist = []
            for sent in text_processed.sents:
                for token in sent:
                    token_text = token.text.lower()
                    matching_row = self.senticnet_data[self.senticnet_data['CONCEPT'] == token_text]
                    if not matching_row.empty:
                        max_category = matching_row[self.categories].astype(float).idxmax(axis=1).iloc[0]
                        min_category = matching_row[self.categories].astype(float).idxmin(axis=1).iloc[0]

                        primary_emotion = matching_row['PRIMARY EMOTION'].iloc[0]
                        secondary_emotion = matching_row['SECONDARY EMOTION'].iloc[0]

                        if pd.isna(primary_emotion):
                            max_emotion = max_category
                        else:
                            max_emotion = f"{max_category}{matching_row['PRIMARY EMOTION'].iloc[0]}"

                        if pd.isna(secondary_emotion):
                            min_emotion = min_category
                        else:
                            min_emotion = f"{min_category}{matching_row['SECONDARY EMOTION'].iloc[0]}"

                        if max_emotion not in accumulators:
                            accumulators[max_emotion] = []
                        if min_emotion not in accumulators:
                            accumulators[min_emotion] = []

                        accumulators[max_emotion].append(matching_row[max_category].iloc[0])
                        if max_emotion != min_emotion:
                            accumulators[min_emotion].append(matching_row[min_category].iloc[0])

                        polarity = matching_row["POLARITY INTENSITY"].astype(float).iloc[0]
                        polaritylist.append(polarity)

            emotion_avg = {emotion: sum(values) / len(values) if values else 0 for emotion, values in
                           accumulators.items()}
            polarity_avg = {"POLARITY": sum(polaritylist) / len(polaritylist) if polaritylist else 0}

            result_row = {'text': text, **emotion_avg, **polarity_avg}
            results.append(result_row)

        results_df = pd.DataFrame(results).fillna(0)
        results_df = results_df.loc[:, (results_df != 0).any(axis=0)]

        logging.info("Saving results to results/processed_texts.csv")
        Path("results/processed_texts.csv").parent.mkdir(parents=True, exist_ok=True)
        results_df.to_csv('results/processed_texts.csv', index=False)
        return results_df

# Example usage
# processor = SpeechProcessor('data/SenticNet4.txt')
# input_df = pd.DataFrame({'title': ['Title 1', 'Title 2'], 'speaker': ['Speaker 1', 'Speaker 2'], 'speech': ['I am happy', 'I am sad']})
# processed_speeches = processor.process_speeches(input_df)
# print(processed_speeches)

# input_df = pd.DataFrame({'id': [1, 2], 'text': ['I am happy', 'I am sad']})
# processed_texts = processor.process_texts(input_df)
# print(processed_texts)
