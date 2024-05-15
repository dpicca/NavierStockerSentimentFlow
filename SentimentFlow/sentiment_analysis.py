import numpy as np
from scipy.integrate import odeint
from tqdm.notebook import tqdm
import logging


def calculate_sentiment_density(sentiment_scores: np.ndarray):
    return np.sum(np.abs(sentiment_scores))


def calculate_sentiment_pressure(score, keywords, text):
    pressure = 0
    if any(keyword.lower() in text.lower() for keyword in keywords):
        pressure += score
    return pressure


def calculate_sentiment_viscosity(sentiment_scores):
    return np.std(sentiment_scores)


def calculate_external_contextual_force(polarity):
    return polarity


def navier_stokes_sentiment_flow(rho_sent, p_sent, nu_sent, g_context, s):
    if rho_sent == 0:
        pressure_term = np.zeros_like(s)
    else:
        pressure_term = -1 / rho_sent * np.gradient(p_sent)

    grad_s = np.gradient(s)
    laplacian_s = np.gradient(grad_s)

    if np.any(np.isnan(s)) or np.any(np.isinf(s)) or np.any(np.isnan(grad_s)) or np.any(np.isinf(grad_s)):
        logging.warning("Warning: NaN or inf detected in s or grad_s. Skipping this iteration.")
        return None

    convective_term = s * grad_s
    viscous_term = nu_sent * laplacian_s

    rhs = convective_term + pressure_term + viscous_term + g_context
    np.clip(rhs, -1e10, 1e10, out=rhs)

    if np.any(np.isnan(rhs)) or np.any(np.isinf(rhs)):
        logging.warning("Warning: NaN or inf detected in rhs. Skipping this iteration.")
        return None

    return rhs


def differential_equation(s, t, speech_info):
    rho_sent, p_sent, nu_sent, g_context = speech_info
    dsdt = navier_stokes_sentiment_flow(rho_sent, p_sent, nu_sent, g_context, s)

    if dsdt is None:
        raise ValueError("Invalid sentiment flow calculation")

    return dsdt


def calculate_navier_stocker(data):
    all_s = {}
    sentiment_columns = data.columns.difference(['title', 'speaker', 'speech', 'POLARITY'])

    for speaker in tqdm(data['speaker'].unique(), desc="Processing speakers"):
        speaker_data = data[data['speaker'] == speaker]
        title = speaker_data.iloc[0]['title']
        initial_speaker = speaker_data.iloc[0]
        s0 = initial_speaker[sentiment_columns].apply(pd.to_numeric, errors='coerce').fillna(0).to_numpy()
        s0_g_context = calculate_external_contextual_force(initial_speaker['POLARITY'])
        initial_speech = initial_speaker['speech']
        current_time = 0
        all_results = []
        unique_all_results = []

        for i in range(1, len(speaker_data)):
            current_speech_data = speaker_data.iloc[i]
            if i == 1:
                g_context = s0_g_context
                current_speech = initial_speech
            else:
                g_context = calculate_external_contextual_force(current_speech_data['POLARITY'])
                current_speech = current_speech_data['speech']

            t = np.array([current_time, current_time + 1])
            speech_info = (
                calculate_sentiment_density(s0),
                np.array([calculate_sentiment_pressure(score, keywords_example, current_speech) for score in s0]),
                calculate_sentiment_viscosity(s0),
                g_context
            )
            s = odeint(differential_equation, s0, t, args=(speech_info,))

            for sim_result in s.tolist():
                all_results.append((sim_result, current_speech))

            s0 = s[-1]
            current_time += 1

        simulation_results, speeches = zip(*unique_all_results) if unique_all_results else ([], [])
        simulation_results = np.vstack(simulation_results) if simulation_results else np.array([])

        if title not in all_s:
            all_s[title] = []
        all_s[title].append({
            'speaker': speaker,
            'speech': speeches,
            'simulation': simulation_results,
            'emotion dimension': sentiment_columns
        })

    return all_s
