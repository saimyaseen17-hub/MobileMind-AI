# 📱 Mobile Mind AI

**Mobile Mind AI** is an AI-powered mobile phone search and recommendation system built with **Python, Pandas, NumPy, and Streamlit**.

It helps users find suitable mobile phones based on their **preferred company and budget**, and provides an AI-based recommendation using available mobile specifications.

## 🚀 Features

* 📱 Mobile phone search
* 🏢 Company/brand selection
* 💰 Price range filtering
* ⚡ Quick price filters
* 🤖 AI Best Choice recommendation
* 🧠 RAM comparison
* 💾 ROM/Storage information
* 🔋 Battery information
* 📱 Screen/Display information
* 🤳 Front camera information
* 📷 Back camera information
* 📡 Network technology information
* 📋 Complete mobile specifications
* 🔎 Detailed mobile information
* 📱 Responsive and professional UI

## 🤖 AI Recommendation

Mobile Mind AI uses an internal **weighted recommendation system** to rank mobiles according to available hardware specifications such as:

* RAM
* ROM/Storage
* Battery
* Screen size
* Front camera
* Back camera

The highest-ranked mobile is displayed as the **AI Best Choice**.

> Note: The recommendation system is a rule-based AI-style scoring system, not a trained machine-learning model.

## 🛠️ Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Regular Expressions
* HTML/CSS for UI styling

## 📂 Project Structure

```text
MobileMind-AI/
│
├── app.py
├── style.css
├── mobile_price_final_dataset.csv
├── requirements.txt
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/MobileMind-AI.git
```

Open the project folder:

```bash
cd MobileMind-AI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## 📊 Search Flow

```text
Select Company
      ↓
Select Price Range
      ↓
Matching Mobiles
      ↓
AI Best Choice
      ↓
View
```
