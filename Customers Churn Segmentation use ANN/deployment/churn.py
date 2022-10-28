import streamlit as st
import pandas as pd
import pickle
import tensorflow as tf
import numpy as np


fe = pickle.load(open('preprocess_model.pkl','rb'))
model = tf.keras.models.load_model('customer_churn_model.h5')

st.header('Churn Classifiers')

st.video('https://www.youtube.com/watch?v=l5ZYKdul6dI&ab_channel=StevenSoewignyo')

partner = st.selectbox('Apakah anda partner?', ['Yes','No'])
dependents = st.selectbox('Apakah anda bergantungan?', ['Yes','No'])
tenure = int(st.number_input('Masukkan lama berlangganan?'))
onlinesecurity = st.selectbox('Apakah anda berlangganan online security?', ['Yes','No','No internet service'])
onlinebackup = st.selectbox('Apakah anda berlangganan online backup?', ['Yes','No','No internet service'])
deviceprotection = st.selectbox('Apakah anda berlangganan device protection?', ['Yes','No','No internet service'])
techsupport = st.selectbox('Apakah anda berlangganan techsupport?', ['Yes','No','No internet service'])
contract = st.selectbox('Apa jenis contract anda?', ['Month-to-month','One year','Two year'])
paperlessbilling = st.selectbox('Tanpa kertas tagihan?', ['Yes','No'])
paymentmethod = st.selectbox('Metode pembayaran yang digunakan?', ['Electronic check','Mailed check','Bank transfer (automatic)','Credit card (automatic)'])
monthlycharges = st.number_input('Biaya bulanan?')
totalcharges = st.number_input('Total biaya berlangganan?')


# Churn or Not Churn

if st.button('Submit'):


    columns = ['partner', 'dependents', 'tenure', 'onlinesecurity', 'onlinebackup', 'deviceprotection', 'techsupport', 'contract', 'paperlessbilling', 'paymentmethod', 'monthlycharges', 'totalcharges']

    X = pd.DataFrame([[partner, dependents, tenure, onlinesecurity, onlinebackup, deviceprotection, techsupport, contract, paperlessbilling, paymentmethod, monthlycharges, totalcharges]], columns=columns)

    new_data = fe.transform(X)

    pred = model.predict(new_data)

    prediction = np.round_(pred)

    # Create prediction to new column
    predict_tar = pd.DataFrame(prediction, columns=['Prediction Churn'])

    # Concat between data inference with predix
    Pred_inf = pd.concat([predict_tar, X], axis=1)
    Pred_inf

    if pred == 1:
        st.text(f'Kamu termasuk Churn')
    else:
        st.text(f'Kamu tidak Churn')

