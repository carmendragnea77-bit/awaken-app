import streamlit as st
from openai import OpenAI
from duckduckgo_search import DDGS

st.set_page_config(page_title="The Awaken", layout="wide")
st.title("The Awaken: Verificator de Realitate")

st.sidebar.header("Setări")
mod = st.sidebar.radio("Alege varianta:", ["Gratuit (Căutare Web Inteligentă)", "Premium (OpenAI API)"])

api_key = ""
if mod == "Premium (OpenAI API)":
    api_key = st.sidebar.text_input("Introdu cheia ta OpenAI aici:", type="password")

text_verificat = st.text_area("Lipește știrea sau textul aici:")

if st.button("Verifică"):
    if not text_verificat:
        st.error("Scrie ceva în căsuță mai întâi!")
    else:
        st.write("Se analizează...")
        
        if mod == "Gratuit (Căutare Web Inteligentă)":
            try:
                # Extragem inteligent primele 6 cuvinte pentru a forma o căutare relevantă, nu o frază blocantă
                cuvinte = text_verificat.split()
                termen_cautare = " ".join(cuvinte[:6])
                
                with DDGS() as ddgs:
                    rezultate = list(ddgs.text(termen_cautare, max_results=3))
                    
                if rezultate:
                    st.success(f"Am căutat pe web subiectul: '{termen_cautare}...'")
                    for r in rezultate:
                        st.markdown(f"**[{r['title']}]({r['href']})**")
                        st.write(r['body'])
                        st.write("---")
                else:
                    st.warning("Nu am găsit rezultate clare. Încearcă să pui un titlu mai scurt sau folosește Premium.")
            except Exception as e:
                st.error(f"Eroare la căutarea gratuită: {e}")
                
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
