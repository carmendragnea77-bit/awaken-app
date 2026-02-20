import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import urllib.parse

st.set_page_config(page_title="The Awaken", layout="wide")
st.title("The Awaken: Verificator de Realitate")

st.sidebar.header("Setări")
mod = st.sidebar.radio("Alege varianta:", ["Gratuit (Căutare Web Liberă)", "Premium (OpenAI API)"])

api_key = ""
if mod == "Premium (OpenAI API)":
    api_key = st.sidebar.text_input("Introdu cheia ta OpenAI aici:", type="password")

text_verificat = st.text_area("Lipește știrea sau textul aici:")

if st.button("Verifică"):
    if not text_verificat:
        st.error("Scrie ceva în căsuță mai întâi!")
    else:
        st.write("Se analizează...")
        
        if mod == "Gratuit (Căutare Web Liberă)":
            try:
                # Extragem esența (primele 6 cuvinte) și le codăm pentru URL
                cuvinte = text_verificat.split()
                termen = " ".join(cuvinte[:6])
                termen_url = urllib.parse.quote_plus(termen)
                
                # Căutăm pe un motor care blochează mai greu cererile simple (DuckDuckGo formatat ca html)
                url = f"https://html.duckduckgo.com/html/?q={termen_url}"
                
                # Mimăm un browser uman (trecem de bariera de bază)
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }
                
                raspuns = requests.get(url, headers=headers)
                
                if raspuns.status_code == 200:
                    supa = BeautifulSoup(raspuns.text, 'html.parser')
                    rezultate_gasite = supa.find_all('a', class_='result__url', limit=3)
                    fragmente = supa.find_all('a', class_='result__snippet', limit=3)
                    
                    if rezultate_gasite and fragmente:
                        st.success(f"Căutare după: '{termen}...'")
                        for i in range(len(rezultate_gasite)):
                            link = rezultate_gasite[i].get('href')
                            text_snippet = fragmente[i].text.strip()
                            st.markdown(f"**[{link}]({link})**")
                            st.write(text_snippet)
                            st.write("---")
                    else:
                        st.warning("Motorul de căutare a returnat o pagină fără rezultate clare. Încearcă un text diferit.")
                else:
                    st.error(f"Eroare de conexiune la serverul de căutare (Cod: {raspuns.status_code}).")
                    
            except Exception as e:
                st.error(f"Eroare tehnică la căutarea gratuită: {e}")
                
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
