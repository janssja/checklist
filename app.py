import os
import openai
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from helpers import send_email

load_dotenv()

logo = "Logo-Happy-2-Change.png.webp"
title = "Happy 2 Change Maturiteitsbeoordeling AI"

# secrets TOML
# Toegang krijgen tot de OpenAI API key
api_key_toml = st.secrets["OPENAI_API_KEY"]

# Toegang krijgen tot SMTP-instellingen
smtp_server_toml = st.secrets["smtp"]["server"]
smtp_port_toml = st.secrets["smtp"]["port"]
smtp_user_toml = st.secrets["smtp"]["user"]
smtp_password_toml = st.secrets["smtp"]["password"]

# Printen van de variabelen
print("API Key: ", api_key_toml)
print("SMTP Server: ", smtp_server_toml)
print("SMTP Port: ", smtp_port_toml)
print("SMTP User: ", smtp_user_toml)
print("SMTP Password: ", smtp_password_toml)

# Gebruik de omgevingsvariabelen
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = int(os.getenv('SMTP_PORT'))  # Zorg dat dit een integer is voor smtplib
smtp_user = os.getenv('SMTP_USER')
smtp_password = os.getenv('SMTP_PASSWORD')
test_mode = os.getenv('TEST')

smtp_server = smtp_server_toml
smtp_port = smtp_port_toml
smtp_user = smtp_user_toml
smtp_password = smtp_password_toml
api_key = api_key_toml

st.sidebar.image(logo, width=150)   
st.sidebar.title(title)
# api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

st.sidebar.title('Vul uw gegevens in')
st.sidebar.write('Enkel nodig als je het rapport ook per mail wilt ontvangen.')
organisation = st.sidebar.text_input('Organisatie:', key='organisation')
role = st.sidebar.text_input('Rol binnen de organisatie:', key='role')
user_email = st.sidebar.text_input('Uw e-mailadres:', key='user_email')

# Titel van de applicatie
st.title('AI Maturiteit Beoordeling')

# Introductie
st.write("""
Dit is een beoordelingstool om te helpen bepalen in welke fase van AI-maturiteit jouw organisatie zich momenteel bevindt. 
Beantwoord de volgende vragen op een schaal van 0 (helemaal niet akkoord) tot 5 (volledig akkoord).
""")

client = OpenAI(api_key=api_key)

# Lijst van vragen
vragen = [
    "Heeft je organisatie een overvloed aan data zonder een duidelijk plan voor gebruik?",
    "Is het managementteam op de hoogte van het belang van data voor de strategische besluitvorming?",
    "Worden verzamelde data momenteel gebruikt buiten reguliere rapportages om strategische inzichten te verkrijgen?",
    "Zijn er al successen geboekt met AI-projecten binnen de organisatie?",
    "Bestaat er een duidelijke visie en een specifiek team voor de implementatie van AI?",
    "Wordt data-analyse momenteel toegepast voor operationele inzichten in plaats van voor strategische besluitvorming?",
    "Is er een voorlopige roadmap of strategie voor de inzet van data en AI?",
    "Worden data-analyses uitgevoerd met een vaste structuur en methodologie?",
    "Beschikt het team over de noodzakelijke expertise om AI-projecten te leiden en uit te voeren?",
    "Zijn er voorbeelden van succesvolle AI-projecten die kunnen dienen als basis voor verdere ontwikkeling?",
    "Wordt er actief gewerkt aan het integreren van data uit verschillende bronnen?",
    "Bestaat er interesse binnen de organisatie om voorspellende analyses te gebruiken?",
    "Is er een strategisch plan voor het implementeren van AI-technologieën ter ondersteuning van organisatorische veranderingen?",
    "Zijn er toegewezen budgetten en partnerships voor AI-innovatie?",
    "Wordt binnen de organisatie gepleit voor een actievere benadering van AI zonder een specifiek plan?",
    "Zijn er 'data champions' of leiders binnen de organisatie die data-initiatieven promoten?",
    "Is de huidige infrastructuur van de organisatie geschikt om AI-technologieën te ondersteunen?",
    "Wordt er rekening gehouden met ethische overwegingen en het beheren van risico's bij AI-projecten?",
    "Voelen leidinggevenden de noodzaak om concurrentievoordelen te behalen door middel van data-analyse en AI?",
    "Zijn er duidelijke procedures en richtlijnen voor databeveiliging en privacy binnen AI-initiatieven?"
]

# Correspondentie tussen scores en tekst
antwoorden = {
    0: 'Helemaal niet akkoord',
    1: 'Niet akkoord',
    2: 'Enigszins niet akkoord',
    3: 'Enigszins akkoord',
    4: 'Akkoord',
    5: 'Helemaal akkoord'
}

# Maak sliders voor elke vraag en sla de scores op
scores = [st.slider(vraag, 0, 5, 0, key=vraag, help="0 = Helemaal niet akkoord, 5 = Helemaal akkoord") for vraag in vragen]

