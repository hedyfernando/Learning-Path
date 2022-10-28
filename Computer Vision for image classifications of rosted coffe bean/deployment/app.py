#app.py 
import streamlit as st
import tensorflow as tf
import numpy as np
 
@st.cache(allow_output_mutation=True)
def load_model():
    model = tf.keras.models.load_model("model_improved_coffe.h5")
    return model
 
 
if __name__ == '__main__':
 
    model = load_model()
    st.title('Rosted Coffe Beans')
 
    uploaded_file = st.file_uploader('File uploader')
 
    if not uploaded_file:
        st.warning("Please upload an image before proceeding!")
        st.stop()
    else:
        # Decode Image and Predict Right Class
        image_as_bytes = uploaded_file.read()
        st.image(image_as_bytes, use_column_width=True)
        img = tf.io.decode_image(image_as_bytes, channels=3)
        img = tf.image.resize(img, (100, 100))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create a batch
 
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        image_class = str(predictions)
 
        st.title('Results')
 
        st.write("This image most likely belongs to with a percent confidence.",100 * np.max(score))
    