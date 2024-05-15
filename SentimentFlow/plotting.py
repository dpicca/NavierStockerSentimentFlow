import matplotlib.pyplot as plt
import numpy as np
import math
from pathlib import Path
import logging

def normalize_data(data):
    min_val = np.min(data)
    max_val = np.max(data)
    normalized = 2 * ((data - min_val) / (max_val - min_val)) - 1 if max_val > min_val else -np.ones_like(data)
    return normalized

def plot_speaker_simulations(all_s):
    for title, speakers_data in all_s.items():
        filtered_speakers_data = [d for d in speakers_data if d['simulation'].size]

        num_speakers = len(filtered_speakers_data)
        num_cols = 3
        num_rows = math.ceil(num_speakers / num_cols)

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
        if num_rows * num_cols > 1:
            axes = axes.flatten()
        else:
            axes = [axes]

        subplot_index = 0

        for speaker_data in filtered_speakers_data:
            ax = axes[subplot_index]
            subplot_index += 1

            simulations = speaker_data['simulation']
            x_axis = range(1, simulations.shape[0] + 1)

            simulation_labels = ['ATTITUDE', 'INTROSPECTION', 'SENSITIVITY', 'TEMPER']
            for i, label in enumerate(simulation_labels):
                normalized_sim_step = normalize_data(simulations[:, i])
                ax.plot(x_axis, normalized_sim_step, label=label)

            ax.set_title(f'{speaker_data["speaker"]}')
            ax.set_xlabel('Simulation Step')
            ax.set_ylabel('Normalized Simulation Value')
            ax.legend(title="Simulation Components")

            ax.set_xticks([x for x in x_axis if x == 1 or x % 5 == 0])
            ax.set_xticklabels([x for x in x_axis if x == 1 or x % 5 == 0])

        for j in range(subplot_index, len(axes)):
            axes[j].axis('off')

        fig.suptitle(title)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        Path("results/sentiment_flow_plots").mkdir(parents=True, exist_ok=True)
        plt.savefig(f'results/sentiment_flow_plots/{title}.png')
        logging.info(f"Saved plot for {title}")
        plt.close()

def plot_highest_avg_dimension(all_s, dimension_names):
    for title, speakers_data in all_s.items():
        num_speakers = len(speakers_data)
        num_cols = 3
        num_rows = math.ceil(num_speakers / num_cols)

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
        if num_rows * num_cols > 1:
            axes = axes.flatten()
        else:
            axes = [axes]

        for i, speaker_data in enumerate(speakers_data):
            if i >= len(axes):
                break

            ax = axes[i]
            simulations = speaker_data['simulation']

            if simulations.size == 0 or not any(len(sim) > 0 for sim in simulations):
                ax.text(0.5, 0.5, 'No Data', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
                ax.set_title(f'{speaker_data["speaker"]}')
                continue

            avg_values = np.mean(normalize_data(np.array(simulations)), axis=0)
            max_avg_dim_index = np.argmax(avg_values)
            max_avg_dim = avg_values[max_avg_dim_index]

            ax.plot(normalize_data(np.array(simulations))[:, max_avg_dim_index], label=f"{dimension_names[max_avg_dim_index].split('#')[0]} (Avg: {max_avg_dim:.2f})")
            ax.set_title(f'{speaker_data["speaker"]}')
            ax.set_xlabel('Text Segment')
            ax.set_ylabel('Normalized Value')
            ax.legend()

        fig.suptitle(title)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        Path("results/sentiment_flow_plots_highest_avg").mkdir(parents=True, exist_ok=True)
        plt.savefig(f'results/sentiment_flow_plots_highest_avg/{title}.png')
        logging.info(f"Saved plot for {title}")
        plt.close()
