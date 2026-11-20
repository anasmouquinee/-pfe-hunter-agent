/**
 * TERMINAL ENGINE MODULE
 * Provides an interactive developer console with real command processing,
 * history navigation, Tab autocomplete, and semantic styling classes.
 */

class TerminalEngine {
  constructor(outputElementId, inputElementId) {
    this.output = document.getElementById(outputElementId);
    this.input = document.getElementById(inputElementId);
    this.history = [];
    this.historyIndex = -1;

    this.commands = {
      help: (args) => this.cmdHelp(args),
      bio: (args) => this.cmdBio(args),
      skills: (args) => this.cmdSkills(args),
      projects: (args) => this.cmdProjects(args),
      pfe: (args) => this.cmdPfe(args),
      status: (args) => this.cmdStatus(args),
      scrapers: (args) => this.cmdScrapers(args),
      offers: (args) => this.cmdOffers(args),
      certifs: (args) => this.cmdCertifs(args),
      theme: (args) => this.cmdTheme(args),
      mode: (args) => this.cmdMode(args),
      contact: (args) => this.cmdContact(args),
      'download-cv': (args) => this.cmdDownloadCv(args),
      clear: () => this.cmdClear()
    };
  }

  init() {
    if (!this.input || !this.output) return;

    // Command submission & keyboard navigation
    this.input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const cmd = this.input.value.trim();
        if (cmd) {
          this.execute(cmd);
          this.history.push(cmd);
          this.historyIndex = this.history.length;
          this.input.value = '';
        }
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (this.historyIndex > 0) {
          this.historyIndex--;
          this.input.value = this.history[this.historyIndex];
        }
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (this.historyIndex < this.history.length - 1) {
          this.historyIndex++;
          this.input.value = this.history[this.historyIndex];
        } else {
          this.historyIndex = this.history.length;
          this.input.value = '';
        }
      } else if (e.key === 'Tab') {
        e.preventDefault();
        this.handleAutocomplete();
      }
    });

    // Quick Command Bar Event Delegation
    const quickBar = document.getElementById('terminal-quick-bar');
    if (quickBar) {
      quickBar.addEventListener('click', (e) => {
        const btn = e.target.closest('.terminal-quick-btn');
        if (btn) {
          const cmd = btn.getAttribute('data-cmd');
          if (cmd) this.execute(cmd);
        }
      });
    }

    // Initial greeting
    this.appendRaw(
      '<div class="terminal-line"><span class="term-cyan" style="font-weight: 700;">➜ Anas Mouquine DevShell [v3.0.0]</span>' +
      '<span class="term-muted">Tapez <code class="term-success" style="font-weight: 600;">help</code> pour découvrir les commandes ou appuyez sur <code class="term-indigo">Tab</code> pour l\'autocomplétion.</span></div>'
    );
  }

  handleAutocomplete() {
    const val = this.input.value.trim().toLowerCase();
    const commandNames = Object.keys(this.commands);

    if (!val) {
      this.appendRaw(
        `<div class="terminal-line term-muted">Commandes disponibles : ${commandNames.join(', ')}</div>`
      );
      this.output.scrollTop = this.output.scrollHeight;
      return;
    }

    const matches = commandNames.filter(c => c.startsWith(val));
    if (matches.length === 1) {
      this.input.value = matches[0];
    } else if (matches.length > 1) {
      this.appendRaw(
        `<div class="terminal-line term-muted">Suggestions : ${matches.join(', ')}</div>`
      );
      this.output.scrollTop = this.output.scrollHeight;
      // Complete common prefix
      let prefix = val;
      for (let i = val.length; ; i++) {
        const char = matches[0][i];
        if (!char || !matches.every(m => m[i] === char)) break;
        prefix += char;
      }
      this.input.value = prefix;
    }
  }

  execute(rawCmd) {
    const parts = rawCmd.trim().split(/\s+/);
    const commandName = parts[0].toLowerCase();

    this.appendRaw(
      `<div class="terminal-line"><div class="terminal-prompt-row">` +
      `<span class="terminal-prompt-user">visitor@anas-mouquine</span>:<span class="terminal-prompt-path">~</span>$ ` +
      `<span>${escapeHtml(rawCmd)}</span></div></div>`
    );

    if (this.commands[commandName]) {
      this.commands[commandName](parts.slice(1));
    } else {
      this.appendRaw(
        `<div class="terminal-line term-danger">Commande non reconnue: '${escapeHtml(commandName)}'. Tapez <strong>help</strong> pour l'aide.</div>`
      );
    }

    this.output.scrollTop = this.output.scrollHeight;
  }

  appendRaw(htmlString) {
    const div = document.createElement('div');
    div.innerHTML = htmlString;
    while (div.firstChild) {
      this.output.appendChild(div.firstChild);
    }
  }

  cmdHelp() {
    this.appendRaw(`
      <div class="terminal-line term-muted" style="margin-top: 4px;">
        <span class="term-cyan" style="font-weight: 700;">COMMANDES DISPONIBLES :</span><br>
        • <strong class="term-success">bio</strong>         : Profil académique &amp; objectifs d'Anas Mouquine (EMSI)<br>
        • <strong class="term-success">skills</strong>      : Matrice des compétences en IA, Big Data et Génie Logiciel<br>
        • <strong class="term-success">projects</strong>    : Vue d'ensemble des 3 projets d'ingénierie majeurs<br>
        • <strong class="term-success">pfe</strong>         : Période et modalité du stage de fin d'études 2026<br>
        • <strong class="term-success">status</strong>      : État opérationnel du bot de veille autonome<br>
        • <strong class="term-success">scrapers</strong>    : Métriques temps réel des 6 portails d'emploi surveillés<br>
        • <strong class="term-success">offers</strong>      : Top des offres PFE hautement qualifiées (≥ 90%)<br>
        • <strong class="term-success">certifs</strong>     : Certifications industrielles validées (Google, HKUST, Meta)<br>
        • <strong class="term-success">theme [dark|light]</strong> : Basculer le mode d'affichage visuel<br>
        • <strong class="term-success">mode [mission|portfolio]</strong> : Basculer entre cockpit et vitrine<br>
        • <strong class="term-success">contact</strong>     : Liens directs LinkedIn, GitHub, Email et Téléphone<br>
        • <strong class="term-success">download-cv</strong> : Déclencher le téléchargement immédiat du CV ATS PDF<br>
        • <strong class="term-success">clear</strong>       : Nettoyer la console
      </div>
    `);
  }

  cmdBio() {
    this.appendRaw(`
      <div class="terminal-line term-muted">
        <strong class="term-cyan">Anas MOUQUINE</strong> — Élève-Ingénieur 5<sup>e</sup> Année<br>
        École Marocaine des Sciences de l'Ingénieur (EMSI), Casablanca<br>
        Spécialité : <span class="term-indigo">Intelligence Artificielle &amp; Génie des Données (IAGD)</span><br>
        Objectif : Stage PFE de 4 à 6 mois (Février – Juillet 2026) au Maroc ou à l'international.
      </div>
    `);
  }

  cmdSkills() {
    this.appendRaw(`
      <div class="terminal-line term-muted">
        <span class="term-cyan" style="font-weight: 700;">COMPÉTENCES TECHNIQUES :</span><br>
        • <strong>IA &amp; LLM :</strong> RAG, Multi-Agents (LangChain), Prompt Engineering, PyTorch, Vector DBs (Chroma/FAISS)<br>
        • <strong>Data Engineering :</strong> Apache Airflow, Apache Kafka, Medallion Lakehouse, ETL/ELT, PostgreSQL, Neo4j<br>
        • <strong>Dev &amp; Cloud :</strong> Python 3.11, FastAPI, Docker Compose, CI/CD GitHub Actions, Linux, React
      </div>
    `);
  }

  cmdProjects() {
    this.appendRaw(`
      <div class="terminal-line term-muted">
        <span class="term-cyan" style="font-weight: 700;">PROJETS PHARES :</span><br>
        1. <strong>Autonomous PFE Hunter Agent :</strong> Bot de veille multi-sources 24/7 avec qualification IA &amp; GitHub Actions.<br>
        2. <strong>Enterprise Media Lakehouse :</strong> Architecture Medallion avec Apache Airflow, Kafka &amp; Docker Compose.<br>
        3. <strong>Film-A Hybrid Recommender :</strong> Moteur de recommandation sémantique sur graphes Neo4j &amp; LLM Gemini.
      </div>
    `);
  }

  cmdPfe() {
    this.appendRaw(`
      <div class="terminal-line term-success">
        ✔ <strong>DISPONIBILITÉ PFE 2026 :</strong> 4 à 6 mois (Février / Juillet 2026)<br>
        Localisation : Casablanca, Rabat, Hybride ou Télétravail complet.<br>
        Conventionnement : EMSI Casablanca, Cycle Ingénieur d'État.
      </div>
    `);
  }

  cmdStatus() {
    const stats = window.dataEngine?.stats || { totalScraped: 370, highMatchCount: 71, remuneratedCount: 69, dispatchedCount: 153 };
    this.appendRaw(`
      <div class="terminal-line term-muted">
        <span class="term-cyan" style="font-weight: 700;">STATUT SYSTÈME AGENT :</span><br>
        • Scrapers Actifs : 6 / 6 (DreamJob, LinkedIn Guest, Joblia, Talent, ReKrute, MarocAnnonces)<br>
        • Offres Traitées : <strong class="term-cyan">${stats.totalScraped}</strong> opportunités archivées<br>
        • Match Élevé (≥ 80%) : <strong class="term-success">${stats.highMatchCount}</strong> opportunités hautement compatibles<br>
        • Candidatures Transmises : <strong class="term-indigo">${stats.dispatchedCount}</strong> candidatures préparées<br>
        • Taux de Blocage / Ban : 0.00% (Sessions publiques + rotation User-Agents)
      </div>
    `);
  }

  cmdScrapers() {
    const sources = window.dataEngine?.stats?.sourcesCount || { dreamjob: 159, linkedin_guest: 148, joblia: 34, talent: 14, rekrute: 8, marocannonces: 7 };
    this.appendRaw(`
      <div class="terminal-line term-muted">
        <span class="term-cyan" style="font-weight: 700;">MÉTRIQUES DES SCRAPERS :</span><br>
        • DreamJob.ma : <span class="term-success">${sources.dreamjob || 0} offres</span> (API REST &amp; pagination)<br>
        • LinkedIn Guest : <span class="term-success">${sources.linkedin_guest || 0} offres</span> (Endpoint public sans authentification)<br>
        • Joblia.ma : <span class="term-success">${sources.joblia || 0} offres</span> (Agrégateur offres tech)<br>
        • Talent.com : <span class="term-success">${sources.talent || 0} offres</span> (Flux agrégé Maroc)<br>
        • ReKrute.com : <span class="term-success">${sources.rekrute || 0} offres</span> (Sélecteurs CSS stricts)<br>
        • MarocAnnonces : <span class="term-success">${sources.marocannonces || 0} offres</span> (Extraction directe emails RH)
      </div>
    `);
  }

  cmdOffers() {
    const topOffers = (window.dataEngine?.offers || [])
      .filter(o => o.score >= 90)
      .slice(0, 5);

    if (topOffers.length === 0) {
      this.appendRaw('<div class="terminal-line term-muted">Chargement des offres en cours...</div>');
      return;
    }

    let html = `<div class="terminal-line term-muted"><span class="term-cyan" style="font-weight: 700;">TOP OFFRES PFE (MATCH ≥ 90%) :</span><br>`;
    topOffers.forEach((o, i) => {
      html += `${i + 1}. <strong class="term-primary">${escapeHtml(o.title)}</strong> chez <em>${escapeHtml(o.company)}</em> — <span class="term-success">${o.score}%</span> [${o.source}]<br>`;
    });
    html += '</div>';
    this.appendRaw(html);
  }

  cmdCertifs() {
    this.appendRaw(`
      <div class="terminal-line term-muted">
        <span class="term-cyan" style="font-weight: 700;">CERTIFICATIONS VÉRIFIÉES :</span><br>
        1. <strong>Google :</strong> Agile Project Management (ID: G2064X5FGLVB)<br>
        2. <strong>HKUST :</strong> Software Engineering Design (ID: PYISBTHNMK4R)<br>
        3. <strong>University of Michigan :</strong> Python Web Data &amp; REST APIs (ID: 3HIOWYMU2G7V)<br>
        4. <strong>EPFL :</strong> POO en C++ Mémoire &amp; Architecture (ID: 402FN9N1EN8K)<br>
        5. <strong>Meta :</strong> Advanced React Architecture (ID: EOQZZ5AJA4PN)
      </div>
    `);
  }

  cmdTheme(args) {
    const target = args[0]?.toLowerCase();
    if (target === 'light' || target === 'dark') {
      document.documentElement.setAttribute('data-theme', target);
      localStorage.setItem('pfe_theme', target);
      if (typeof updateThemeIcon === 'function') updateThemeIcon(target);
      this.appendRaw(`<div class="terminal-line term-success">Thème basculé vers: <strong>${target}</strong></div>`);
    } else {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      this.appendRaw(`<div class="terminal-line term-muted">Thème actuel: <strong>${current}</strong>. Usage: <code>theme dark</code> ou <code>theme light</code>.</div>`);
    }
  }

  cmdMode(args) {
    const target = args[0]?.toLowerCase();
    if (target === 'mission' || target === 'mission-control') {
      if (typeof switchMode === 'function') switchMode('mission-control');
      this.appendRaw(`<div class="terminal-line term-success">Navigation vers <strong>Mission Control</strong></div>`);
    } else if (target === 'portfolio') {
      if (typeof switchMode === 'function') switchMode('portfolio');
      this.appendRaw(`<div class="terminal-line term-success">Navigation vers <strong>AI Portfolio</strong></div>`);
    } else {
      this.appendRaw(`<div class="terminal-line term-muted">Usage: <code>mode mission</code> ou <code>mode portfolio</code>.</div>`);
    }
  }

  cmdContact() {
    this.appendRaw(`
      <div class="terminal-line term-muted">
        • Email : <a href="mailto:anasmouqine@gmail.com" target="_blank" class="term-cyan">anasmouqine@gmail.com</a><br>
        • Tél : +212 672-104126<br>
        • LinkedIn : <a href="https://www.linkedin.com/in/anas-mouqine-329207304/" target="_blank" class="term-cyan">linkedin.com/in/anas-mouqine</a><br>
        • GitHub : <a href="https://github.com/anasmouquinee" target="_blank" class="term-cyan">github.com/anasmouquinee</a>
      </div>
    `);
  }

  cmdDownloadCv() {
    this.appendRaw(`
      <div class="terminal-line term-success">
        ⚡ Téléchargement de cv_ats_pfe.pdf initié...
      </div>
    `);
    const link = document.createElement('a');
    link.href = 'cv_ats_pfe.pdf';
    link.download = 'Anas_Mouquine_CV_PFE.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  cmdClear() {
    this.output.innerHTML = '';
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return str.toString()
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}