ai_usage = st.text_area("Beschrijf hoe AI momenteel wordt gebruikt binnen de verschillende afdelingen van uw organisatie.")

# Bronnen voor AI-gerelateerde kennis en opleiding
ai_resources = st.multiselect("Welke interne of externe bronnen gebruikt uw organisatie voor AI-gerelateerde kennis en opleiding?",
               ['Interne trainingen', 'Online cursussen', 'Conferenties', 'Academische publicaties', 'Andere'])

# ROI van AI-initiatieven
ai_roi = st.slider("Hoe beoordeelt uw organisatie de ROI van AI-initiatieven?", 0, 10, 5, help="0 = Niet beoordeeld, 10 = Uitgebreid beoordeeld")

# Barrières bij het implementeren van AI
ai_barriers = st.text_area("Beschrijf eventuele barrières die uw organisatie heeft ervaren bij het implementeren van AI.")

# Data-integriteit en -kwaliteit
data_integrity = st.radio("Hoe gaat uw organisatie om met data-integriteit en -kwaliteit?", ['Niet systematisch', 'Reactief', 'Proactief', 'Geavanceerd'])

# Gebruikte tools en platforms voor AI en data-analyse
ai_tools = st.text_area("Welke tools en platforms gebruikt uw organisatie momenteel voor AI en data-analyse?")

rapport_mail = ""
quick_wins_mail = ""
lange_termijn_mail = ""
actieplan_mail = ""

