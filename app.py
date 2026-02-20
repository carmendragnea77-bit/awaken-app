import streamlit as st
from openai import OpenAI
import requests

st.set_page_config(page_title="The Awaken", layout="wide")
st.title("The Awaken - Multisystem")
st.markdown("Arhitectura globală de verificare a realității.")

st.sidebar.header("Setări")
mod = st.sidebar.radio("Alege varianta:", ["Gratuit (Bază de Date Liberă)", "Premium (OpenAI API)"])

api_key = ""
if mod == "Premium (OpenAI API)":
    api_key = st.sidebar.text_input("Introdu cheia ta OpenAI aici:", type="password")

text_verificat = st.text_area("Lipește știrea sau textul aici:")

if st.button("Verifică"):
    if not text_verificat:
        st.error("Scrie ceva în căsuță mai întâi!")
    else:
        st.write("Se analizează...")
        
        if mod == "Gratuit (Bază de Date Liberă)":
            try:
                # Luăm primele 8 cuvinte
                cuvinte = text_verificat.split()
                termen_cautare = " ".join(cuvinte[:8])
                
                url = "https://ro.wikipedia.org/w/api.php"
                params = {
                    "action": "query",
                    "list": "search",
                    "srsearch": termen_cautare,
                    "utf8": "1",
                    "format": "json"
                }
                
                # REZOLVAREA: Cartea de vizită obligatorie pentru Wikipedia
                headers = {
                    "User-Agent": "TheAwakenMultisystem/1.0 (admin@awaken.ro)"
                }
                
                raspuns = requests.get(url, params=params, headers=headers)
                
                # Verificăm dacă Wikipedia ne-a răspuns cu succes (Cod 200)
                if raspuns.status_code == 200:
                    date = raspuns.json()
                    rezultate = date.get("query", {}).get("search", [])
                    
                    if rezultate:
                        st.success(f"Informații găsite pentru: '{termen_cautare}...'")
                        for r in rezultate[:3]:
                            snippet = r['snippet'].replace('<span class="searchmatch">', '**').replace('</span>', '**')
                            st.markdown(f"### [{r['title']}](https://ro.wikipedia.org/wiki/{r['title'].replace(' ', '_')})")
                            st.write(f"...{snippet}...")
                            st.write("---")
                    else:
                        st.warning("Nu am găsit informații în sursele libere pentru textul introdus.")
                else:
                    st.error(f"Eroare de conexiune la server. Cod: {raspuns.status_code}")
                    
            except Exception as e:
                st.error(f"Eroare tehnică: {e}")
                
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
