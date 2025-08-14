#!/bin/bash

# Script automatico per setup identificazione sviluppatori
echo "🚀 Setting up developer identification tools for Nino Medical AI..."

# 1. Crea directory per issue templates
echo "📁 Creating .github/ISSUE_TEMPLATE directory..."
mkdir -p .github/ISSUE_TEMPLATE

# 2. Crea issue template presentazioni
echo "📝 Creating presentation issue template..."
cat > .github/ISSUE_TEMPLATE/presentation.md << 'EOF'
---
name: 👋 Presentazione Sviluppatore
about: Presentati alla community Medical AI
title: '[PRESENTAZIONE] 👋 Ciao, sono [TUO NOME]'
labels: 'presentazione, community'
assignees: NinoF840
---

## 👋 Chi Sono

**Nome:** 
**Professione/Specializzazione:** 
**Ubicazione:** 
**GitHub:** @
**LinkedIn:** 

## 🏥 Il Mio Interesse per Medical AI

**Perché hai clonato il progetto?**


**Su cosa vorresti collaborare?**
- [ ] Algoritmi AI
- [ ] Interface/UX 
- [ ] Validazione medica
- [ ] Testing
- [ ] Documentazione
- [ ] Altro: ______

## 🚀 Idee/Feedback

**Cosa ti piacerebbe vedere nel progetto?**


**Hai esperienza con:**
- [ ] Python/Streamlit
- [ ] TensorFlow/PyTorch
- [ ] Settore medico/sanitario
- [ ] Database medici
- [ ] Clinical research

---
🎖️ **Grazie per unirti alla community Nino Medical AI!**
EOF

# 3. Crea issue template per bug report
echo "🐛 Creating bug report template..."
cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: 🐛 Bug Report
about: Segnala un bug per aiutarci a migliorare
title: '[BUG] '
labels: 'bug'
assignees: NinoF840
---

## 🐛 Descrizione del Bug
Descrizione chiara del problema riscontrato.

## 🔄 Per Riprodurre
Passi per riprodurre il comportamento:
1. Vai a '...'
2. Clicca su '....'
3. Vedi errore

## ✅ Comportamento Atteso
Descrizione di cosa ti aspettavi accadesse.

## 📱 Ambiente
- OS: [es. Windows 10]
- Browser: [es. Chrome, Firefox]
- Versione Python: [es. 3.11.7]

## 👤 Chi Sei (Opzionale)
Se vuoi, presentati! Aiuta a costruire la community.
- Nome/GitHub: 
- Specializzazione:
EOF

# 4. Crea issue template per feature request  
echo "💡 Creating feature request template..."
cat > .github/ISSUE_TEMPLATE/feature_request.md << 'EOF'
---
name: 💡 Feature Request
about: Suggerisci una nuova funzionalità
title: '[FEATURE] '
labels: 'enhancement'
assignees: NinoF840
---

## 💡 Funzionalità Richiesta
Descrizione chiara della funzionalità che vorresti.

## 🎯 Problema che Risolve
Spiega il problema che questa funzionalità risolverebbe.

## 🔧 Soluzione Proposta
Descrizione di come implementeresti questa funzionalità.

## 📋 Alternative Considerate
Altre soluzioni che hai considerato.

## 🏥 Contesto Medical AI
Come questa feature migliorerebbe l'esperienza medical AI?

## 👤 Chi Sei (Opzionale)
- Nome/GitHub: 
- Background: [es. Medico, Sviluppatore, Ricercatore]
- Interesse nel contribuire: [ ] Sì [ ] No
EOF

# 5. Aggiungi topics al repository (se gh CLI è disponibile)
if command -v gh &> /dev/null; then
    echo "🏷️ Adding repository topics..."
    gh repo edit --add-topic medical-ai 2>/dev/null || echo "⚠️ Failed to add medical-ai topic"
    gh repo edit --add-topic healthcare 2>/dev/null || echo "⚠️ Failed to add healthcare topic"
    gh repo edit --add-topic python 2>/dev/null || echo "⚠️ Failed to add python topic"
    gh repo edit --add-topic streamlit 2>/dev/null || echo "⚠️ Failed to add streamlit topic"
    gh repo edit --add-topic artificial-intelligence 2>/dev/null || echo "⚠️ Failed to add AI topic"
    
    # Prova ad attivare discussioni
    echo "💬 Trying to enable discussions..."
    gh repo edit --enable-discussions 2>/dev/null || echo "⚠️ Failed to enable discussions (might need manual activation)"
    
    echo "⭐ Repository topics and discussions configured!"