if st.button('Rapport en advies genereren'):
    with st.spinner('Bezig met het genereren van het rapport ...'):
        totaalscore = sum(scores)
        org_vragen = "\n".join([f"{vraag} : {antwoorden[score]}" for vraag, score in zip(vragen, scores)] +
                            [f"Beschrijf het AI-gebruik binnen uw organisatie: {ai_usage}",
                                f"Bronnen voor AI-kennis: {', '.join(ai_resources)}",
                                f"Beoordeling van ROI voor AI-initiatieven: {ai_roi}",
                                f"Barrières bij het implementeren van AI: {ai_barriers}",
                                f"Omgaan met data-integriteit: {data_integrity}",
                                f"Gebruikte AI-tools en platforms: {ai_tools}"])

        instructions = """
            Je bent een specialist in Kunstmatige Intelligentie en bent aangesteld om een uitgebreid rapport te schrijven over de AI-maturiteit 
            van een organisatie op basis van hun recent voltooide zelfevaluatie. De organisatie heeft de zelfbeoordelingsvragenlijst ingevuld, 
            waarbij elke vraag betrekking heeft op verschillende aspecten van AI-gebruik en -strategie. Het rapport is in het Nederlands en
            moet een overzicht geven van de huidige status van de organisatie met betrekking tot AI.

            Gebruik de informatie die verkregen is uit de zelfevaluatie om de organisatie te positioneren in één van de vijf fases van AI-maturiteit: 
            Bewustwordingsfase, Plantrekkingsfase, Experimenteringsfase, Industrialiseringsfase, Innovatiefase.

            Geef een algemeen overzicht van de huidige status van de organisatie met betrekking tot AI. 
            Identificeer specifieke sterke punten en verbeterpunten. Concentreer op het geven van heldere, beknopte analyses en aanbevelingen 
            zonder te herhalen wat al bekend is uit de antwoorden. Zorg voor een gestructureerd en logisch rapport dat de organisatie zal 
            helpen begrijpen hoe ze hun AI-capaciteiten kunnen verbeteren.
        """

        org_score = f""" Totaalscore : {totaalscore} """

        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": org_score},
                {"role":"user","content": f""" Graag een advies op basis van de score en deze antwoorden op de vragen: 
                    {org_vragen}"""},
            ],
        )

        output = completion.choices[0].message.content   

    st.write(output)
    rapport_mail = output
    print("**** Rapport klaar ****")
    print(rapport_mail[0:60])
    rapport = output
    print("*** ")

    st.subheader("Quick Wins")

    with st.spinner('Bezig met het genereren van het advies (deel Quick Wins)...'):

        instructions = """
            Gebaseerd op het AI Maturiteitsrapport en de zelfbeoordeling van de organisatie, ontwikkel je een uitgebreid advies voor de organisatie. 
            Dit advies moet gericht zijn op het helpen van de organisatie om naar de volgende fase van AI-maturiteit te evolueren. De adviezen moeten
            gericht zijn op het verbeteren van de AI-maturiteit van de organisatie op korte termijn en wordt daarom 'quick wins' genoemd.
            Maak gebruik van het Nederlandse taalmodel om dit advies te genereren.

            Focus op het identificeren van 'low hanging fruit' en 'quick wins' - gebieden waar de organisatie snel verbeteringen kan zien 
            met minimale investering of inspanning. Je houdt je in dit enkel bezig met de quick wins.

            Deze quick, wins moeten concreet en haalbaar zijn, met duidelijke stappen die de organisatie kan ondernemen.

            Zorg ervoor dat je aanbevelingen direct gekoppeld zijn aan de bevindingen uit het rapport en aansluiten bij de specifieke behoeften 
            en mogelijkheden van de organisatie. Benadruk hoe deze aanbevelingen de AI-maturiteit van de organisatie zullen verbeteren en bijdragen 
            aan hun algehele succes.
        """

        completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
            messages= [
                {"role": "system", "content": instructions},
                {"role": "user", "content": f""" Dit waren de antwoorden op de vragen: 
                    {org_vragen}"""},
                {"role":"user","content": f""" Graag een overzicht van quickwins op basis van de vragen en dit rapport. 
                    {rapport}"""},
            ],
        )

        quick_wins = completion.choices[0].message.content
        
    quick_wins_mail = quick_wins
    st.write(quick_wins)
    print("**** Quick Wins klaar ****")
    print(quick_wins[0:60])
    print("Rapport:", rapport_mail[0:60])
    print("**** Quick Wins klaar ****") 

    with st.spinner('Bezig met het genereren van het advies (Lange termijnstrategie)...'):

        instructions = """
            Gebaseerd op het AI Maturiteitsrapport en de zelfbeoordeling van de organisatie, ontwikkel je een uitgebreid en onderbouwd 
            advies voor de organisatie. 
            Dit uitgebreid en professioneel advies moet gericht zijn op het helpen van de organisatie om naar de volgende fase van 
            AI-maturiteit te evolueren. 
            Maak gebruik van het Nederlandse taalmodel om dit advies te genereren.

            Focus op het identificeren van de lange termijn strategie en de stappen die de organisatie moet nemen om de AI-maturiteit te verbeteren.

            Het advies moet onderbouwd, concreet en haalbaar zijn.

            Zorg ervoor dat je aanbevelingen direct gekoppeld zijn aan de bevindingen uit het rapport en aansluiten bij de specifieke behoeften 
            en mogelijkheden van de organisatie. Daar waar mogelijk bouw je verder op de quickwins.
            Benadruk hoe deze acties de AI-maturiteit van de organisatie zullen verbeteren en bijdragen aan hun algehele succes.
        """

        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
                messages= [
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": f""" Dit waren de antwoorden op de vragen: 
                        {org_vragen}"""},
                    {"role": "user", "content": f""" Dit zijn de quickwins op basis van de antwoorden op de vragen: 
                        {quick_wins}"""},
                    {"role":"user","content": f""" Graag een advies voor de lange termijn op basis van de vragen en dit rapport. 
                        {rapport}"""},
                ],
        )

        lange_termijn = completion.choices[0].message.content
        
    lange_termijn_mail = lange_termijn
    print("**** Lange termijn klaar ****")
    print(lange_termijn[0:60])
    print("Quick Wins:", quick_wins[0:60])
    print("Rapport:", rapport_mail[0:60])
    print("**** Lange termijn klaar ****")
    st.write(lange_termijn)

    with st.spinner('Bezig met het genereren van het actieplan...'):

        instructions = """
            Gebaseerd op het AI Maturiteitsrapport, een overzicht van quick wins en een lange termijnstrategie voor de organisatie,
            Creëer een je een zeer uitgebreid concreet, stap-voor-stap actieplan dat de organisatie kan volgen om de voorgestelde 
            Quick Wins en lange-termijnstrategieën te implementeren. 
            
            Dit plan moet duidelijke doelstellingen, tijdlijnen en toegewezen verantwoordelijkheden bevatten.
        """

        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
                messages= [
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": f""" Dit zijn de antwoorden uit zelfevaluatie: 
                        {org_vragen}"""},
                    {"role": "user", "content": f""" Dit zijn de quickwins op basis van de antwoorden op de vragen: 
                        {quick_wins}"""},
                    {"role": "user", "content": f""" Dit is de gedefinieerde lange termijnstrategie op basis van de antwoorden op de vragen: 
                        {lange_termijn}"""},
                    {"role":"user","content": f""" Graag een concreet actieplan op basis van deze input en dit rapport. 
                        {rapport}"""},
                ],
        )

        actieplan = completion.choices[0].message.content

    actieplan_mail = actieplan
    st.write(actieplan)


#    print("**** Actieplan klaar ****")
#    print(actieplan[0:60])
#    print("Lange Termijn:", lange_termijn[0:60])
#    print("Quick Wins:", quick_wins[0:60])
#    print("Rapport:", rapport_mail[0:60])
#    print("**** Actieplan klaar ****")

# generated_report = rapport_mail + quick_wins_mail + lange_termijn_mail + actieplan_mail
# print("Rapport klaar: ", generated_report[0:60])

# if user_email:
#    if st.button('Verstuur rapport per e-mail'):
#        try:    
#            print("Verzenden van e-mail naar: ", user_email)
#            send_email(user_email, generated_report, smtp_server, smtp_port, smtp_user, smtp_password)
#        except Exception as e:
#            st.error(f'Er is een fout opgetreden bij het verzenden van de e-mail: {e}')
# else:
#    st.warning('Vul je e-mailadres in om het rapport ook per e-mail te ontvangen.')
