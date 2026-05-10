# 🤖 ML.Hub - freeCodeCamp Machine Learning Projects

A professional web interface showcasing Machine Learning models built for the freeCodeCamp "Machine Learning with Python" certification.

## 🚀 Projects Included
1. **✅ Neural Network SMS Text Classifier** (Spam Detector)
2. **⏳ Cat and Dog Image Classifier** (Coming Soon)
3. **⏳ Book Recommendation Engine** (Coming Soon)
4. **⏳ Health Costs Calculator** (Coming Soon)

## 🛠️ Technology Stack
- **Frontend**: HTML5, Vanilla CSS (Premium Dark Theme), JavaScript, Lucide Icons
- **Backend**: Python, Flask, Flask-CORS
- **Machine Learning**: TensorFlow, Keras, Pandas, NumPy

## 💻 How to Run Locally

If you want to test these AI models on your own machine, follow these steps:

### 1. Prerequisites
Make sure you have [Python](https://www.python.org/downloads/) installed on your computer.

### 2. Installation
Clone this repository or download the ZIP file, then open your terminal/PowerShell in the `backend` folder and install the required packages:
```bash
cd backend
pip install flask flask-cors tensorflow pandas numpy
```

### 3. Start the AI Server
Run the python backend:
```bash
python app.py
```
*(Note: On the first run, it will securely download the dataset and train the Neural Network automatically. This may take 1-2 minutes. Subsequent runs will be instant).*

### 4. Open the Interface
Once the terminal displays `Running on http://127.0.0.1:5000`, navigate to the `frontend` folder and double-click `index.html` to open it in any web browser. Type a message and analyze it!
