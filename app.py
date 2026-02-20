import streamlit as st
from openai import OpenAI
from googlesearch import search

st.set_page_config(page_title="The Awaken", layout="wide")
st.title("The Awaken - Multisystem")
st.markdown("Arhitectura globală de verificare a realității.")

st.sidebar.header("Setări")
mod = st.sidebar.radio("Alege varianta:", ["Gratuit (Google Search)", "Premium (OpenAI API)"])

api_key = ""
if mod == "Premium (OpenAI API)":
    api_key = st.sidebar.text_input("Introdu cheia ta OpenAI aici:", type="password")

text_verificat = st.text_area("Lipește știrea sau textul aici:")

if st.button("Verifică"):
    if not text_verificat:
        st.error("Scrie ceva în căsuță mai întâi!")
    else:
        st.write("Se analizează...")
        
        if mod == "Gratuit (Google Search)":
            try:
                # Extragem primele 8 cuvinte pentru o căutare logică pe Google
                cuvinte = text_verificat.split()
                termen_cautare = " ".join(cuvinte[:8])
                
                # Căutăm rezultatele direct
                rezultate = list(search(termen_cautare, num_results=3, advanced=True, lang="ro"))
                
                if rezultate:
                    st.success(f"Am căutat pe Google: '{termen_cautare}...'")
                    for r in rezultate:
                        st.markdown(f"**[{r.title}]({r.url})**")
                        st.write(r.description)
                        st.write("---")
                else:
                    st.warning("Nu am găsit rezultate. Încearcă o altă formulare.")
            except Exception as e:
                st.error(f"Eroare la conexiunea cu Google: {e}")
                
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
