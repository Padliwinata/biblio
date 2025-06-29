import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


def citation_frequency_table_human_bins(df, column="citation"):
    """
    Create a frequency table with human-readable citation bins (e.g. '1–5', '6–10', etc.)

    Returns:
        freq_df (pd.DataFrame): DataFrame with readable citation ranges and frequencies.
    """
    # Ensure the column is numeric
    df[column] = pd.to_numeric(df[column], errors='coerce')
    df_clean = df.dropna(subset=[column])

    max_citation = int(df_clean[column].max())

    # Define custom bin edges: example bin edges like 0, 5, 10, 20, 50, 100, ...
    custom_bins = []
    current = 0
    steps = [5, 5, 10, 30, 50, 100, 200, 300, 500, 1000]

    for step in steps:
        next_bin = current + step
        if next_bin >= max_citation:
            custom_bins.append(max_citation + 1)
            break
        custom_bins.append(next_bin)
        current = next_bin

    bin_edges = [0] + custom_bins

    # Bin the data
    df_clean["citation_bin"] = pd.cut(df_clean[column], bins=bin_edges, right=True)

    # Create string labels for human readability
    labels = [f"{int(interval.left + 1)}–{int(interval.right)}" for interval in df_clean["citation_bin"].cat.categories]
    df_clean["citation_bin"] = pd.cut(df_clean[column], bins=bin_edges, labels=labels, right=True)

    # Frequency count
    freq_series = df_clean["citation_bin"].value_counts().sort_index()

    # To DataFrame
    freq_df = freq_series.reset_index()
    freq_df.columns = ["Citation Range", "Frequency"]

    return freq_df


file = st.sidebar.file_uploader('Upload CSV Document', type='csv', accept_multiple_files=False)


if file is not None:
    new_df = pd.read_csv(file)
    # Define bin boundaries
    bins_min = int(new_df['citation'].min())
    bins_max = int(new_df['citation'].max())
    bins = list(range(bins_min, bins_max + 2))  # +2 to include last value

    # Create histogram
    fig, ax = plt.subplots()
    n, bins_used, patches = ax.hist(new_df['citation'], bins=bins, edgecolor='black')

    # Remove grid
    ax.grid(False)

    # Set x-axis ticks to integers
    ax.set_xticks(np.arange(bins_min, bins_max + 1, 1))
    ax.set_xticklabels(np.arange(bins_min, bins_max + 1, 1))

    # Calculate bar centers for placing markers
    bar_centers = 0.5 * (bins_used[:-1] + bins_used[1:])

    # Plot markers and line
    ax.plot(bar_centers, n, marker='o', linestyle='-', color='orange', label='Frequency')

    # Optional: add exact numbers above each marker
    for x, y in zip(bar_centers, n):
        ax.annotate(str(int(y)), xy=(x, y), xytext=(0, 5), textcoords='offset points',
                    ha='center', fontsize=9, color='black')

    ax.set_xlabel("Citation Count")
    ax.set_ylabel("Frequency")
    ax.set_title("Histogram of Citation Distribution")

    # Show in Streamlit
    st.pyplot(fig)
    plt.clf()
else:
    st.write("Please upload some CSV document")


