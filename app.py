import streamlit as st
import google.generativeai as genai

# ڕێکخستنی شێوەی پەڕەکە
st.set_page_config(page_title="Kurd Safety AI", page_icon="🛡️")
st.title("🛡️ Kurd Safety AI - HSE Expert Assistant")

# وەرگرتنی API Key لە سێرڤەرەوە
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ڕێنماییە سەرەکییەکان بۆ بۆتەکە (دەتوانیت لێرەدا ڕێنماییەکانت زیاد بکەیت)
sys_instruct = """
تۆ یاریدەدەرێکی زیرەکی دەستکردی بۆ بواری سەلامەتی پیشەیی (HSE) لە پلاتفۆرمی کورد سەیفتی.
وەڵامەکانت دەبێت خێرا، دروست و بە زمانی کوردی بن و پشت بە ستانداردەکانی وەک OSHA و NFPA ببەستن.
"""

# هەڵبژاردنی مۆدێلە خێراکە
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=sys_instruct)

# پاراستنی نامەکانی پێشوو بۆ ئەوەی ڕێستارت نەبێتەوە
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانی نامەکانی پێشوو لەسەر شاشەکە
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# وەرگرتنی پرسیاری نوێ لە بەکارهێنەرەوە
if prompt := st.chat_input("پرسیارەکەت دەربارەی سەلامەتی لێرە بنووسە..."):
    # نیشاندانی پرسیارەکە
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # وەرگرتن و نیشاندانی وەڵامی AI
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
