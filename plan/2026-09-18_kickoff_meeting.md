# Project planning meeting 2026-09-18
This document is in Finnish.


## Osallistujat
- Aaron Haarti
- Antti "Hippe" Hippeläinen
- Mika Mäki


## Suunnitelma v1
- 2h + tauko + 2h workshop
  - 2 h perusteet
    - Myös demoja
  - 2 h kehittynyt (advanced)
    - Myös demoja
  - Tai eri päivinä?
- Livedemot hyviä
  - Harnessien tehokkuus
  - Integraatiot
- Läppärit mukaan
- LLM-pääsy
  - Kutsuviestiin vaihtoehdot:
      1) tarvitset subscriptionin johonkin maksulliseen AI:hin
      2) voit seurata
      3) jos on teknistä osaamista, niin voi ajaa paikallisia malleja
  - GitHub Education
    - Hakemus tulee lähettää hyvissä ajoin
    - [AI usage](https://github.com/settings/billing/ai_usage)
- Yleensä koulutukset tarjoavat laskentaresurssit
- Vaihtoehtoinen rakenne
  - Aloitetaan siitä, miten asennetaan
  - Tauon aikana voidaan käyttää 15 min debuggaamisiin ym.
- Claude for Science
  - Pro ilmainen, Max 5x (tai 6.25x) 20 €
  - Pitää tehdä hakemus ryhmälle
  - Ei ole mikään apurahahakemus, vaan lomake, joka tarvitsee täyttää


## Ajatuksia
- [Claude Team plan for scientists](https://support.claude.com/en/articles/16634237-claude-team-plan-for-scientists)
  - Hakemuksen tekijän on oltava PI (Principal Investigator)
  - Max. 25 hlö/hakemus
- IDE:nä VSCode
- [Verda](https://verda.com/)
	- Saattaa pystyä sponssaamaan OpenAI-yhteensopivan endpointin tmv.
	- Voisiko Claude Coden konffata käyttämään sitä?
- Aloitus: motivointi
- Miten käsitellä skeptisyyttä?
- Filosofiset keskustelut jätetään kahvitauolle ja workshopin jälkeen
- Moraaliset kysymykset
	- Minkä palveluntarjoajan työkaluja kannattaa käyttää?
- Alussa 0,5 - 1 h introa
	- Huomioidaan yleisöstä he, jotka eivät ole seuranneet viimeaikaista kehitystä
	- Ladotaan faktoja
	- Kerrotaan, mikä on tämänhetkinen tehokas käyttötapa
	- "Navier-Stokesia ei todistettu chatissa kyselemällä", vaan agenteilla
- Varoitus ennalta eksistentiaalisesta kriisistä
	- Mikä on ihmisen funktio, kun tekoäly ymmärtää fysiikan ihmistä paremmin?
	- Miten käyttää AI-työkaluja fiksusti eikä liikaa?
	- Myös negatiivisten puolien esittely antaa kredibiliteettiä
	- Kilpailu voi johtaa AI-pakotukseen tehokkuuden nimissä -> publish or perish -tyyppinen tilanne
- Pilviympäristöt
	- Mainitaan ennen paikallista harnessia, mutta todetaan, että paikallinen harness on parempi.
- Pyydetään esittämään kysymyksiä
	- Ns. tyhmät kysymykset on tärkeää kysyä
- Aaron saattaa alustavasti päästä vetämään esim. vartin demon
- Skillit, hookit, agentit
	- Demottava tarkasti ensimmäisen 2 h aikana


## Suunnitelma v2
- 2 + 2 h, tauko välissä
- Pohjustetaan infoviestissä, miten ottaa työkalut käyttöön
- Ensimmäiset 0,5 - 1 h teoriaa
  - Mitä tapahtunut viimeisten 2-3 h aikana
- 1 h perusdemoja
  - VSCode-plugarit (Antigravity + Codex ym. myös?)
  - Mitä ovat hookit ja skillit ym.
  - Miten käyttää harnessia
  - Miksi konteksti on niin keskeinen
- 0,5 - 1 h välein kysymyssessio
  - On tärkeää, että porukka kysyy kärryillä
- Toinen 2 h
  - Pitkälti demoja
  - 0,5 h kehittyneemmät ominaisuudet: skillit, hookit, agentit (advanced topics)
- 0,5 h demoja kultakin meistä
  - Hippe
    - Vapaa-ajan projekteja
    - Research loop
      - "Infinite for loop, kunnes tehtävä on tehty"
      - Fable orchestratorina
      - Käy research looppia läpi. Tekee kokonaisen research projektin. Inferraa Hipen tyylin vanhoista tiedostoista.
  - Mika
    - Paikalliset LLM-mallit
  - Aaron
    - Yhdistetty workflow, jollaista ei ole Hipellä tai Mikalla
    - Aaronin projektit
      - Doom Emacs -konffit
        - Clauden tekemät
      - Supertietokoneiden etäkäyttö
        - Claude omalla koneella -> ottaa SSH-yhteyden supertietokoneelle ja käynnistää Slurm-jobin
- Diat
  - Enemmän ensimmäiselle osuudelle
  - Tarvitaan, jotta tohtoriohjelma voi antaa opintopisteitä


## Ajatuksia
- GitHub-repo Mikan tilille
	- Aluksi private, myöhemmin public
	- ai-workshop
- Joonas pääasiallinen kontakti
	- Saattaa olla näkemystä alustavista suunnitelmistamme
	- Joonas haluaa opiskelijat mukaan
- Hippe käy USA:ssa 26.11.->
- Tavoiteajankohta marraskuun alku
	- Kakkosperiodin alkuun?
- A3 minikurssijulisteita
	- QR-koodi ja URL materiaaleihin
	- -> Motivoi ryhmänjohtajia ottamaan Claude for Scientistsin käyttöön
- Paras sali D101
	- Pystyy kiertelemään ihmisten joukossa
	- Kunnon näytöt joka kerroksessa
- Viestintäalusta
	- Telegram?
	- Zulip?
	- Mattermost-kanava
		- Tähän päädyttiin
