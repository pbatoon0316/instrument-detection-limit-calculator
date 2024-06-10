import streamlit as st
import pandas as pd
from scipy.stats import t

st.set_page_config(page_title='Instrument/Method Detection Limit Calculator',
                   page_icon='🔎', 
                   layout="centered")

###########
def normalize_data(input_values):
    # Normalize the string by replacing line breaks with commas
    normalized_data_string = input_values.replace('\n', ',').replace(' ',',')
    # Split the normalized string into a list of strings
    values_list = normalized_data_string.split(',')
    # Convert the list into a DataFrame
    df = pd.DataFrame(values_list, columns=['Response Values'])
    # Convert the string representations of numbers to actual numeric types
    df['Response Values'] = pd.to_numeric(df['Response Values'], errors='coerce')
    df = df.dropna().reset_index(drop=True)
    return df
###########

st.title('Instrument Detection Limit Calculator')
st.caption('Created by Patrick Batoon - https://www.linkedin.com/in/pbatoon')

input_values = st.text_area(label='Input Response (Signal Height/Area) :orange[_required_]', height=150)
df = normalize_data(input_values)
input1, input2 = st.columns(2)
with input1:
    input_oncolumn = st.number_input(label='Input Conc. or Amt. On-column :orange[_required_]', value=0, min_value=0)
with input2:
    input_conflevel = st.number_input(label='Confidence Level :orange[_(Default=0.99)_]', value=0.99)

###########
# Compute Statistics
###########
n = len(df)
dof = n-1
t_val = t.ppf(0.99, df=dof)
mean = df.mean()
stdev = df.std()
rsd = stdev/mean
if input_oncolumn==0:
    pass
else:
    idl = input_oncolumn * t_val * rsd

output1, output2 = st.columns([1,2])
with output1:
    st.dataframe(df)

with output2:
    st.markdown(body=f'''
        *n* = {n} \n
        *d.o.f.* = {dof} \n
        *t*-statistic (*t*) = {round(t_val,3)} \n
        Mean (*x̄*) = {round(stdev[0],3)} \n
        St.Dev (*s*) = {round(stdev[0],3)} \n
    ''')

    if input_oncolumn==0:
        pass
    else:
        st.divider()
        st.markdown(body=f'''
            #### Results:
            ##### IDL = ({input_oncolumn}) × ({round(t_val,3)}) × ({round(rsd[0],3)})
            ##### IDL = {round(idl[0],3)}
        ''')

    if rsd[0] < 0.1:
        st.markdown(body=':red[**Warning**: RSD is too low. Detection Limit is overly optimistic.]')
    elif rsd[0] > 0.5:
        st.markdown(body=':red[**Warning**: RSD is too high. Detection Limit is overly pessimistic.]')
    else:
        pass

#st.line_chart(data=df)
###########
# Overview
###########
st.divider()
st.markdown(body='''
            ### **Purpose:**

            This application was built to aid in the calculation of Instrument Detection Limit (IDL) or Method Detection Limit (MDL). Both values are obtained using the same calculation.

            ###### IDL or MDL = (Amt. On Column) × (_t_-statistic) × (RSD)

            - **Instrument Detection Limit (IDL)** is obtained with the sample analyte dissolved in neat solvent. This presumes that there will be no interference from components in the sample.
            - **Method Detection Limit (MDL)** is obtained in sample matrix and can contain a mixture of analytes.

            ### **Method/Instructions:** 
            
            When carrying out an IDL or MDL calculation, the series of response values should be obtained from replicate injections of known concentration or on-column amount.
            1. Aim for a reasonable Number of replicates (*n*), to obtain good statistics ~*n*=8 or more
                - Signal should also be relatively stable, meaning that there is no noticable upward or downward drift.
            2. The series of injections should be an RSD between 0.10 to 0.50. (Ideal = 0.20)
                - RSD values lower than 0.10 will produce an optimistic detection limit
                - RSD values higher than 0.50 wil produce a pessimistic detection limit
            3. By default the calculation is set up to use a confidence level of 99%, however other values can be used instead.
            4. Best results obtained when copy/pasted from spreadsheet program.''')

st.markdown(body='''
            
    ### References:
    If you're interested in the background to this topic, please feel free to check out the references below.

    - https://www.chromatographyonline.com/view/what-s-most-meaningful-standard-mass-spectrometry-instrument-detection-limit-or-signal-noise-ratio

    - https://www.epa.gov/cwa-methods/procedures-detection-and-quantitation-documents

    - https://www.agilent.com/en/support/liquid-chromatography-mass-spectrometry-lc-ms/instrument-detection-limit
''')



