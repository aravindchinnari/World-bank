import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration - This must be the very first Streamlit command used
st.set_page_config(page_title="Brazil Jobs Data Analysis", page_icon="📊", layout="wide")

# Function to load data with an option to specify the number of rows
@st.cache(allow_output_mutation=True)
def load_data(max_rows=None):
    try:
        # Adjust the file path as needed
        #data = pd.read_csv(r"C:\GWU\world bank\brazil.csv", nrows=max_rows)
        data = pd.read_csv(r"C:\Users\aravi\Downloads\BRA_GLD_Data_CSV\BRA_GLD_Data.csv", nrows=max_rows)
        return data
    except FileNotFoundError:
        st.error("File not found. Please check the file path and try again.")
        return pd.DataFrame()  # Returns an empty DataFrame if the file is not found

# Sidebar for data load options
st.sidebar.header("Data Load Options")
row_limit = st.sidebar.number_input('Number of rows to load:', min_value=100, max_value=1000000, value=1000, step=100)

# Load data
data = load_data(max_rows=row_limit)

# First row for identifying information

# Sidebar for selecting year - assuming 'year' is a column in your data
if 'year' in data.columns:
    years = sorted(data['year'].unique())
    selected_year = st.sidebar.selectbox('Select Year', years)
    data = data[data['year'] == selected_year]  # Filter data for selected year
else:
    st.error("Year data is not available in the dataset.")
    
col1, col2, col3 = st.columns(3)
col1.metric(label="Country Code", value="BRA")
col2.metric(label="Survey Name", value="PNAD")
col3.metric(label="Survey Type", value="Other Household Survey")

# Second row for version information
col4, col5, col6, col7 = st.columns(4)
col4.metric(label="ICLS Version", value="ICLS-13")
col5.metric(label="ISCED Version", value="isced_2011")
col6.metric(label="ISCO Version", value="isco_1988")
col7.metric(label="ISIC Version", value="isic_3")

# Third row for year
col8, col9 = st.columns(2)
col8.metric(label="Year", value=selected_year)  # Using only one column here for Year, center it by using an empty column next
col9.metric(label="Month", value = 'September')

if not data.empty:
    # Sidebar for filtering data
    st.sidebar.header('Filter Data')
    age = st.sidebar.slider('Age', int(data['age'].min()), int(data['age'].max()), (25, 40))
    gender = st.sidebar.radio('Gender', ['All', 'Male', 'Female'])
    education_level = st.sidebar.selectbox('Education Level', ['All'] + list(data['educat7'].unique()))

    # Apply filters
    if gender != 'All':
        data = data[data['male'] == (gender == 'Male')]
    if education_level != 'All':
        data = data[data['educat7'] == education_level]
    data = data[(data['age'] >= age[0]) & (data['age'] <= age[1])]

    # Display filtered data overview
    st.header('Filtered Data Overview')
    st.write(data)

    # Visualization: Age Distribution Plot
    st.header(f'Age Distribution for {gender} aged {age[0]} to {age[1]}')
    fig, ax = plt.subplots()
    sns.histplot(data['age'], bins=30, kde=False, ax=ax)
    ax.set_title('Age Distribution')
    st.pyplot(fig)

    # Visualization: Gender Distribution (if data on gender is available)
    if 'male' in data.columns:
        st.header('Gender Distribution')
        gender_count = data['male'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(gender_count, labels=['Male', 'Female'], autopct='%1.1f%%', startangle=90)
        ax1.set_title('Gender Distribution')
        st.pyplot(fig1)

# Custom CSS for better visualization
st.markdown("""
<style>
.main {
    background-color: #EFEFEF;
}
</style>
""", unsafe_allow_html=True)

st.subheader('Dataset Overview')
st.write(data.head())  # Display the first few rows of the dataset
st.write("Data types:", data.dtypes)  # Show data types of each column



urban_rural = st.sidebar.radio("Area Type", ['All', 'Urban', 'Rural'])

# Apply urban/rural filter
if urban_rural != 'All':
    data = data[data['urban'] == urban_rural]

# Subnational Region Filter (adjust this to use the actual column for subnational regions in your data if available)
if 'subnatid1' in data.columns:
    regions = ['All'] + sorted(data['subnatid1'].unique().tolist())
    selected_region = st.sidebar.selectbox('Region', regions)
    if selected_region != 'All':
        data = data[data['subnatid1'] == selected_region]
if 'subnatid1' in data.columns:
    st.header("Regional Distribution")
    region_data = data['subnatid1'].value_counts()
    fig2, ax2 = plt.subplots()
    region_data.plot(kind='bar', ax=ax2)
    ax2.set_title("Number of Survey Responses by Region")
    ax2.set_xlabel("Region")
    ax2.set_ylabel("Number of Responses")
    st.pyplot(fig2)
st.header("Urban vs Rural Distribution")
urban_rural_data = data['urban'].value_counts()
fig3, ax3 = plt.subplots()
urban_rural_data.plot(kind='pie', labels=urban_rural_data.index, autopct='%1.1f%%', startangle=90, ax=ax3)
ax3.set_title("Urban vs Rural Distribution")
st.pyplot(fig3)


if 'lstatus' in data.columns and 'subnatid1' in data.columns:
    st.header("Employment Status by Region")
    employment_status_region = pd.crosstab(data['subnatid1'], data['lstatus'])
    fig4, ax4 = plt.subplots()
    sns.heatmap(employment_status_region, annot=True, cmap="YlGnBu", ax=ax4)
    ax4.set_title("Heatmap of Employment Status by Region")
    st.pyplot(fig4)

if 'educat7' in data.columns:
    st.header("Education Level Distribution")
    education_data = data['educat7'].value_counts()
    fig5, ax5 = plt.subplots()
    education_data.plot(kind='barh', ax=ax5)
    ax5.set_title("Education Level Distribution")
    st.pyplot(fig5)




