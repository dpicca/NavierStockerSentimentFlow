def main():
    import argparse
    from .data_processing import parse_xml_to_dataframe, process_speeches
    from .sentiment_analysis import calculate_navier_stocker
    from .plotting import plot_speaker_simulations, plot_highest_avg_dimension
    from .utils import save_all_s_to_csv

    parser = argparse.ArgumentParser(description='Process and analyze sentiment in speeches.')
    parser.add_argument('--input', type=str, required=True, help='Path to the input XML file')
    parser.add_argument('--senticnet', type=str, required=True, help='Path to the SenticNet data file')
    args = parser.parse_args()

    df = parse_xml_to_dataframe(args.input)
    processed_df = process_speeches(df, args.senticnet)
    all_s = calculate_navier_stocker(processed_df)
    save_all_s_to_csv(all_s, 'results/allEmotionSimulations.csv')
    plot_speaker_simulations(all_s)
    plot_highest_avg_dimension(all_s, processed_df.columns.difference(['title', 'speaker', 'speech', 'POLARITY']))

if __name__ == '__main__':
    main()
