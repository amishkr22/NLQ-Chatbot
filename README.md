# 📊 NLQ-Based Sales Insights Chatbot

### 🔹 **Natural Language Query (NLQ) Chatbot using RASA**
This chatbot is built using **RASA** and allows users to ask **sales-related queries** in natural language.  
It fetches **real-time sales insights** from structured datasets and responds dynamically.

---

## 🚀 **Features**
✅ **Sales Performance Analysis** – Compare sales across quarters.  
✅ **Top SKUs Contribution** – Find the highest revenue-generating products.  
✅ **Promotion Effectiveness** – Analyze the impact of discounts and offers.  
✅ **Retail & Channel Insights** – Compare revenue between regions and stores.  
✅ **Customer & Pricing Analysis** – Identify price-sensitive products.  
✅ **A/B Testing Simulations** – Predict the impact of pricing changes.  
✅ **Market Disruptions Simulations** – Model competitor activity or supply chain changes.  

---

## ⚙️ **Tech Stack**
- **RASA** – Conversational AI Framework  
- **Python** – Backend Logic  
- **Pandas** – Data Analysis  
- **NLU & NLG** – Natural Language Processing  
- **Sanic** – Action Server  
- **VS Code** – Development & Debugging  

---

## 📂 **Project Structure**
```bash
📁 NLQ Chatbot
│── 📂 data                 # Training data (nlu.yml, stories.yml)
│── 📂 models               # Trained RASA models
│── 📂 actions              # Custom action scripts (actions.py)
│── 📂 config               # RASA configuration files
│── 📂 tests                # Unit tests
│── endpoints.yml           # Action server endpoint
│── domain.yml              # Bot's domain (intents, responses, actions)
│── config.yml              # RASA pipeline settings
│── credentials.yml         # API credentials (if required)
│── README.md               # Documentation (You are here!)
```

---

## 🔧 **Installation & Setup**
### **1️⃣ Install Dependencies**
Make sure you have **Python 3.8+** installed. Then, install RASA:
```sh
pip install rasa
pip install rasa-sdk pandas
```

### **2️⃣ Clone the Repository**
```sh
git clone https://github.com/amishkr22/NLQ-Chatbot.git
cd nlq-chatbot
```

### **3️⃣ Train the Chatbot**
```sh
rasa train
```

### **4️⃣ Start the Action Server**
```sh
rasa run actions
```

### **5️⃣ Run the Chatbot**
```sh
rasa shell
```

Now, you can start chatting! Try:  
```sh
How did our total sales in Q4 compare to the previous quarter?
Show me the top 5 SKUs contributing to 80% of our revenue.
```

---