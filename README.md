🍅 Tomato Leaf Disease Detection System
A Streamlit-based web application that uses a TensorFlow deep learning model to detect diseases in tomato leaves from uploaded images. It also supports multi-language translation of results and provides a simple, interactive UI for farmers and researchers.

📌 Features
🔍 Detects tomato leaf diseases using a trained CNN model

🖼️ Upload and process leaf images via web interface

🌍 Translates disease names into local languages using Google Translator

📊 Displays model predictions with probabilities

💡 Suggests basic treatment tips (optional feature)

🧑‍🌾 Farmer-friendly design, accessible on mobile

🛠️ Tech Stack
Python 3.x

TensorFlow

Streamlit

Pandas & NumPy

Pillow (PIL)

deep-translator

Requests

📦 Installation
Clone the Repository

bash
Copy
Edit
git clone https://github.com/your-username/tomato-leaf-disease-detector.git
cd tomato-leaf-disease-detector
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the Streamlit App

bash
Copy
Edit
streamlit run app.py
🖼️ How to Use
Upload a clear image of a tomato leaf.

The model will analyze the image and detect any disease.

The result (e.g., Early Blight, Late Blight, Healthy) will be shown along with a translation option.

(Optional) Get basic remedies or suggestions.

📁 Folder Structure
bash
Copy
Edit
tomato-leaf-disease-detector/
├── app.py
├── model/                  # Trained model file (e.g., tomato_model.h5)
├── utils/                  # Helper functions (optional)
├── requirements.txt
└── README.md
🔬 Supported Diseases
Healthy

Early Blight

Late Blight

Leaf Mold

Bacterial Spot
(Add or modify based on your model)

🚀 Deployment
You can deploy this project to:

Streamlit Cloud

Render

Heroku
(Ask me if you need help with deployment setup)

👨‍💻 Authors:
O.Revanth raju
G.Sravani
D.Likitha
G.Deepika
