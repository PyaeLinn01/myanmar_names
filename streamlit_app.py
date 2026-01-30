from pathlib import Path

import streamlit as st

from mm_names.convert import Converter

# Instantiate once to reuse dictionaries across interactions
converter = Converter()

st.set_page_config(
    page_title="Myanmar Name Converter",
    page_icon="🔤",
    layout="centered",
)

CUSTOM_STYLE = """
<style>
:root {
  --bg: radial-gradient(120% 120% at 20% 20%, #f3f1ff 0, #eef7ff 25%, #fdfdfd 60%);
  --panel: #ffffffea;
  --primary: #0f766e;
  --accent: #2563eb;
  --muted: #475569;
  --border: #e2e8f0;
  --radius: 12px;
  --shadow: 0 12px 35px rgba(15, 118, 110, 0.08);
  --font: "Space Grotesk", "Manrope", "Helvetica Neue", Arial, sans-serif;
}

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&display=swap');

body {
  background: var(--bg);
  font-family: var(--font);
}

.block-container {
  padding-top: 2rem;
  padding-bottom: 2.5rem;
}

.app-card {
  background: var(--panel);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  border-radius: var(--radius);
  padding: 1.25rem 1.5rem;
}

.stButton>button {
  background: linear-gradient(120deg, var(--primary), var(--accent));
  color: #f8fafc;
  border: none;
  border-radius: 999px;
  padding: 0.65rem 1.6rem;
  font-weight: 600;
  letter-spacing: 0.2px;
  box-shadow: 0 10px 30px rgba(37, 99, 235, 0.25);
}

.stButton>button:hover {
  filter: brightness(1.05);
}

.label-text {
  color: var(--muted);
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 0.35rem;
}

.result-box {
  background: #f8fafc;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  padding: 0.9rem 1rem;
  font-size: 1.05rem;
  font-weight: 600;
  color: #0f172a;
}

.helper {
  color: var(--muted);
  font-size: 0.88rem;
}
</style>
"""

st.markdown(CUSTOM_STYLE, unsafe_allow_html=True)

st.title("Myanmar → English Name Converter")
st.caption(
    "Convert Burmese names to English syllables using the project dictionary."
)

with st.sidebar:
    st.header("How it works")
    st.write(
        "We segment the Burmese name into syllables and map each syllable to an"
        " English equivalent from the provided dictionaries. Unmapped pieces are"
        " kept as-is."
    )
    st.markdown(
        "*Example Burmese input:* **မင်းခန့်မောင်မောင်** → **min khant maung maung**"
    )
    st.markdown("Data files live in `data/en2mm.json` and `data/mm2en.json`.")

with st.container():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)

    mm_input = st.text_area(
        "Burmese name",
        placeholder="မင်းခန့်မောင်မောင်" ,
        height=120,
    )

    submitted = st.button("Convert to English")

    if submitted:
        stripped = mm_input.strip()
        if not stripped:
            st.warning("Please enter a Burmese name to convert.")
        else:
            english = converter.mm2en(stripped)
            syls = converter.syl_break.syllable(stripped)

            st.markdown('<div class="label-text">Syllable segmentation</div>', unsafe_allow_html=True)
            st.markdown(f"<div class='result-box'>{syls}</div>", unsafe_allow_html=True)

            st.markdown('<div class="label-text" style="margin-top:0.75rem">English output</div>', unsafe_allow_html=True)
            st.markdown(f"<div class='result-box'>{english}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with st.expander("Need English → Burmese too?"):
    en_input = st.text_input("English name", placeholder="Min Khant Maung Maung")
    if st.button("Convert to Burmese"):
        en_stripped = en_input.strip()
        if not en_stripped:
            st.warning("Please enter an English name to convert.")
        else:
            mm_value = converter.en2mm(en_stripped)
            st.markdown('<div class="label-text">Burmese output</div>', unsafe_allow_html=True)
            st.markdown(f"<div class='result-box'>{mm_value}</div>", unsafe_allow_html=True)
