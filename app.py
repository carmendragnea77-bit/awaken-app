import streamlit as st
from openai import OpenAI
from duckduckgo_search import DDGS

st.set_page_config(page_title="The Awaken", layout="wide")
st.title("The Awaken: Verificator de Realitate")

st.sidebar.header("Setări")
mod = st.sidebar.radio("Alege varianta:", ["Gratuit (AI Liber)", "Premium (OpenAI API)"])

api_key = ""
if mod == "Premium (OpenAI API)":
    api_key = st.sidebar.text_input("Introdu cheia ta OpenAI aici:", type="password")

text_verificat = st.text_area("Lipește știrea sau textul aici:")

if st.button("Verifică"):
    if not text_verificat:
        st.error("Scrie ceva în căsuță mai întâi!")
    else:
        st.write("Se analizează...")
        
        if mod == "Gratuit (AI Liber)":
            try:
                # Folosim motorul AI gratuit din DuckDuckGo pentru a analiza tot textul
                prompt = f"Acționează ca un expert în fact-checking. Verifică rapid dacă următoarea afirmație este adevărată, falsă sau o manipulare, aducând argumente scurte. Text: {text_verificat}"
                
                rezultat_ai = DDGS().chat(prompt)
                
                if rezultat_ai:
                    st.success("Analiză Gratuită Finalizată cu Succes!")
                    st.write(rezultat_ai)
                else:
                    st.warning("Serverul gratuit este aglomerat momentan. Mai apasă o dată butonul Verifică.")
            except Exception as e:
                st.error(f"Eroare la AI-ul gratuit (posibil prea multe accesări globale): {e}")
                
        elif mod == "Premium (OpenAI API)":
            if not api_key:
                st.error("Ai uitat să pui cheia API în meniul din stânga!")
            else:
                try:
                    client = OpenAI(api_key=api_key)
                    raspuns = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Verifică dacă textul următor e adevărat sau fals. Fii scurt, la obiect și adu argumente logice."},
                            {"role": "user", "content": text_verificat}
                        ]
                    )
                    st.success("Analiză Premium Finalizată!")
                    st.write(raspuns.choices[0].message.content)
                except Exception as e:
                    st.error(f"Eroare la cheia API: {e}")
