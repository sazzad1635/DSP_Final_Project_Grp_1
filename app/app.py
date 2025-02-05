import streamlit as st
import pandas as pd
import joblib

# Title of the app
st.title('Fire Weather Index Prediction App')

# Sidebar inputs for user data
FFMC = st.sidebar.slider('Fine Fuel Moisture Code (FFMC)', 0.0, 100.0, 86.2)
DMC = st.sidebar.slider('Duff Moisture Code (DMC)', 0.0, 150.0, 26.2)
DC = st.sidebar.slider('Drought Code (DC)', 0.0, 800.0, 94.3)
ISI = st.sidebar.slider('Initial Spread Index (ISI)', 0.0, 50.0, 5.1)
Temperature = st.sidebar.slider('Temperature (°C)', -10.0, 50.0, 8.2)
RH = st.sidebar.slider('Relative Humidity (%)', 0, 100, 51)
Rain = st.sidebar.slider('Rain (mm)', 0.0, 10.0, 0.0)
Ws = st.sidebar.slider('Wind Speed (km/h)', 0.0, 30.0, 2.2)
Region = st.sidebar.selectbox('Region', ['Los Angels', 'California'])
BUI = st.sidebar.slider('Buildup Index (BUI)', 0.0, 100.0, 7.9)
Fire_Class = st.sidebar.selectbox('Fire Class', ['Not Fire', 'Fire'])

# Convert categorical variables to numeric values
region_mapping = {'Los Angels': 0, 'California': 1}
fire_class_mapping = {'Not Fire': 0, 'Fire': 1}

input_data = {
    'FFMC': FFMC,
    'DMC': DMC,
    'DC': DC,
    'ISI': ISI,
    'Temperature': Temperature,
    'RH': RH,
    'Rain': Rain,
    'Ws': Ws,
    'Region': region_mapping[Region],
    'BUI': BUI,
    'Classes': fire_class_mapping[Fire_Class]
}

# Convert input to DataFrame
input_df = pd.DataFrame([input_data])

# Load the trained model
model = joblib.load('../models/model_pipeline.pkl')

# Make prediction
def categorize_fwi(fwi):
    if fwi < 5.2:
        return "Very Low Danger"
    elif 5.2 <= fwi < 11.2:
        return "Low Danger"
    elif 11.2 <= fwi < 21.3:
        return "Moderate Danger"
    elif 21.3 <= fwi < 38.0:
        return "High Danger"
    elif 38.0 <= fwi < 50.0:
        return "Very High Danger"
    else:
        return "Extreme Danger"

if st.sidebar.button('Predict FWI'):
    prediction = model.predict(input_df)
    danger_level = categorize_fwi(prediction[0])
    
    # Display background image based on fire danger level
    if danger_level in ["High Danger", "Very High Danger", "Extreme Danger"]:
        bg_image = '\app\forest_fire.jpeg'  # Replace with the actual path to the fire forest image
    else:
        bg_image = '\app\normal_forest.jpg'  # Replace with the actual path to the normal forest image
    
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("{bg_image}");
        background-size: cover;
    }}
    </style>
    '''
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    st.write(f'### Predicted Fire Weather Index (FWI): {prediction[0]:.2f}')
    st.write(f'### Fire Danger Level: {danger_level}')
