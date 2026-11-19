/**
 * TERMINAL ENGINE MODULE
 * Provides an interactive developer console with real command processing.
 */

class TerminalEngine {
  constructor(outputElementId, inputElementId) {
    this.output = document.getElementById(outputElementId);
    this.input = document.getElementById(inputElementId);
    this.history = [];
    this.historyIndex = -1;

    this.commands = {
      help: () => this.cmdHelp(),
      bio: () => this.cmdBio(),
      skills: () => this.cmdSkills(),
      projects: () => this.cmdProjects(),
      pfe: () => this.cmdPfe(),
      status: () => this.cmdStatus(),
      contact: () => this.cmdContact(),
      'download-cv': () => this.cmdDownloadCv(),
      clear: () => this.cmdClear()
    };
  }

  init() {
    if (!this.input || !this.output) return;

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
        if (this.historyIndex > 0) {
          this.historyIndex--;
          this.input.value = this.history[this.historyIndex];
        }
      } else if (e.key === 'ArrowDown') {
        if (this.historyIndex < this.history.length - 1) {
          this.historyIndex++;
          this.input.value = this.history[this.historyIndex];
        } else {
          this.historyIndex = this.history.length;
          this.input.value = '';
        }
      }
    });

    // Initial greeting
    this.appendRaw(
      '<div class="terminal-line"><span style="color: #00e5ff; font-weight: 700;">➜ Anas Mouquine DevShell [v2.4.0]</span>' +
      '<span style="color: #94a3b8;">Tapez <code style="color: #10b981; font-weight: 600;">help</code> pour découvrir les commandes interactives disponibles.</span></div>'
    );
  }

  execute(rawCmd) {
    const parts = rawCmd.split(' ');
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
        `<div class="terminal-line" style="color: #ef4444;">Commande non reconnue: '${escapeHtml(commandName)}'. Tapez <strong>help</strong> pour l'aide.</div>`
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
      <div class="terminal-line" style="color: #cbd5e1; margin-top: 4px;">
        <span style="color: #00e5ff; font-weight: 700;">COMMANDES DISPONIBLES :</span><br>
        • <strong style="color: #10b981;">bio</strong>         : Profil académique & objectifs d'Anas Mouquine (EMSI)<br>
        • <strong style="color: #10b981;">skills</strong>      : Matrice des compétences en IA, Big Data et Génie Logiciel<br>
        • <strong style="color: #10b981;">projects</strong>    : Vue d'ensemble des 3 projets d'ingénierie majeurs<br>
        • <strong style="color: #10b981;">pfe</strong>         : Période et modalité du stage de fin d'études 2026<br>
        • <strong style="color: #10b981;">status</strong>      : État opérationnel du bot de chasse d'offres autonome<br>
        • <strong style="color: #10b981;">contact</strong>     : Liens directs LinkedIn, GitHub, Email et Téléphone<br>
        • <strong style="color: #10b981;">download-cv</strong> : Déclencher le téléchargement immédiat du CV ATS PDF<br>
        • <strong style="color: #10b981;">clear</strong>       : Nettoyer la console
      </div>
    `);
  }

  cmdBio() {
    this.appendRaw(`
      <div class="terminal-line" style="color: #cbd5e1;">
        <strong style="color: #00e5ff;">Anas MOUQUINE</strong> — Élève-Ingénieur 5ème Année<br>
        École Marocaine des Sciences de l'Ingénieur (EMSI), Casablanca<br>
        Spécialité : <span style="color: #6366f1;">Intelligence Artificielle & Génie des Données (IAGD)</span><br>
        Objectif : Stage PFE de 4 à 6 mois (2026) au Maroc ou à l'international.
      </div>
    `);
  }

  cmdSkills() {
    this.appendRaw(`
      <div class="terminal-line" style="color: #cbd5e1;">
        <span style="color: #00e5ff; font-weight: 700;">COMPÉTENCES TECHNIQUES :</span><br>
        • <strong>IA & LLM :</strong> RAG, Multi-Agents (LangChain), Prompt Engineering, PyTorch, Vector DBs<br>
        • <strong>Data Engineering :</strong> Apache Airflow, Kafka, Medallion Lakehouse, ETL/ELT, PostgreSQL, Neo4j<br>
        • <strong>Dev & Cloud :</strong> Python, FastAPI, Docker, CI/CD GitHub Actions, Linux, Flutter, React
      </div>
    `);
  }

  cmdProjects() {
    this.appendRaw(`
      <div class="terminal-line" style="color: #cbd5e1;">
        <span style="color: #00e5ff; font-weight: 700;">PROJETS PHARES :</span><br>
        1. <strong>Autonomous PFE Hunter Agent :</strong> Bot de veille multi-sources 24/7 avec qualification IA & GitHub Actions.<br>
        2. <strong>Enterprise Media Lakehouse :</strong> Architecture Medallion avec Apache Airflow, Kafka & Docker Compose.<br>
        3. <strong>Film-A Hybrid Recommender :</strong> Moteur de recommandation sémantique sur graphes Neo4j & LLM Gemini.
      </div>
    `);
  }

  cmdPfe() {
    this.appendRaw(`
      <div class="terminal-line" style="color: #10b981;">
        ✔ <strong>DISPONIBILITÉ PFE 2026 :</strong> 4 à 6 mois (Février / Juillet 2026)<br>
        Localisation : Casablanca, Rabat, Hybride ou Télétravail complet.<br>
        Conventionnement : EMSI Casablanca, Cycle Ingénieur d'État.
      </div>
    `);
  }

  cmdStatus() {
    const total = window.dataEngine?.stats.totalScraped || 100;
    this.appendRaw(`
      <div class="terminal-line" style="color: #cbd5e1;">
        <span style="color: #00e5ff; font-weight: 700;">STATUT SYSTÈME AGENT :</span><br>
        • Scrapers Actifs : 6 / 6 (DreamJob, LinkedIn Guest, ReKrute, Emploi.ma, MarocAnnonces, Talent)<br>
        • Offres Traitées : ${total} opportunités archivées<br>
        • Risque de Bannissement : 0.00% (Sessions publiques + rotation User-Agents)<br>
        • Mode Opérationnel : Production Continue via GitHub Actions Serverless
      </div>
    `);
  }

  cmdContact() {
    this.appendRaw(`
      <div class="terminal-line" style="color: #cbd5e1;">
        • Email : <a href="mailto:anasmouqine@gmail.com" target="_blank" style="color: #00e5ff;">anasmouqine@gmail.com</a><br>
        • Tél : +212 672-104126<br>
        • LinkedIn : <a href="https://www.linkedin.com/in/anas-mouqine-329207304/" target="_blank" style="color: #00e5ff;">linkedin.com/in/anas-mouqine</a><br>
        • GitHub : <a href="https://github.com/anasmouquinee" target="_blank" style="color: #00e5ff;">github.com/anasmouquinee</a>
      </div>
    `);
  }

  cmdDownloadCv() {
    this.appendRaw(`
      <div class="terminal-line" style="color: #10b981;">
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
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
