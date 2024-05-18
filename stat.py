import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
# Load the survey data
@st.cache_data
def load_survey_data():
    survey_raw_df = pd.read_csv("Data/survey_results_public.csv")
    survey_raw_df.drop(0, inplace=True)
    return survey_raw_df

survey_df = load_survey_data()

# Page Title
st.title("Exploratory Data Analysis on Stackoverflow Dataset")

# Display the first few rows of the dataset
st.subheader("Dataset Overview")
st.write(survey_df.head())

# Limiting analysis to selected columns
selected_columns = [
    'MainBranch', 'Employment', 'RemoteWork', 'CodingActivities', 'EdLevel', 'LearnCode',
    'LearnCodeOnline', 'LearnCodeCoursesCert', 'YearsCode', 'YearsCodePro', 'DevType',
    'OrgSize', 'PurchaseInfluence', 'BuyNewTool', 'Country', 'Currency', 'CompTotal',
    'LanguageHaveWorkedWith', 'LanguageWantToWorkWith', 'PlatformHaveWorkedWith',
    'PlatformWantToWorkWith', 'NEWSOSites', 'SOVisitFreq', 'SOAccount', 'SOPartFreq',
    'SOComm', 'Age', 'TBranch', 'ICorPM', 'WorkExp','ProfessionalTech', 'ConvertedCompYearly'
]
survey_df = survey_df[selected_columns]
st.markdown("<hr>", unsafe_allow_html=True)
# Add border to separate sections
st.markdown(
    """
    <style>
    .section-divider {
        border-top: 2px solid #ddd;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Dataset Information
st.markdown("<h2 style='color: #336699;'>Dataset Information</h2>", unsafe_allow_html=True)
st.write(f"The dataset contains over {survey_df.shape[0]} rows and {survey_df.shape[1]} columns.")

# Data Cleaning and Preprocessing
st.markdown("<h2 style='color: #336699;'>Data Cleaning and Preprocessing</h2>", unsafe_allow_html=True)

# Convert YearsCode and YearsCodePro to numeric
survey_df['YearsCode'] = pd.to_numeric(survey_df['YearsCode'], errors='coerce')
survey_df['YearsCodePro'] = pd.to_numeric(survey_df['YearsCodePro'], errors='coerce')

# Display cleaned data
st.subheader("Cleaned Data")
st.write(survey_df.head())

# Employment Categories
employment_categories = [
    'Employed, full-time', 'Independent contractor, freelancer, or self-employed',
    'Student, full-time', 'Employed, part-time', 'Not employed, but looking for work',
    'Student, part-time', 'Not employed, and not looking for work', 'Retired',
    'I prefer not to say'
]

# Developer Types
developer_types = [
    'Senior executive (C-Suite, VP, etc.)',
    'Engineering manager',
    'Marketing or sales professional',
    'Engineer, site reliability',
    'Developer experience',
    'Cloud infrastructure engineer',
    'Blockchain',
    'Developer advocate',
    'Security professional',
    'Scientist',
    'Product manager',
    'Hardware engineer',
    'Research & Development role',
    'Engineer, data',
    'Data scientist or machine learning specialist',
    'DevOps specialist',
    'Database administrator',
    'Developer, embedded applications or devices',
    'Developer, back-end',
    'Developer, full-stack',
    'Developer, game or graphics',
    'Developer, desktop or enterprise applications',
    'Developer, mobile',
    'Educator',
    'Developer, QA or test',
    'Project manager',
    'Data or business analyst',
    'Developer, front-end',
    'Designer',
    'System administrator',
    'Academic researcher',
    'Student'
]

# Specify countries of interest
countries = ['United States of America', 'Germany', 'India', 'United Kingdom', 'Canada']
st.markdown("<hr>", unsafe_allow_html=True)
# Dropdown menu to select country for employment plot
selected_country_employment = st.selectbox("Select Country for Employment Plot", countries)

if selected_country_employment == 'United Kingdom':
    cnt_employment = 'United Kingdom of Great Britain and Northern Ireland'
else:
    cnt_employment = selected_country_employment 

# Group employment by categories and country
grouped_employment_country = survey_df[survey_df['Country'] == cnt_employment]['Employment'].value_counts().reindex(employment_categories, fill_value=0)
# Plot Employment by Country
st.subheader("Employment in " + selected_country_employment)
fig_employment = px.bar(
    x=grouped_employment_country.values,
    y=grouped_employment_country.index,
    orientation='h',
    text=grouped_employment_country.values,
    labels={'x': 'Number of Responses', 'y': 'Employment Status'},
    title="Employment Distribution",
    template="plotly_white",  # Set plot style
    height=500,
    width=800,
)
fig_employment.update_traces(marker=dict(line=dict(width=0.5)))  # Adjust bar border width
fig_employment.update_layout(
    xaxis_showgrid=False,  # Hide x-axis grid lines
    yaxis_showgrid=True,  # Show y-axis grid lines
    yaxis_categoryorder='total ascending',  # Sort y-axis categories
    uniformtext_minsize=8,  # Set minimum font size for text
    margin=dict(l=100, r=100, t=50, b=50)
)
st.plotly_chart(fig_employment)

st.markdown("<hr>", unsafe_allow_html=True)
# Dropdown menu to select country for median salary plot
selected_country_salary = st.selectbox("Select Country for Median Salary Plot", countries)

if selected_country_salary == 'United Kingdom':
    cnt_salary = 'United Kingdom of Great Britain and Northern Ireland'
else:
    cnt_salary = selected_country_salary 

# Group median salaries by country and developer type
median_salary_country_devtype = survey_df[(survey_df['Country'] == cnt_salary) & (~survey_df['DevType'].isna())].groupby(['DevType'])['ConvertedCompYearly'].median().reset_index()

# Filter out developer types with less than 30 entries
median_salary_country_devtype_filtered = median_salary_country_devtype[median_salary_country_devtype['DevType'].map(survey_df['DevType'].value_counts()) >= 30]
median_salary_country_devtype_filtered = median_salary_country_devtype_filtered[median_salary_country_devtype_filtered['ConvertedCompYearly'] <= 130000]


# Plot Median Salary by Country and Developer Type
st.subheader(f"Median Salary in {selected_country_salary}")
fig_salary = px.bar(
    x=median_salary_country_devtype_filtered['ConvertedCompYearly'],
    y=median_salary_country_devtype_filtered['DevType'],
    orientation='h',
    text=median_salary_country_devtype_filtered['ConvertedCompYearly'].apply(lambda x: f"${x:,.0f}"),
    labels={'x': 'Median Salary', 'y': 'Developer Type'},
    title="Median Salary Distribution",
    template="plotly_white",
    height=800,
    width=800
)
fig_salary.update_traces(marker=dict(line=dict(width=0.5)))  # Adjust bar border width
fig_salary.update_layout(
    xaxis_showgrid=False,  # Hide x-axis grid lines
    yaxis_showgrid=True,  # Show y-axis grid lines
    yaxis_categoryorder='total ascending',  # Sort y-axis categories
    uniformtext_minsize=8,  # Set minimum font size for text
    margin=dict(l=100, r=100, t=50, b=50)
)

# Add salaries on bars
for i, bar in enumerate(fig_salary.data):
    fig_salary.add_annotation(
        x=bar.x[0] + 20000,
        y=bar.y[0],
        text=bar.text[0],
        font=dict(color='black', size=10),
        showarrow=False
    )

st.plotly_chart(fig_salary)

st.markdown("<hr>", unsafe_allow_html=True)

# Group by dev type and calculate the median salary and average years of experience
median_salary_avg_exp = survey_df.groupby('DevType').agg({'ConvertedCompYearly': 'median', 'WorkExp': 'mean'}).reset_index()

# Plot Scatter plot
fig_salary_exp = px.scatter(
    x=median_salary_avg_exp['WorkExp'],  # Median salary on x-axis
    y=median_salary_avg_exp['ConvertedCompYearly'],  # Average years of experience on y-axis
    text=median_salary_avg_exp['DevType'],  # Developer Type as text
    labels={'x': 'Average Years of Experience', 'y': 'Median Salary'},
    title="Median Salary vs Average Years of Experience by Developer Type",
    template="plotly_dark",  # Dark mode template
    height=700,
    width=800,
    color=median_salary_avg_exp['WorkExp'],  # Use average years of experience for color
    color_continuous_scale='viridis',  # Choose color scale
    color_continuous_midpoint=np.median(median_salary_avg_exp['WorkExp']),  # Set midpoint of color scale
    opacity=0.8,  # Set opacity
)

# Update traces
fig_salary_exp.update_traces(
    mode='markers',  # Set mode to markers
    marker=dict(
        symbol='circle',  # Set symbol to circle
        size=10,  # Set size of markers
        opacity=0.8,  # Set opacity
    ),
    textposition='top center',  # Set position of text
)

# Update layout
fig_salary_exp.update_layout(
    showlegend=False,  # Hide legend
    uniformtext_minsize=8,  # Set minimum font size for text
    uniformtext_mode='hide',  # Hide text if it doesn't fit
    yaxis=dict(
        title='Median Salary (USD)',
        showline=True,
        linecolor='white',  # White line color
        linewidth=2,
        range=[50000, 130000],  # Set x-axis range from 0 to 130000
        showgrid=True,  # Show grid
        gridcolor='rgba(128,128,128,0.2)',  # Set grid color
        gridwidth=0.2,  # Set grid width
        dtick = 10000,
    ),
    xaxis=dict(
        title='Average Years of Experience',
        showline=True,
        linecolor='white',  # White line color
        linewidth=2,
        range=[6, None],  # Set y-axis range from 6 to maximum
        showgrid=True,  # Show grid
        gridcolor='rgba(128,128,128,0.2)',  # Set grid color
        gridwidth=0.2,  # Set grid width
        dtick = 1,
    ),
    plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color
    paper_bgcolor='rgba(0,0,0,0)',  # Set paper background color
    margin=dict(l=50, r=50, t=50, b=50),  # Adjust margin
)

# Add devType label to each marker
for i, devtype in enumerate(median_salary_avg_exp['DevType']):
    fig_salary_exp.add_annotation(
        x=median_salary_avg_exp['WorkExp'][i],
        y=median_salary_avg_exp['ConvertedCompYearly'][i],
        text=devtype,
        showarrow=False,
        font=dict(color='white', size=8),
        align='center',
        yshift=10,
    )
# Show the plot
st.plotly_chart(fig_salary_exp)

st.markdown("<hr>", unsafe_allow_html=True)

# Group by programming languages and calculate the median salary and average years of experience
survey_df['Lang'] = survey_df['LanguageHaveWorkedWith'].str.split(';')
survey_df = survey_df.explode('Lang')
median_salary_avg_lang = survey_df.groupby('Lang').agg({'ConvertedCompYearly': 'median', 'WorkExp': 'mean'}).reset_index()

# Plot Scatter plot for median salary vs average years of experience by programming languages
fig_salary_lang = px.scatter(
    x=median_salary_avg_lang['WorkExp'],  # Average years of experience on x-axis
    y=median_salary_avg_lang['ConvertedCompYearly'],  # Median salary on y-axis
    text=median_salary_avg_lang['Lang'],  # Language as text
    labels={'x': 'Average Years of Experience', 'y': 'Median Salary'},
    title="Median Salary vs Average Years of Experience by Programming Languages",
    template="plotly_dark",  # Dark mode template
    height=700,
    width=800,
    color=median_salary_avg_lang['WorkExp'],  # Use average years of experience for color
    color_continuous_scale='viridis',  # Choose color scale
    color_continuous_midpoint=np.median(median_salary_avg_lang['WorkExp']),  # Set midpoint of color scale
    opacity=0.8,  # Set opacity
)

# Update traces
fig_salary_lang.update_traces(
    mode='markers',  # Set mode to markers
    marker=dict(
        symbol='circle',  # Set symbol to circle
        size=10,  # Set size of markers
        opacity=0.8,  # Set opacity
    ),
    textposition='top center',  # Set position of text
)

# Update layout
fig_salary_lang.update_layout(
    showlegend=False,  # Hide legend
    uniformtext_minsize=8,  # Set minimum font size for text
    uniformtext_mode='hide',  # Hide text if it doesn't fit
    yaxis=dict(
        title='Median Salary (USD)',
        showline=True,
        linecolor='white',  # White line color
        linewidth=2,
        range=[50000, 110000],  # Set y-axis range from 50000 to 130000
        showgrid=True,  # Show grid
        gridcolor='rgba(128,128,128,0.2)',  # Set grid color
        gridwidth=0.2,  # Set grid width
        dtick=10000,  # Set tick step
    ),
    xaxis=dict(
        title='Average Years of Experience',
        showline=True,
        linecolor='white',  # White line color
        linewidth=2,
        range=[8, 24],  # Set x-axis range from 0 to maximum
        showgrid=True,  # Show grid
        gridcolor='rgba(128,128,128,0.2)',  # Set grid color
        gridwidth=0.2,  # Set grid width
        dtick=1,  # Set tick step
    ),
    plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color
    paper_bgcolor='rgba(0,0,0,0)',  # Set paper background color
    margin=dict(l=50, r=50, t=50, b=50),  # Adjust margin
)

# Add language labels to each marker
for i, lang in enumerate(median_salary_avg_lang['Lang']):
    fig_salary_lang.add_annotation(
        x=median_salary_avg_lang['WorkExp'][i],
        y=median_salary_avg_lang['ConvertedCompYearly'][i],
        text=lang,
        showarrow=False,
        font=dict(color='white', size=8),
        align='center',
        yshift=10,
    )

# Show the plot
st.plotly_chart(fig_salary_lang)

st.markdown("<hr>", unsafe_allow_html=True)
# Plot Programming Languages Worked With and Want to Work With
st.subheader("Programming Languages Worked With and Want to Work With")
a = survey_df['LanguageHaveWorkedWith'].str.split(';').explode().value_counts()
b = survey_df['LanguageWantToWorkWith'].str.split(';').explode().value_counts()
combined_df = pd.concat([a, b], axis=1).fillna(0)
combined_df.columns = ['workedwith', 'wanttoworkwith']

fig_languages = px.bar(
    combined_df,
    x=combined_df.index,
    y=['workedwith', 'wanttoworkwith'],
    barmode='group',
    labels={'x': 'Programming Language', 'value': 'Count'},
    title="Programming Languages Worked With and Want to Work With",
    template="plotly_white",
    height=700,
    width=1000
)
fig_languages.update_traces(marker=dict(line=dict(width=1)))  # Adjust bar border width
fig_languages.update_layout(
    xaxis_showgrid=False,  # Hide x-axis grid lines
    yaxis_showgrid=True,  # Show y-axis grid lines
    uniformtext_minsize=8,  # Set minimum font size for text
    bargap=0.35
)
fig_languages.update_xaxes(tickangle=270, tickmode='linear', nticks=len(combined_df))
st.plotly_chart(fig_languages)

st.markdown("<hr>", unsafe_allow_html=True)
# Plot Platforms Worked With and Want to Work With
st.subheader("Platforms Worked With and Want to Work With")
a = survey_df['PlatformHaveWorkedWith'].str.split(';').explode().value_counts()
b = survey_df['PlatformWantToWorkWith'].str.split(';').explode().value_counts()
combined_platform_df = pd.concat([a, b], axis=1).fillna(0)
combined_platform_df.columns = ['workedwith', 'wanttoworkwith']

fig_platforms = px.bar(
    combined_platform_df,
    x=combined_platform_df.index,
    y=['workedwith', 'wanttoworkwith'],
    barmode='group',
    labels={'x': 'Platform', 'value': 'Count'},
    title="Platforms Worked With and Want to Work With",
    template="plotly_white",
    height=700,
    width=1000
)
fig_platforms.update_traces(marker=dict(line=dict(width=1)))  # Adjust bar border width
fig_platforms.update_layout(
    xaxis_showgrid=False,  # Hide x-axis grid lines
    yaxis_showgrid=True,  # Show y-axis grid lines
    uniformtext_minsize=8,  # Set minimum font size for text
    bargap=0.35
)
fig_platforms.update_xaxes(tickangle=270, tickmode='linear', nticks=len(combined_platform_df))
st.plotly_chart(fig_platforms)

 # type: ignore