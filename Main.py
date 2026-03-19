import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO

# --- GEMINI API AYARI ---
# Buraya Google AI Studio'dan aldığın API Key'i yazmalısın
genai.configure(api_key="AIzaSyBV7utXd97uuMjdWwGzTFB_OeZCzz2lrUE")
model = genai.GenerativeModel('gemini-1.5-flash')

# Sayfa Genişliği ve Başlık
st.set_page_config(page_title="Dijital Kartvizit Oluşturucu", layout="wide")

st.title("📇 Akıllı Dijital Kartvizit")
st.write("Bilgilerini gir, yapay zeka senin için profesyonel bir profil oluştursun.")

# Arayüzü iki sütuna ayırıyoruz
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📝 Bilgilerini Doldur")
    isim = st.text_input("Ad Soyad", placeholder="Örn: Ahmet Yılmaz")
    unvan = st.text_input("Ünvan", placeholder="Örn: Bilgisayar Mühendisi")
    email = st.text_input("E-posta")
    telefon = st.text_input("Telefon")
    linkedin = st.text_input("LinkedIn Linki")
    yetenekler = st.text_area("Yeteneklerin / Hakkında", placeholder="Örn: Python, React, Siber Güvenlik...")

    # Gemini'den destek alma butonu
    ai_destegi = st.button("✨ Gemini ile Profesyonel Özet Yaz")

with col2:
    st.subheader("🖼️ Kartvizit Önizleme")

    hakkimda_metni = ""
    if ai_destegi:
        if yetenekler:
            with st.spinner("Gemini senin için yazıyor..."):
                prompt = f"{isim} için {unvan} pozisyonuna uygun, şu yetenekleri içeren: {yetenekler}, profesyonel ve kısa (max 2 cümle) bir kartvizit özeti yaz."
                response = model.generate_content(prompt)
                hakkimda_metni = response.text
        else:
            st.warning("Özet oluşturabilmem için 'Yetenekler' kısmını doldurmalısın.")

    # Modern HTML Kartvizit Tasarımı
    # Burada CSS kullanarak tasarımı dilediğin gibi özelleştirebilirsin
    kart_html = f"""
    <div style="
        border: 1px solid #ddd; 
        border-radius: 20px; 
        padding: 30px; 
        background: linear-gradient(135deg, #ffffff 0%, #f0f2f6 100%);
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333;
    ">
        <h2 style="color: #0e1117; margin-bottom: 5px;">{isim if isim else 'Ad Soyad'}</h2>
        <h5 style="color: #ff4b4b; margin-top: 0; font-weight: 400;">{unvan if unvan else 'Ünvan'}</h5>
        <hr style="border: 0.5px solid #ccc;">
        <p style="font-size: 14px; line-height: 1.6;">{hakkimda_metni}</p>
        <div style="font-size: 13px; margin-top: 15px;">
            <p><strong>📧 :</strong> {email}</p>
            <p><strong>📞 :</strong> {telefon}</p>
            <p><strong>🔗 :</strong> <a href="{linkedin}" style="color: #0077b5; text-decoration: none;">LinkedIn Profilim</a></p>
        </div>
    </div>
    """

    st.markdown(kart_html, unsafe_allow_html=True)

    # QR Kod Bölümü
    if isim and telefon:
        st.write("---")
        # vCard formatı: Telefon kamerasından okutulunca rehbere eklemeyi sağlar
        vcard_data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{isim}\nTEL:{telefon}\nEMAIL:{email}\nEND:VCARD"

        qr = qrcode.make(vcard_data)
        buf = BytesIO()
        qr.save(buf, format="PNG")

        st.image(buf, caption="Rehbere eklemek için QR kodu taratın", width=150)