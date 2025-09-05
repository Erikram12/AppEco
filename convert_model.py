# Crear archivo: convert_model.py
import tensorflow as tf

# Cargar el modelo Keras
model = tf.keras.models.load_model('modelo/keras_model.h5')

# Convertir a TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Guardar el modelo convertido
with open('modelo/model.tflite', 'wb') as f:
    f.write(tflite_model)

print("✅ Modelo convertido a TensorFlow Lite")