import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# Function to display general data overview
def display_data_overview(df):
    st.write("### Data Overview")
    st.write(f"Number of rows: {df.shape[0]}")
    st.write(f"Number of columns: {df.shape[1]}")
    st.write("Data types:")
    st.write(df.dtypes)
    st.write("Sample data:")
    st.write(df.head())


# Function to display basic statistics
def display_basic_statistics(df):
    st.write("### Basic Statistics")
    st.write(df.describe())


# Function to display missing values
def display_missing_values(df):
    st.write("### Missing Values")
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if not missing.empty:
        st.write(missing)
        fig, ax = plt.subplots()
        sns.barplot(x=missing.index, y=missing.values, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        st.pyplot(fig)
    else:
        st.write("No missing values.")


# Function to display correlation heatmap
def display_correlation_heatmap(df):
    st.write("### Correlation Heatmap")
    corr = df.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)


# Function to display distribution plots for numeric columns
def display_distribution_plots(df):
    st.write("### Distribution of Numeric Columns")
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    selected_columns = st.multiselect("Select columns for distribution plot", numeric_columns)

    if selected_columns:
        for col in selected_columns:
            st.write(f"Distribution for {col}")
            fig, ax = plt.subplots()
            sns.histplot(df[col], bins=20, kde=True, ax=ax)
            st.pyplot(fig)


# Function to display pairplot for numeric columns
def display_pairplot(df):
    st.write("### Pairplot")
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    selected_columns = st.multiselect("Select columns for pairplot", numeric_columns, key="pairplot")

    if selected_columns:
        fig = sns.pairplot(df[selected_columns])
        st.pyplot(fig)


# Function to display boxplot for numeric columns
def display_boxplot(df):
    st.write("### Boxplot")
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    selected_column = st.selectbox("Select column for boxplot", numeric_columns, key="boxplot")

    if selected_column:
        fig, ax = plt.subplots()
        sns.boxplot(y=df[selected_column], ax=ax)
        st.pyplot(fig)


# Main function to run the Streamlit app
def main():
    st.title("Detailed Exploratory Data Analysis Dashboard")

    # Upload Excel File
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls", "csv"])

    if uploaded_file:
        # Load Data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, index_col=0, sheet_name=None)

        # Display Data Overview
        st.sidebar.subheader("Data Overview")
        if st.sidebar.checkbox("Show Data Overview"):
            display_data_overview(df)

        # Basic Statistics
        st.sidebar.subheader("Basic Statistics")
        if st.sidebar.checkbox("Show Basic Statistics"):
            display_basic_statistics(df)

        # Missing Values
        st.sidebar.subheader("Missing Values")
        if st.sidebar.checkbox("Show Missing Values"):
            display_missing_values(df)

        # Correlation Heatmap
        st.sidebar.subheader("Correlation Heatmap")
        if st.sidebar.checkbox("Show Correlation Heatmap"):
            display_correlation_heatmap(df.select_dtypes(include='number'))

        # Distribution Plots
        st.sidebar.subheader("Distribution Plots")
        if st.sidebar.checkbox("Show Distribution Plots"):
            display_distribution_plots(df)

        # Pairplot
        st.sidebar.subheader("Pairplot")
        if st.sidebar.checkbox("Show Pairplot"):
            display_pairplot(df)

        # Boxplot
        st.sidebar.subheader("Boxplot")
        if st.sidebar.checkbox("Show Boxplot"):
            display_boxplot(df)


if __name__ == "__main__":
    main()
