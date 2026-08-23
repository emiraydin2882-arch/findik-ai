import streamlit as st
from google import genai

st.set_page_config(page_title="Benim Gemini AI Sitem", page_icon="🤖")
st.title("🤖 Benim Gemini AI Asistanım")

# Arka planda gizli anahtarı otomatik kullan
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = None

if not api_key:
    st.error("⚠️ API Key bulunamadı! Lütfen Streamlit Secrets ayarlarına ekleyin.")
    st.stop()

# Sohbet gecmisi hafizasi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajlari goster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Kullanicidan soru alma
if prompt := st.chat_input("Gemini'a bir sey sor..."):
    if not api_key:
        st.error("Lutfen sol menudeki kutuya API Key'inizi yapistirin.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        try:
            client = genai.Client(api_key=api_key)
            with st.chat_message("assistant"):
                with st.spinner("Dusunuyor..."):
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt,
                    )
                    st.write(response.text)
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Hata olustu: {e}")


# (Kodun geri kalanı...)

# Kullanıcıdan Girdi Al ve Yanıtla kısmı bittikten sonra en alta:

if st.button("🗑️ Sohbeti Temizle"):
    st.session_state.messages = []
    st.rerun()
