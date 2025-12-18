# Deploy Fonetizer till Streamlit Cloud

## Steg 1: Testa lokalt (valfritt)

Öppna terminal i Fonetizer-mappen:

```bash
streamlit run app.py
```

Appen öppnas på `http://localhost:8501`

---

## Steg 2: Pusha till GitHub

### 2.1 Skapa GitHub repo (om inte redan gjort)

1. Gå till [github.com](https://github.com)
2. Klicka "New repository"
3. Namn: `Fonetizer` (eller vad du vill)
4. Välj "Private" om du vill hålla det privat
5. Klicka "Create repository"

### 2.2 Pusha koden

I Fonetizer-mappen:

```bash
# Initiera git (om inte redan gjort)
git init

# Lägg till alla filer
git add .

# Committa
git commit -m "Add Streamlit app for Fonetizer"

# Länka till GitHub (ersätt USERNAME med ditt GitHub-användarnamn)
git remote add origin https://github.com/USERNAME/Fonetizer.git

# Pusha
git branch -M main
git push -u origin main
```

---

## Steg 3: Deploy till Streamlit Cloud

### 3.1 Logga in

1. Gå till [share.streamlit.io](https://share.streamlit.io)
2. Klicka "Sign in with GitHub"
3. Godkänn åtkomst

### 3.2 Deploy appen

1. Klicka "New app" eller "Deploy an app"
2. Fyll i:
   - **Repository:** `USERNAME/Fonetizer`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Klicka "Deploy!"

### 3.3 Vänta på deployment

Det tar ~2-3 minuter första gången. Du ser loggarna live.

---

## Steg 4: Dela länken! 🎉

När deployment är klar får du en länk som:

```
https://USERNAME-fonetizer.streamlit.app
```

**Dela denna länk med din kvartett!**

De kan:
- Öppna i mobilen → funkar direkt
- Lägga till på hemskärmen (ser ut som app)
- Bokmerka sidan

---

## Uppdatera appen

När du gör ändringar i koden:

```bash
git add .
git commit -m "Update app"
git push
```

Streamlit Cloud deployer automatiskt om några minuter!

---

## Felsökning

**Problem:** Appen startar inte
- Kolla att `requirements.txt` är med i repo
- Kolla logs på Streamlit Cloud

**Problem:** Git push fungerar inte
- Kolla att du har rätt remote: `git remote -v`
- Kan behöva authenticera med GitHub token

**Problem:** Vill göra repo privat
- Gå till GitHub → repo Settings → Change visibility → Private
- Appen fungerar fortfarande!

---

## Kostnad

**100% GRATIS** för offentliga appar!

För privata repos: Gratis för upp till 1 app.
