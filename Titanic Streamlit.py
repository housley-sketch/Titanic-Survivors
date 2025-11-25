# streamlit_titanic_final.py
# python -m streamlit run "Streamlit Titanic dashboard.py"
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="R.M.S. Titanic", layout="centered")

# ────── DEEP-SEA SHIPWRECK BACKGROUND + PERFECT SCALING ──────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Alegreya+Sans+SC:wght@400;700&display=swap');

    /* Shipwreck background — only on the main page */
    html, body, .main, .stApp, [data-testid="stAppViewContainer"] {
        background: url('https://upload.wikimedia.org/wikipedia/commons/1/1b/Titanic_wreck_bow.jpg') no-repeat center center fixed !important;
        background-size: cover !important;
        background-color: #0b1d3d !important;
    }

    /* Gentle dark overlay so text is readable */
    .overlay {
        background: rgba(5, 20, 45, 0.82);
        position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;
    }

    /* Gold text for titles and labels */
    h1, .subtitle, [data-testid="stSidebar"] label, .stSlider label, footer p {
        color: #ffd700 !important;
        text-shadow: 0 0 12px rgba(255,215,0,0.7) !important;
    }

    h1 {
        font-family: 'Cinzel', serif; font-size: 4.2rem; text-align: center;
        background: linear-gradient(to right, #d4af37, #ffd700);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 20px 0 10px 0;
    }

    /* === DROPDOWNS: Gold border + dark readable background === */
    .stSelectbox > div > div > div:first-child {
        background: rgba(11, 26, 46, 0.97) !important;
        border: 3px solid #d4af37 !important;
        border-radius: 12px !important;
        box-shadow: 0 0 18px rgba(212,175,55,0.7) !important;
        color: #ffd700 !important;
    }

    /* Dropdown arrow */
    .stSelectbox svg {color: #ffd700 !important;}

    /* Dropdown menu items — THIS IS THE FIX */
    div[role="listbox"] div[role="option"] {
        background-color: #0f1e38 !important;
        color: #e8dccc !important;
        padding: 10px !important;
    }
    div[role="listbox"] div[role="option"]:hover {
        background-color: #1c4a7a !important;
        color: gray !important;
    }

    /* Age slider — glowing gold */
    .stSlider > div > div > div > div {
        background: linear-gradient(to right, #d4af37, #ffd700) !important;
        height: 10px !important;
        border-radius: 5px !important;
        box-shadow: 0 0 15px #ffd700 !important;
    }
    .stSlider > div > div > div[role="slider"] {
        background: #ffd700 !important;
        border: 3px solid #0b1d3d !important;
        box-shadow: 0 0 20px #ffd700 !important;
        width: 28px !important;
        height: 28px !important;
    }

    .stPlotlyChart {
        background: rgba(11,26,61,0.7) !important;
        border-radius: 20px;
        padding: 20px;
        border: 2px solid rgba(212,175,55,0.3);
    }
</style>
<div class="overlay"></div>
""", unsafe_allow_html=True)

# ────── SINKING ANIMATION ────── 
st.image("Titanic sinking.gif", use_column_width=True)

# ────── DATA ──────
@st.cache_data
def load_data():
    df = pd.read_csv("Titanic Age, Gender, Class CSV.csv")
    df = df[['Survived', 'Age', 'Sex', 'Pclass']].dropna(subset=['Age'])
    df.columns = ['Survived', 'Age', 'Sex', 'Class']
    df['Sex'] = df['Sex'].str.lower()
    return df

df = load_data()

# ────── SIDEBAR ──────
with st.sidebar:
    st.markdown("### Navigation")
    gender = st.selectbox("Souls", ["All Hands", "Gentlemen", "Ladies"])
    gender = {"Gentlemen":"male", "Ladies & Children":"female"}.get(gender)

    pclass = st.selectbox("Deck", ["All Decks", "1st Class", "2nd Class", "3rd Class"])
    pclass = int(pclass[0]) if pclass != "All Decks" else None

    age_range = st.slider("Age range", 0, 80, (0, 80), step=1)

# ────── FILTER ──────
f = df.copy()
if gender: f = f[f['Sex'] == gender]
if pclass: f = f[f['Class'] == pclass]
f = f[f['Age'].between(*age_range)]

saved = int(f['Survived'].sum())
perished = len(f) - saved
total = len(f)

# ────── PERFECTLY SIZED PIE CHART ──────
fig = px.pie(
    names=['Perished at Sea', 'Saved'],
    values=[perished, saved],
    hole=0.5,
    color_discrete_sequence=['#8b1a1a', '#ffd700']
)

fig.update_traces(
    textinfo='percent+value',
    textfont_size=22,
    textfont_color='white',
    marker=dict(line=dict(color='#d4af37', width=4))
)

fig.update_layout(
    height=680,                     # ← big, but not too big
    margin=dict(t=100, b=80, l=40, r=40),
    title=f"<b>{total:,} souls</b><br>Age {age_range[0]}–{age_range[1]} • {gender or 'All'} • Class {pclass or 'All'}",
    title_x=0.5,
    title_font=dict(size=22, family="Cinzel", color="#ffd700"),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(font=dict(size=18, color="#e8dccc"), orientation="h", y=-0.1),
    annotations=[dict(text=f"{saved}<br>saved", x=0.5, y=0.5, font_size=52, font_family="Cinzel", font_color="#ffd700", showarrow=False)]
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ────── FOOTER ──────
st.markdown("<p style='text-align:center; font-style:italic; margin-top:40px; color:#d4af37;'>"
            "“The sea keeps her own counsel.” – Captain Edward John Smith</p>", unsafe_allow_html=True)
