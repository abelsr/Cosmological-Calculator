import streamlit as st
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from functions import get_luminosity_distance

# Set page config
st.set_page_config(layout="wide", page_title="Cosmological Calculator")

# Title
st.title("Cosmological Calculator")

# Input fields

# REDSHIFT
z = st.number_input("Redshift (z)", min_value=0.0, value=0.0, step=0.01)

# HUBBLE CONSTANT (H_0)
h0 = st.number_input("Hubble Constant ($H_0$)", min_value=0.0, value=69.6, step=1.0)

# Lambda (Λ)
lambda_ = st.number_input("Lambda ($\lambda$)", min_value=0.0, value=0.714, step=0.1)

# MATTER DENSITY (Λ_m)
lambda_m = st.number_input("Matter Density ($\lambda_m$)", min_value=0.0, value=0.286, step=0.1)

# Calculate the distance
if st.button("Calculate"):
    res = get_luminosity_distance(redshift=z, h0=h0, omega_lambda=lambda_, omega_matter=lambda_m)
    res = pd.DataFrame(res, index=[0])
    st.write(res)
    
    
# Input field for the user to upload a file to the app
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# If the user uploads a file, read it and display it
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
    
# Select column to get redshift values
col = st.selectbox("Select column with redshift values", df.columns)

# If the user selects a column, show button to calculate distances
if col:
    if st.button("Calculate Distances"):
        res = [get_luminosity_distance(redshift=z, h0=h0, omega_lambda=lambda_, omega_matter=lambda_m) for z in df[col]]
        res = pd.DataFrame(res)
        st.write(res)