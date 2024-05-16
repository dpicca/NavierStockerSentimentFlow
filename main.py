#
import pandas as pd

from SentimentFlow.sentiment_analysis import SentimentFlowCalculator
from SentimentFlow.data_processing import SpeechProcessor


sentiment_calculator = SentimentFlowCalculator()
#
df = pd.Series(
    [
        'Despite the challenges, I feel quite optimistic about the future and the opportunities it holds.',
        'Today has been a particularly tough day, and I am feeling overwhelmed by everything happening around me.',
        'I am delighted with the progress I have made on my project and look forward to sharing it with my team.',
        'There are days when everything feels like it is falling apart, and today is one of those days for me.',
        'I cannot contain my excitement about the upcoming vacation; it has been a long time since I took a break.',
        'I am deeply disappointed with the results of the recent meeting; I had higher expectations from the team.',
        'After a productive week, I am content with how things have turned out and ready for a relaxing weekend.',
        'The ongoing issues at work are causing a lot of frustration, and I am struggling to find a solution.',
        'I feel elated after receiving the news about my promotion; it is a significant milestone in my career.',
        'The uncertainty of the current situation is making me anxious, and I am finding it hard to focus.'
    ]
)

SpeechProcessor = SpeechProcessor('senticnet.tsv')
processed_df = SpeechProcessor.process_texts(df)

results = sentiment_calculator.calculate_navier_stocker_for_texts(processed_df)
