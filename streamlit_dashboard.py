# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import plotly.express as px
# from io import BytesIO
#
# # Set page layout
# st.set_page_config(page_title="Analysis Dashboard", layout="wide")
#
#
# # Function to load data
# @st.cache
# def load_data(file):
#     data = pd.read_excel(file)
#     return data
#
#
# # Function to filter data by date range (if applicable)
# def filter_by_date(data, date_column, start_date, end_date):
#     filtered_data = data[(data[date_column] >= start_date) & (data[date_column] <= end_date)]
#     return filtered_data
#
#
# # Function to download dataframe as Excel
# def to_excel(df):
#     output = BytesIO()
#     writer = pd.ExcelWriter(output, engine='xlsxwriter')
#     df.to_excel(writer, index=False, sheet_name='Sheet1')
#     writer.save()
#     processed_data = output.getvalue()
#     return processed_data
#
#
# # Sidebar - file uploader
# st.sidebar.title("Upload Your Data")
# uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type="xlsx")
#
# if uploaded_file is not None:
#     data = load_data(uploaded_file)
#     st.sidebar.success("Data successfully loaded!")
#
#     # Display the first few rows of the dataset
#     st.write("### Dataset Preview")
#     st.dataframe(data.head())
#
#     # Sidebar - options for visualizations
#     st.sidebar.title("Visualization Options")
#     chart_type = st.sidebar.selectbox("Select Chart Type",
#                                       ["Bar Chart", "Pie Chart", "Line Chart", "Correlation Heatmap",
#                                        "Correlation Matrix"])
#
#     # Feature selection for visualizations
#     column = st.sidebar.selectbox("Select Feature for Visualization", data.columns)
#
#     # Additional Feature Filtering
#     st.sidebar.title("Feature Filtering")
#     filter_column = st.sidebar.selectbox("Filter by Feature", data.columns)
#     unique_values = data[filter_column].unique()
#     selected_values = st.sidebar.multiselect(f"Select {filter_column} values to filter", unique_values,
#                                              default=unique_values)
#
#     # Apply the filter
#     filtered_data = data[data[filter_column].isin(selected_values)]
#
#     # If dataset has date columns, filter by date range
#     if 'Date' in data.columns:  # Assuming a date column named 'Date'
#         st.sidebar.title("Date Range Filter")
#         start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime(data['Date']).min())
#         end_date = st.sidebar.date_input("End Date", value=pd.to_datetime(data['Date']).max())
#
#         # Apply date filter
#         filtered_data = filter_by_date(filtered_data, 'Date', start_date, end_date)
#
#     # Bar Chart
#     if chart_type == "Bar Chart":
#         st.write(f"### Bar Chart for {column}")
#         fig = px.bar(filtered_data, x=filtered_data.index, y=column)
#         st.plotly_chart(fig)
#
#     # Pie Chart
#     elif chart_type == "Pie Chart":
#         st.write(f"### Pie Chart for {column}")
#         fig = px.pie(filtered_data, names=column)
#         st.plotly_chart(fig)
#
#     # Line Chart
#     elif chart_type == "Line Chart":
#         st.write(f"### Line Chart for {column}")
#         fig = px.line(filtered_data, x=filtered_data.index, y=column)
#         st.plotly_chart(fig)
#
#     # Correlation Heatmap
#     elif chart_type == "Correlation Heatmap":
#         st.write("### Correlation Heatmap")
#         correlation_matrix = filtered_data.corr()
#         plt.figure(figsize=(10, 6))
#         sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
#         st.pyplot(plt)
#
#     # Correlation Matrix
#     elif chart_type == "Correlation Matrix":
#         st.write("### Correlation Matrix")
#         correlation_matrix = filtered_data.corr()
#         st.dataframe(correlation_matrix)
#
#     # Sidebar - Additional analysis options
#     st.sidebar.title("Additional Analysis")
#     if st.sidebar.checkbox("Show Data Statistics"):
#         st.write("### Data Statistics")
#         st.write(filtered_data.describe())
#
#     # Download Option for Filtered Data
#     st.sidebar.title("Export Data")
#     if st.sidebar.button('Download Filtered Data as Excel'):
#         excel_data = to_excel(filtered_data)
#         st.download_button(label='Download Excel file', data=excel_data, file_name='filtered_data.xlsx')
#
# else:
#     st.sidebar.info("Awaiting file upload.")
#     st.write("## Please upload an Excel file to start.")
#
# # Footer - Streamlit branding
# st.sidebar.markdown("---")
# st.sidebar.text("Built with Streamlit")
#

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Function to create charts for single column
def plot_single_column_chart(data, column, chart_type):
    fig, ax = plt.subplots()

    if chart_type == 'Line Chart':
        ax.plot(data[column])
    elif chart_type == 'Bar Chart':
        ax.bar(data.index, data[column])
    elif chart_type == 'Histogram':
        ax.hist(data[column], bins=20)
    elif chart_type == 'Box Plot':
        sns.boxplot(y=data[column], ax=ax)
    elif chart_type == 'Pie Chart':
        ax.pie(data[column].value_counts(), labels=data[column].value_counts().index, autopct='%1.1f%%')

    st.pyplot(fig)


# Function to create charts for two columns
def plot_two_columns_chart(data, x_column, y_column, chart_type):
    fig, ax = plt.subplots()

    if chart_type == 'Scatter Plot':
        ax.scatter(data[x_column], data[y_column])
    elif chart_type == 'Line Chart':
        ax.plot(data[x_column], data[y_column])
    elif chart_type == 'Bar Chart':
        ax.bar(data[x_column], data[y_column])
    elif chart_type == 'Box Plot':
        sns.boxplot(x=data[x_column], y=data[y_column], ax=ax)
    elif chart_type == 'Heatmap':
        sns.heatmap(pd.crosstab(data[x_column], data[y_column]), annot=True, ax=ax)

    st.pyplot(fig)


# Main function to run the Streamlit app
def main():
    st.title("Customizable Excel Data Visualization")

    # Step 1: Upload Excel File
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

    if uploaded_file:
        # Step 2: Display Excel Data
        df = pd.read_excel(uploaded_file)
        st.write("### Excel Data")
        st.dataframe(df)

        # Step 3: Single column charts
        st.write("### Single Column Charts")
        column = st.selectbox("Select a column", df.columns)
        chart_type = st.selectbox("Select chart type",
                                  ['Line Chart', 'Bar Chart', 'Histogram', 'Box Plot', 'Pie Chart'])
        plot_single_column_chart(df, column, chart_type)

        # Step 4: Two column charts
        st.write("### Two Columns Charts")
        x_column = st.selectbox("Select X-axis column", df.columns, key='x_column')
        y_column = st.selectbox("Select Y-axis column", df.columns, key='y_column')
        chart_type_2 = st.selectbox("Select chart type",
                                    ['Scatter Plot', 'Line Chart', 'Bar Chart', 'Box Plot', 'Heatmap'],
                                    key='chart_type_2')
        plot_two_columns_chart(df, x_column, y_column, chart_type_2)


if __name__ == "__main__":
    main()

