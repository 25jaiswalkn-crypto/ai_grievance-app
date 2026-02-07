import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime
from textblob import TextBlob
import plotly.express as px   
import folium 
from streamlit_folium import st_folium 

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="AI Grievance Redressal",
    page_icon="🏛️",
    layout="wide"
)

# ================== CUSTOM CSS ==================
st.markdown("""
<style>
body { background-color: #f6f8fc; }
.gov-icon {
    font-size: 80px;               
    color: #4a90e2;                
    background-color: #e6f0fa;     
    padding: 20px 25px;            
    border-radius: 50%;            
    box-shadow: 0 6px 18px rgba(0,0,0,0.2);  
    display: inline-block;        
    text-align: center;            
    margin-right: 15px;            
    vertical-align: middle;        
}
.main-title {
    font-size: 44px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #1e3c72, #2a5298);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sub-title {
    text-align: center;
    font-size: 18px;
    color: #555;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background: white;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.badge-high {color: white; background: #e74c3c; padding: 4px 10px; border-radius: 20px;}
.badge-medium {color: white; background: #f39c12; padding: 4px 10px; border-radius: 20px;}
.badge-low {color: white; background: #27ae60; padding: 4px 10px; border-radius: 20px;}
            
</style>
""", unsafe_allow_html=True)
 #---------------- SKY BLUE UI ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#dbeafe,#e0f2fe,#f0f9ff);
    font-family: 'Segoe UI', sans-serif;
}
h1,h2,h3 {color:#0c4a6e;font-weight:800;}
.stButton>button{
    background:linear-gradient(135deg,#38bdf8,#0284c7);
    color:white;font-weight:700;
    border-radius:999px;padding:0.6rem 1.8rem;
}
[data-testid="stTable"],[data-testid="stDataFrame"]{
    background:white;border-radius:14px;
}
footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ================== CONSTANTS ==================
DATA_FILE = "grievances.csv"

# ================== INIT DATA ==================
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=[
        "id","name","city","location","type","description",
        "department","sentiment","priority","status","created_at"
    ]).to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)
# ---------------- CITY DROPDOWN ----------------
city_list = [
    "Nagpur","Wardha","Jabalpur","Bhopal","Patna","Jamshedpur",
    "Solapur","Pune","Mumbai","Nashik","Aurangabad",
    "Indore","Gwalior","Ranchi","Gaya","Ahmedabad","Surat",
    "Bangalore","Mysore","Kolkata","Hyderabad","Delhi"
]
# ================== AI FUNCTIONS ==================
def analyze_sentiment(text):
    p = TextBlob(text).sentiment.polarity
    if p < -0.3:
        return "Negative 😠"
    elif p < 0.1:
        return "Neutral 😐"
    return "Positive 😊"

def detect_priority(text):
    t = text.lower()
    if any(w in t for w in ["urgent","danger","accident","death","fire"]):
        return "High 🔥"
    if any(w in t for w in ["delay","problem","not working"]):
        return "Medium ⚠️"
    return "Low 🟢"


def route_department(gtype):
    return {
         "Public Safety": "🚓 Police",
        "Sanitation": "🧹 Municipal",
        "Infrastructure": "🏗 PWD",
        "Healthcare": "🏥 Health Dept",
        "Utilities": "⚡ Electricity Board",
        "Education": "🎓 Education Dept",
        "Administrative Delay": "📂 General Admin",
        "Other": "📂 General Admin"

    }.get(gtype, "General Admin")

# ================== HEADER ==================
st.markdown("""
<div class="gov-icon">🏛️</div> 
""", unsafe_allow_html=True)
st.markdown('<div class="main-title">AI-Powered Grievance Redressal System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Smart Governance • NLP • Citizen-First Approach</div>', unsafe_allow_html=True)
st.write("")

# ================== LOGIN ==================
with st.container():
    col1, col2 = st.columns([2,1])
    role = col1.selectbox("Login Role", ["Citizen", "Admin"])
    password = col2.text_input("Password", type="password") if role == "Admin" else ""

if role == "Admin":
    if not password or password != os.getenv("ADMIN_PASS", "admin"):
        st.error("❌ Invalid admin password")
        st.stop()

df = load_data()

