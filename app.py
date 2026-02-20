import streamlit as st
from openai import OpenAI
import wikipediaapi

st.set_page_config(page_title="The Awaken", layout="wide")
st.title("The Awaken: Verificator de Realitate")

st.sidebar.header("Setări")
mod = st.sidebar.radio("Alege varianta:", ["Gratuit (Wikipedia)", "Premium (OpenAI API)"])

api_key = ""
if mod == "Premium (OpenAI API)":
    api_key = st.sidebar.text_input("Introdu cheia ta OpenAI aici:", type="password")

text_verificat = st.text_area("Lipește știrea sau textul aici:")

if st.button("Verifică"):
    if not text_verificat:
        st.error("Scrie ceva în căsuță mai întâi!")
    else:
        st.write("Se analizează...")
        if mod == "Gratuit (Wikipedia)":
            wiki = wikipediaapi.Wikipedia('AwakenApp/1.0', 'ro')
            cuvinte = text_verificat.split()
            rezultat = wiki.page(cuvinte[0] if cuvinte else text_verificat)
            if rezultat.exists():
                st.success("Am găsit ceva pe Wikipedia!")
                st.write(rezultat.summary[:1000] + "...")
            else:
                st.warning("Nu am găsit date pe Wikipedia. Folosește varianta Premium.")
                
        elif mod == "Premium (OpenAI API)":
            if not api_key:
                st.error("Ai uitat să pui cheia API în stânga!")
            else:
                try:
                    client = OpenAI(api_key=api_key)
                    raspuns = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Verifică dacă textul e adevărat sau fals. Fii scurt și la obiect."},
                            {"role": "user", "content": text_verificat}
                        ]
                    )
                    st.success("Analiză Premium Gata!")
                    st.write(raspuns.choices[0].message.content)
                except Exception as e:
                    st.error(f"Eroare la cheia API: {e}")