import streamlit as st
import pandas as pd
import numpy as np

st.title("STRAEM-LIT: Streamlit Application for Data Visualization")
st.write("This is a simple Streamlit application that allows you to visualize data using various libraries such as Pandas, NumPy, Matplotlib, and Plotly.")
st.text("You can upload your dataset and choose the type of visualization you want to create.")

st.text("Please upload your dataset (CSV format):")
uploaded_file = st.file_uploader("Choose a file")
button = st.button("Upload")

if button and uploaded_file is not None:
        st.success("File uploaded successfully!")
        df = pd.read_csv(uploaded_file)
        st.write(df)
elif button and uploaded_file is None:
        st.warning("Please upload a file to proceed.")

st.line_chart(np.random.randn(20, 3), use_container_width=True)
st.bar_chart(np.random.randn(20, 3), use_container_width=True)
st.area_chart(np.random.randn(20, 3), use_container_width=True)  
st.sidebar.title("Navigation")
st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)
st.video("https://youtu.be/9QXCkMTbrSk?si=nqklIrhhMEHiYTZT")
st.text_input("What is your name?")
st.text_area("write something ")
st.number_input("pick a number",min_value=0, max_value=100, value=100)
st.slider("choose a range", 0, 100)
st.selectbox("Select the fruit", ["Apple", "Banana", "Cherry"])
st.multiselect("Select your favorite colors", ["Red", "Green", "Blue", "Yellow"])
st.radio("pick one", ["Option 1", "Option 2"])
st.checkbox("I agree to the terms and conditions")
if st.checkbox("Show more detalis"):
        st.info("Here are more details about the application...")
option =st.radio("Choose View", ["show Chart", "Show Table"])
if option == "show Chart":
        st.write("Chart would be displayed here.")
elif option == "Show Table":
        st.write("Table would be displayed here.")
with st.form("my_form"):
       username=st.text_input("Username")
       password=st.text_input("Password", type="password")
       submit_button=st.form_submit_button("login")    
       
       if submit_button:
              st.success(f"Welcome, {username}!")