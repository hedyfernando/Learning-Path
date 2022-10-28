import streamlit as st
import pandas as pd
import pickle

model = pickle.load(open('bg_best.pkl','rb'))
scale = pickle.load(open('scaler_pipeline.pkl','rb'))

st.title('CHECK WATER QUALITY')

st.image('https://images.unsplash.com/photo-1606214554814-e8a9f97bdbb0?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8d2F0ZXIlMjBkcm9wfGVufDB8fDB8fA%3D%3D&w=1000&q=80')


ph = st.number_input('Masukkan nilai ph')
solids = st.number_input('Masukkan nilai solids')
chloramines = st.number_input('Masukkan nilai chloramines')
conductivity = st.number_input('Masukkan nilai conductivity')
organic_carbon = st.number_input('Masukkan nilai organic_carbon')
trihalomethanes = st.number_input('Masukkan nilai trihalomethanes')
turbidity = st.number_input('Masukkan nilai turbidity')


if st.button('Submit'):


    columns = ['ph','solids','chloramines','conductivity','organic_carbon','trihalomethanes','turbidity']

    X = pd.DataFrame([[ph,solids,chloramines,conductivity,organic_carbon,trihalomethanes,turbidity]], columns=columns)
    
    pred = model.predict(X)

    st.text(f'Water-Quality: {pred[0]}')

