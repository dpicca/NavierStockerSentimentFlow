# NavierStockerSentimentFlow

NavierStockerSentimentFlow is a Python package designed for processing and analyzing sentiment flow in texts and speeches using principles derived from fluid dynamics. By combining sentiment analysis with the Navier-Stokes equations, this package allows for a novel approach to understanding and modeling the dynamics of emotions in text data.

## Features

- **Sentiment Analysis**: Uses SenticNet to extract primary and secondary emotions and polarity from texts and speeches.
- **Fluid Dynamics Simulation**: Applies the Navier-Stokes equations to model the flow of sentiment through texts and speeches.

## Installation

You can install the package via pip:

```sh
pip install git+https://github.com/unil-ish/sentimentflow
```

## Dependencies

- `spacy`
- `tqdm`
- `numpy`
- `pandas`
- `scipy`

These dependencies will be automatically installed with the package.

## General Idea of Navier-Stokes and Sentiment Flow

The Navier-Stokes equations are a set of partial differential equations that describe the motion of fluid substances such as liquids and gases. These equations account for various factors including velocity, pressure, density, and viscosity of the fluid. In the context of sentiment analysis, we adapt these principles to model the flow and dynamics of emotions in text and speech.

### How the Package Applies Navier-Stokes to Sentiment

1. **Sentiment Density**: Analogous to fluid density, sentiment density is calculated as the sum of absolute sentiment scores derived from SenticNet.
2. **Sentiment Pressure**: Similar to fluid pressure, sentiment pressure is influenced by the presence of certain keywords in the text or speech that trigger emotional responses.
3. **Sentiment Viscosity**: Corresponding to fluid viscosity, sentiment viscosity represents the variability in sentiment scores.
4. **External Contextual Force**: This factor is analogous to external forces acting on a fluid, modeled here as the overall polarity of the text or speech influencing the flow of sentiment.

By treating the sentiment of a text or speech as a dynamic system, the package simulates how emotions propagate and interact within the text, providing a deeper understanding of the emotional undercurrents.

## Usage

### Step 1: Initialize the Processor

First, initialize the `SpeechProcessor` with the path to the SenticNet data file.

```python
import pandas as pd
from SentimentFlow import SpeechProcessor

processor = SpeechProcessor('path_to_senticnet.tsv')
```

### Step 2: Process Texts or Speeches

You can process texts using the `process_texts` method. This method takes a Pandas Series of texts and returns a DataFrame with extracted emotions and polarity.

```python
texts = pd.Series([
    'Despite the challenges, I feel quite optimistic about the future and the opportunities it holds.',
    'Today has been a particularly tough day, and I am feeling overwhelmed by everything happening around me.',
    'I am delighted with the progress I have made on my project and look forward to sharing it with my team.'
])

processed_texts = processor.process_texts(texts)
print(processed_texts)
```

Alternatively, you can process speeches using the `process_speeches` method. This method takes a Pandas DataFrame with columns 'title', 'speaker', and 'speech', and returns a DataFrame with extracted emotions and polarity.

```python
speeches = pd.DataFrame({
    'title': ['Title 1', 'Title 2'],
    'speaker': ['Speaker 1', 'Speaker 2'],
    'speech': ['I am happy', 'I am sad']
})

processed_speeches = processor.process_speeches(speeches)
print(processed_speeches)
```

### Step 3: Calculate Sentiment Flow

To calculate the sentiment flow using the Navier-Stokes equations, initialize the `SentimentFlowCalculator` and call the appropriate method.

#### For Texts

```python
from SentimentFlow import SentimentFlowCalculator

flow_calculator = SentimentFlowCalculator()
results = flow_calculator.calculate_navier_stocker_for_texts(processed_texts)
print(results)
```

#### For Speeches

```python
results = flow_calculator.calculate_navier_stocker_for_speeches(processed_speeches)
print(results)
```

## Example

Here is a complete example combining the steps above:

```python
import pandas as pd
from SentimentFlow import SpeechProcessor, SentimentFlowCalculator

# Initialize processor and process texts
processor = SpeechProcessor('path_to_senticnet.tsv')
texts = pd.Series([
    'Despite the challenges, I feel quite optimistic about the future and the opportunities it holds.',
    'Today has been a particularly tough day, and I am feeling overwhelmed by everything happening around me.',
    'I am delighted with the progress I have made on my project and look forward to sharing it with my team.'
])
processed_texts = processor.process_texts(texts)

# Initialize flow calculator and calculate sentiment flow for texts
flow_calculator = SentimentFlowCalculator()
text_results = flow_calculator.calculate_navier_stocker_for_texts(processed_texts)
print(text_results)

# Process speeches
speeches = pd.DataFrame({
    'title': ['Title 1', 'Title 2'],
    'speaker': ['Speaker 1', 'Speaker 2'],
    'speech': ['I am happy', 'I am sad']
})
processed_speeches = processor.process_speeches(speeches)

# Calculate sentiment flow for speeches
speech_results = flow_calculator.calculate_navier_stocker_for_speeches(processed_speeches)
print(speech_results)
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/unil-ish/sentimentflow/blob/main/LICENSE) file for more details.

## Author

Your Name
[Email](mailto:your.email@example.com)
[GitHub](https://github.com/unil-ish/sentimentflow)

## Acknowledgements

This package leverages the power of the SenticNet knowledge base and the computational capabilities of the Navier-Stokes equations to provide a unique tool for sentiment analysis. Special thanks to the developers of these foundational technologies.
