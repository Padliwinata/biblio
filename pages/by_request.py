import pandas as pd
import matplotlib.pyplot as plt
import requests
import streamlit as st


st.title("These data are provided by request")
st.write("The 'app' page can be explored to get another data or just request to get another specific data")

st.sidebar.write("This image of a cat to cheer your day")
res = requests.get("https://api.thecatapi.com/v1/images/search")
st.sidebar.image(res.json()[0]['url'], width=200)

tab1, tab2 = st.tabs(['Indonesia', 'Unpad'])

with tab1:
    st.header("Gender research trend in Indonesia (2020-2025)")
    df = pd.read_csv('pages/datasets/gender_trend_indonesia.csv')
    df = df.drop(columns=["Unnamed: 0"])
    # Count publications by year
    counts = df.groupby('publication_year').size()

    # Sort by year
    counts = counts.sort_index()

    # Create the plot
    fig, ax = plt.subplots()
    bars = ax.bar(counts.index.astype(str), counts.values, color='skyblue')

    # Add numbers on top of bars
    for i, val in enumerate(counts.values):
        ax.text(i, val + max(counts.values) * 0.01, str(val), ha='center', va='bottom', fontsize=9)

    # Plot a line connecting the tops of the bars
    ax.plot(range(len(counts)), counts.values, color='orange', marker='o', linestyle='-', linewidth=2)

    # Set labels and title
    ax.set_xlabel('Publication Year')
    ax.set_ylabel('Number of Publications')
    ax.set_title('Publications per Year')

    # Display in Streamlit
    st.pyplot(fig)
    st.dataframe(df)

    st.write('Specific with "gender" keyword')
    df = pd.read_csv('pages/datasets/gender_trend_indonesia_specific.csv')
    df = df.drop(columns=["Unnamed: 0"])
    # Count publications by year
    counts = df.groupby('publication_year').size()

    # Sort by year
    counts = counts.sort_index()

    # Create the plot
    fig, ax = plt.subplots()
    bars = ax.bar(counts.index.astype(str), counts.values, color='skyblue')

    # Add numbers on top of bars
    for i, val in enumerate(counts.values):
        ax.text(i, val + max(counts.values) * 0.01, str(val), ha='center', va='bottom', fontsize=9)

    # Plot a line connecting the tops of the bars
    ax.plot(range(len(counts)), counts.values, color='orange', marker='o', linestyle='-', linewidth=2)

    # Set labels and title
    ax.set_xlabel('Publication Year')
    ax.set_ylabel('Number of Publications')
    ax.set_title('Publications per Year')

    # Display in Streamlit
    st.pyplot(fig)
    st.dataframe(df)

with tab2:
    st.header("Gender research trend in Unpad (2020-2025)")
    df = pd.read_csv('pages/datasets/gender_trend_unpad.csv')
    df = df.drop(columns=["Unnamed: 0"])
    # Count publications by year
    counts = df.groupby('publication_year').size()

    # Sort by year
    counts = counts.sort_index()

    # Create the plot
    fig, ax = plt.subplots()
    bars = ax.bar(counts.index.astype(str), counts.values, color='skyblue')

    # Add numbers on top of bars
    for i, val in enumerate(counts.values):
        ax.text(i, val + max(counts.values) * 0.01, str(val), ha='center', va='bottom', fontsize=9)

    # Plot a line connecting the tops of the bars
    ax.plot(range(len(counts)), counts.values, color='orange', marker='o', linestyle='-', linewidth=2)

    # Set labels and title
    ax.set_xlabel('Publication Year')
    ax.set_ylabel('Number of Publications')
    ax.set_title('Publications per Year')

    # Display in Streamlit
    st.pyplot(fig)
    st.dataframe(df)
    st.write('Specific with "gender" keyword')
    df = pd.read_csv('pages/datasets/gender_trend_unpad_specific.csv')
    df = df.drop(columns=["Unnamed: 0"])
    # Count publications by year
    counts = df.groupby('publication_year').size()

    # Sort by year
    counts = counts.sort_index()

    # Create the plot
    fig, ax = plt.subplots()
    bars = ax.bar(counts.index.astype(str), counts.values, color='skyblue')

    # Add numbers on top of bars
    for i, val in enumerate(counts.values):
        ax.text(i, val + max(counts.values) * 0.01, str(val), ha='center', va='bottom', fontsize=9)

    # Plot a line connecting the tops of the bars
    ax.plot(range(len(counts)), counts.values, color='orange', marker='o', linestyle='-', linewidth=2)

    # Set labels and title
    ax.set_xlabel('Publication Year')
    ax.set_ylabel('Number of Publications')
    ax.set_title('Publications per Year')

    # Display in Streamlit
    st.pyplot(fig)
    st.dataframe(df)