else
    echo "⚠️ GitHub CLI not found. Install 'gh' to auto-configure repository settings."
    echo "📋 Manual tasks:"
    echo "   - Add topics: medical-ai, healthcare, python, streamlit, artificial-intelligence"
    echo "   - Enable GitHub Discussions in repository settings"
fi

# 6. Crea README section per community engagement
echo "📄 Creating community engagement section for README..."
cat > community_section.md << 'EOF'

## 🌟 **Aiutaci a Crescere la Community Medical AI!**

### 👥 **Presentati alla Community**
Hai clonato il progetto? **Facci sapere chi sei!**
- 🌟 **[Metti una stella](https://github.com/NinoF840/curriculum-streamlit/stargazers)** se il progetto ti piace
- 👋 **[Presentati qui](https://github.com/NinoF840/curriculum-streamlit/issues/new?template=presentation.md)** - vogliamo conoscerti!
- 💼 **Collegati su LinkedIn**: [Antonino Piacenza](https://linkedin.com/in/antonino-piacenza)

### 🏆 **Hall of Fame - Primi Contributori**
I primi sviluppatori a contribuire riceveranno:
- ⭐ **Medical AI Pioneer Badge**
- 📧 **Riconoscimento LinkedIn pubblico**  
- 🎖️ **Sezione dedicata nel README**
- 💌 **Accesso anticipato alle nuove features**

### 🤝 **Come Contribuire**
| Tipo Contributo | Come Aiutare | Premio |
|------------------|--------------|---------|
| 🌟 **Prima Stella** | [Clicca qui](https://github.com/NinoF840/curriculum-streamlit/stargazers) | Pioneer Badge |
| 🐛 **Bug Report** | [Segnala qui](https://github.com/NinoF840/curriculum-streamlit/issues/new?template=bug_report.md) | Bug Hunter Badge |
| 💡 **Feature Idea** | [Proponi qui](https://github.com/NinoF840/curriculum-streamlit/issues/new?template=feature_request.md) | Innovator Badge |
| 👋 **Presentazione** | [Presentati qui](https://github.com/NinoF840/curriculum-streamlit/issues/new?template=presentation.md) | Community Member |

### 📧 **Resta Aggiornato**
**Newsletter Medical AI:** [📬 Iscriviti](mailto:ninomedical.ai@gmail.com?subject=Newsletter%20Signup&body=Nome:%20%0ASpecializzazione:%20%0AInteressi:%20)

---
**🔥 Stats Attuali: 25 cloni | 23 sviluppatori unici | Sii il primo a mettere una stella!**

EOF

# 7. Commit e push delle modifiche
if command -v git &> /dev/null; then
    echo "📤 Committing changes..."
    git add .github/
    git add community_section.md 2>/dev/null || true
    
    if git diff --staged --quiet; then
        echo "ℹ️ No changes to commit"
    else
        git commit -m "🚀 Add developer identification tools

- Added issue templates for presentations, bugs, features
- Configured repository for community engagement
- Added community section for README integration

Ref: developers_hunter_dashboard.py"
        
        echo "📤 Pushing to remote..."
        git push origin main 2>/dev/null || git push origin master 2>/dev/null || echo "⚠️ Push failed - check branch name and permissions"
    fi
else
    echo "⚠️ Git not found. Manual commit required."
fi

echo ""
echo "✅ Setup completato!"
echo ""
echo "📋 PROSSIMI PASSI MANUALI:"
echo "1. 📄 Aggiungi il contenuto di 'community_section.md' al tuo README.md"
echo "2. 🌐 Condividi il progetto su LinkedIn Medical AI groups"
echo "3. 📊 Implementa Google Analytics nell'app Streamlit"
echo "4. 📧 Configura newsletter signup form"
echo "5. 🎯 Identifica 5 sviluppatori target da contattare"
echo ""
echo "🎯 MONITORAGGIO:"
echo "   - Controlla issues per nuove presentazioni"
echo "   - Monitora stelle e fork"
echo "   - Esegui: streamlit run developers_hunter_dashboard.py"
echo ""
echo "🚀 Il tuo repository è ora configurato per identificare sviluppatori!"