# ================== CITIZEN DASHBOARD ==================
if role == "Citizen":
    st.markdown("## 📨 Submit a Grievance")
    st.info("Fill out the form below to register your complaint.")

    with st.container():
        c1, c2, c3 = st.columns(3)
        name = c1.text_input("👤 Your Name", placeholder="Enter your full name")
        city = c2.text_input("🏙 City", placeholder="E.g., Delhi, Mumbai")
        location = c3.selectbox("📍 Area", ["Urban","Semi-Urban","Rural"], help="Select your locality type")

        gtype = st.selectbox(
            "🗂 Grievance Category",
            [
                "🚨 Public Safety","🗑 Sanitation","🏗 Infrastructure",
                "🏥 Healthcare","💡 Utilities","🏫 Education",
                "⌛ Administrative Delay","📝 Other"
            ],
            help="Choose the category that best fits your complaint"
        )

        description = st.text_area(
            "✏️ Describe your issue", height=120, 
            placeholder="Provide as many details as possible to help us address it efficiently"
        )

    if st.button("🚀 Analyze & Submit", use_container_width=True):
        if not description or not city:
            st.error("❗ City & description are required to submit a grievance")
        else:
            sid = str(uuid.uuid4())[:8]

            new = {
                "id": sid,
                "name": name or "Anonymous",
                "city": city,
                "location": location,
                "type": gtype,
                "description": description,
                "department": route_department(gtype),
                "sentiment": analyze_sentiment(description),
                "priority": detect_priority(description),
                "status": "Submitted",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

            df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
            save_data(df)

            st.success("✅ Grievance submitted successfully!")

            st.markdown("### 📊 AI Analysis")
            m1, m2, m3 = st.columns(3)

            # Add icons
            sentiment_icon = {"Positive":"😊","Neutral":"😐","Negative":"😠"}
            priority_icon = {"High":"🔴","Medium":"🟠","Low":"🟢"}

            m1.metric("Sentiment", f"{sentiment_icon[new['sentiment']]} {new['sentiment']}")
            m2.metric("Priority", f"{priority_icon[new['priority']]} {new['priority']}")
            m3.metric("Department", f"🏢 {new['department']}")

    st.markdown("## 🕒 Your Recent Complaints")
    st.info("Here are your last 5 submitted grievances.")
    st.dataframe(df[df["name"] == name].tail(5), use_container_width=True)

# ================== ADMIN DASHBOARD ==================
else:
    st.markdown("## 💻 Admin Dashboard")
    st.info("Monitor complaints, update status, and track department performance.")

    if df.empty:
        st.warning("No complaints available yet")
        st.stop()

    a1, a2, a3 = st.columns(3)
    a1.metric("📋 Total Complaints", len(df))
    a2.metric("✅ Resolved", len(df[df["status"]=="Resolved"]))
    a3.metric("⏳ Pending", len(df[df["status"]!="Resolved"]))

    st.divider()

    selected_id = st.selectbox("Select Complaint ID to view", df["id"].tolist(), help="Choose a complaint to view details or update status")
    selected = df[df["id"] == selected_id].iloc[0]

    st.markdown("### 📄 Complaint Details")
    st.write(selected)

    status_options = ["Submitted","In Progress","Resolved"]
    new_status = st.selectbox(
        "Update Status", status_options, 
        index=status_options.index(selected["status"]),
        help="Change the complaint status and save"
    )

    if st.button("💾 Save Status"):
        df.loc[df["id"] == selected_id, "status"] = new_status
        save_data(df)
        st.success(f"Status updated to **{new_status}**")

    st.divider()

    st.markdown("## 📈 Department Performance")
    chart = df.groupby("department").size().reset_index(name="count")
    fig = px.bar(
        chart, x="department", y="count", color="department",
        title="Number of Complaints per Department"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("## 🗺 City Heatmap")
    st.info("Circle size indicates the number of complaints reported from each city.")

    CITY_COORDS = {
        "Nagpur":[21.1458,79.0882],
        "Wardha":[20.7453,78.6022],
        "Jabalpur":[23.1815,79.9864],
        "Bhopal":[23.2599,77.4126],
        "Patna":[25.5941,85.1376],
        "Jamshedpur":[22.8046,86.2029],
        "Solapur":[17.6599,75.9064],
        "Pune":[18.5204,73.8567],
        "Mumbai":[19.0760,72.8777],
        "Nashik":[19.9975,73.7898],
        "Aurangabad":[19.8762,75.3433],
        "Indore":[22.7196,75.8577],
        "Gwalior":[26.2183,78.1828],
        "Ranchi":[23.3441,85.3096],
        "Gaya":[24.7914,85.0002],
        "Ahmedabad":[23.0225,72.5714],
        "Surat":[21.1702,72.8311],
        "Bangalore":[12.9716,77.5946],
        "Mysore":[12.2958,76.6394],
        "Kolkata":[22.5726,88.3639],
        "Hyderabad":[17.3850,78.4867],
        "Delhi":[28.6139,77.2090]
    }

    city_count = df.groupby("city").size().reset_index(name="count")
    m = folium.Map(location=[20.59, 78.96], zoom_start=5)

    for _, r in city_count.iterrows():
        folium.CircleMarker(
            location=CITY_COORDS.get(r["city"], [20.59, 78.96]),
            radius=5 + r["count"] * 2,
            popup=f"{r['city']} : {r['count']} complaints",
            color="#e74c3c",
            fill=True,
            fill_opacity=0.6
        ).add_to(m)

    st_folium(m, width=800)

st.caption("💡 Built with Streamlit • NLP • AI for Smart Governance")
