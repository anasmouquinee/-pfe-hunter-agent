/**
 * MAIN APP CONTROLLER
 * Orchestrates dual-mode switching, theme management, drawer flyouts, and event wiring.
 */

document.addEventListener('DOMContentLoaded', async () => {
  // 1. Initialize Theme (Dark Default or persisted in localStorage)
  initTheme();

  // 2. Initialize Data Engine
  await window.dataEngine.init();

  // 3. Update KPI Metrics in Mission Control
  renderKpis();

  // 4. Render Scraped Offers Table
  renderOffersTable();

  // 5. Setup Search and Filter Listeners
  setupFilterListeners();

  // 6. Setup Scoring Sandbox
  setupScoringSandbox();

  // 7. Setup Email Generator & Dry-Run Simulator
  setupEmailPreviewer();

  // 8. Initialize Interactive Terminal
  const term = new TerminalEngine('terminal-output', 'terminal-input');
  term.init();
  window.terminalInstance = term;

  // 9. Setup Dual-Mode Switcher
  setupModeSwitcher();

  // 10. Setup Drawer / Flyout Details
  setupDrawer();

  // 11. Read URL Hash for Initial Mode
  const currentHash = window.location.hash.replace('#', '');
  if (currentHash === 'portfolio') {
    switchMode('portfolio');
  } else {
    switchMode('mission-control');
  }
});

/* --------------------------------------------------------------------------
   THEME MANAGER
   -------------------------------------------------------------------------- */
function initTheme() {
  const savedTheme = localStorage.getItem('pfe_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);

  const themeBtn = document.getElementById('theme-toggle-btn');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('pfe_theme', next);
      updateThemeIcon(next);
      showToast('Thème mis à jour', `Mode ${next === 'dark' ? 'Cyber-Control sombre' : 'Executive clair'} activé.`);
    });
  }
}

function updateThemeIcon(theme) {
  const iconWrap = document.getElementById('theme-icon-wrap');
  if (!iconWrap) return;
  if (theme === 'dark') {
    iconWrap.innerHTML = `
      <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
      </svg>`;
  } else {
    iconWrap.innerHTML = `
      <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
      </svg>`;
  }
}

/* --------------------------------------------------------------------------
   DUAL-MODE SWITCHER (Mission Control vs Portfolio)
   -------------------------------------------------------------------------- */
function setupModeSwitcher() {
  const btnMission = document.getElementById('mode-btn-mission');
  const btnPortfolio = document.getElementById('mode-btn-portfolio');

  if (btnMission) {
    btnMission.addEventListener('click', () => switchMode('mission-control'));
  }
  if (btnPortfolio) {
    btnPortfolio.addEventListener('click', () => switchMode('portfolio'));
  }
}

function switchMode(mode) {
  const missionView = document.getElementById('view-mission-control');
  const portfolioView = document.getElementById('view-portfolio');
  const btnMission = document.getElementById('mode-btn-mission');
  const btnPortfolio = document.getElementById('mode-btn-portfolio');

  if (mode === 'portfolio') {
    missionView.classList.add('hidden');
    portfolioView.classList.remove('hidden');
    btnMission?.classList.remove('active');
    btnPortfolio?.classList.add('active');
    window.location.hash = 'portfolio';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } else {
    portfolioView.classList.add('hidden');
    missionView.classList.remove('hidden');
    btnPortfolio?.classList.remove('active');
    btnMission?.classList.add('active');
    window.location.hash = 'mission-control';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

/* --------------------------------------------------------------------------
   KPI METRICS RENDERING
   -------------------------------------------------------------------------- */
function renderKpis() {
  const stats = window.dataEngine.stats;
  const elTotal = document.getElementById('kpi-total-scraped');
  const elHighMatch = document.getElementById('kpi-high-match');
  const elRemunerated = document.getElementById('kpi-remunerated');
  const elDispatched = document.getElementById('kpi-dispatched');

  if (elTotal) elTotal.textContent = stats.totalScraped.toString();
  if (elHighMatch) elHighMatch.textContent = stats.highMatchCount.toString();
  if (elRemunerated) elRemunerated.textContent = stats.remuneratedCount.toString();
  if (elDispatched) elDispatched.textContent = stats.dispatchedCount.toString();
}

/* --------------------------------------------------------------------------
   OFFERS TABLE RENDERING & FILTERING
   -------------------------------------------------------------------------- */
function renderOffersTable() {
  const tbody = document.getElementById('offers-table-body');
  if (!tbody) return;

  const keyword = document.getElementById('search-offers-input')?.value || '';
  const source = document.getElementById('filter-source-select')?.value || 'all';
  const status = document.getElementById('filter-status-select')?.value || 'all';

  const filtered = window.dataEngine.filterOffers({ keyword, source, status });
  tbody.innerHTML = '';

  if (filtered.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5" style="text-align: center; padding: 32px; color: var(--text-muted);">
          Aucune offre ne correspond aux critères de recherche actuels.
        </td>
      </tr>
    `;
    return;
  }

  filtered.forEach(offer => {
    const tr = document.createElement('tr');
    tr.className = 'offer-row';
    tr.addEventListener('click', () => openOfferDrawer(offer.id));

    // Badge Source
    const sourceBadge = `<span class="badge badge-neutral">${offer.source.toUpperCase()}</span>`;

    // Status Badge
    let statusBadge = `<span class="badge badge-warning">EN ATTENTE</span>`;
    if (offer.applied) {
      statusBadge = `<span class="badge badge-success">DISPATCHÉ (DRY)</span>`;
    } else if (offer.is_remunerated) {
      statusBadge = `<span class="badge badge-cyan">RÉMUNÉRÉ</span>`;
    }

    // Score Color Fill
    let scoreColor = 'var(--status-danger)';
    if (offer.score >= 80) scoreColor = 'var(--status-success)';
    else if (offer.score >= 60) scoreColor = 'var(--status-warning)';

    tr.innerHTML = `
      <td class="offer-title-cell">
        <div class="offer-title-text">${escapeHtml(offer.title)}</div>
        <div class="offer-company-sub">${escapeHtml(offer.company)} · ${escapeHtml(offer.location)}</div>
      </td>
      <td>${sourceBadge}</td>
      <td>
        <div class="score-bar-wrapper">
          <div class="score-bar-track">
            <div class="score-bar-fill" style="width: ${offer.score}%; background-color: ${scoreColor};"></div>
          </div>
          <span class="score-num" style="color: ${scoreColor};">${offer.score}%</span>
        </div>
      </td>
      <td>${statusBadge}</td>
      <td style="text-align: right;">
        <button class="btn btn-outline btn-sm" onclick="event.stopPropagation(); openOfferDrawer('${offer.id}')">
          Examiner
        </button>
      </td>
    `;

    tbody.appendChild(tr);
  });

  const countBadge = document.getElementById('filtered-count-badge');
  if (countBadge) {
    countBadge.textContent = `${filtered.length} offre(s)`;
  }
}

function setupFilterListeners() {
  const searchInput = document.getElementById('search-offers-input');
  const sourceSelect = document.getElementById('filter-source-select');
  const statusSelect = document.getElementById('filter-status-select');
  const filterChips = document.querySelectorAll('.filter-chip');

  searchInput?.addEventListener('input', debounce(renderOffersTable, 200));
  sourceSelect?.addEventListener('change', renderOffersTable);
  statusSelect?.addEventListener('change', renderOffersTable);

  // Quick Filter Chips Handling
  filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      filterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');

      const filterType = chip.getAttribute('data-filter');
      if (filterType === 'all') {
        if (searchInput) searchInput.value = '';
        if (statusSelect) statusSelect.value = 'all';
        if (sourceSelect) sourceSelect.value = 'all';
      } else if (filterType === 'high_match') {
        if (statusSelect) statusSelect.value = 'high_match';
      } else if (filterType === 'remunerated') {
        if (statusSelect) statusSelect.value = 'remunerated';
      } else if (filterType === 'ai_rag') {
        if (searchInput) searchInput.value = 'RAG';
        if (statusSelect) statusSelect.value = 'all';
      } else if (filterType === 'lakehouse') {
        if (searchInput) searchInput.value = 'Lakehouse';
        if (statusSelect) statusSelect.value = 'all';
      } else if (filterType === 'airflow') {
        if (searchInput) searchInput.value = 'Airflow';
        if (statusSelect) statusSelect.value = 'all';
      }
      renderOffersTable();
    });
  });

  // Global Linear Keyboard Shortcut (Cmd+K / Ctrl+K or /)
  window.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      searchInput?.focus();
      searchInput?.select();
    } else if (e.key === '/' && document.activeElement !== searchInput && document.activeElement.tagName !== 'TEXTAREA') {
      e.preventDefault();
      searchInput?.focus();
    }
  });
}

/* --------------------------------------------------------------------------
   DRAWER / INSPECT DETAILS FLYOUT
   -------------------------------------------------------------------------- */
function setupDrawer() {
  const backdrop = document.getElementById('drawer-backdrop');
  const drawer = document.getElementById('drawer-flyout');
  const closeBtn = document.getElementById('drawer-close-btn');

  function close() {
    backdrop?.classList.remove('active');
    drawer?.classList.remove('active');
  }

  backdrop?.addEventListener('click', close);
  closeBtn?.addEventListener('click', close);
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') close();
  });
}

function openOfferDrawer(id) {
  const offer = window.dataEngine.getOfferById(id);
  if (!offer) return;

  const backdrop = document.getElementById('drawer-backdrop');
  const drawer = document.getElementById('drawer-flyout');

  // Populate drawer fields
  document.getElementById('drawer-offer-title').textContent = offer.title;
  document.getElementById('drawer-offer-company').textContent = `${offer.company} · ${offer.location}`;
  document.getElementById('drawer-offer-score').textContent = `${offer.score}%`;
  document.getElementById('drawer-offer-source').textContent = offer.source.toUpperCase();

  // Recruiter Intel
  const emailBox = document.getElementById('drawer-recruiter-email');
  if (offer.contact_email) {
    emailBox.innerHTML = `
      <a href="mailto:${offer.contact_email}" class="btn btn-primary btn-sm" target="_blank">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
        ${offer.contact_email}
      </a>`;
  } else {
    emailBox.innerHTML = `<span style="color: var(--text-muted); font-size: 13px;">Aucun email direct dans l'annonce publique</span>`;
  }

  const linkedinBox = document.getElementById('drawer-recruiter-linkedin');
  if (offer.hr_linkedin_url || offer.linkedin_url) {
    const targetUrl = offer.hr_linkedin_url || offer.linkedin_url;
    linkedinBox.innerHTML = `
      <a href="${targetUrl}" class="btn btn-outline btn-sm" target="_blank">
        <svg fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
        ${offer.hr_name ? `Contacter ${offer.hr_name}` : 'Voir Profil Recruteur'}
      </a>`;
  } else {
    linkedinBox.innerHTML = `<span style="color: var(--text-muted); font-size: 13px;">Profil LinkedIn personnel non indexé</span>`;
  }

  // Skills chips
  const skillsContainer = document.getElementById('drawer-skills-chips');
  skillsContainer.innerHTML = '';
  offer.matched_skills.forEach(skill => {
    const chip = document.createElement('span');
    chip.className = 'skill-chip skill-chip-detected';
    chip.textContent = skill;
    skillsContainer.appendChild(chip);
  });

  // Action Apply Preview in Drawer
  const previewBtn = document.getElementById('drawer-preview-application-btn');
  if (previewBtn) {
    previewBtn.onclick = () => {
      drawer?.classList.remove('active');
      backdrop?.classList.remove('active');
      loadOfferIntoEmailPreview(offer);
      document.getElementById('email-preview-section')?.scrollIntoView({ behavior: 'smooth' });
    };
  }

  backdrop?.classList.add('active');
  drawer?.classList.add('active');
}

/* --------------------------------------------------------------------------
   AI SCORING SANDBOX (PLAYGROUND)
   -------------------------------------------------------------------------- */
function setupScoringSandbox() {
  const textarea = document.getElementById('sandbox-input-textarea');
  const runBtn = document.getElementById('sandbox-run-btn');

  const presets = {
    pfe_ai: "Entreprise : AI Innovate Casablanca\nIntitulé : Stage PFE - Ingénieur RAG & Agents Autonomes\nMissions : Conception de pipelines RAG sémantiques avec LangChain, Python et FastAPI. Modélisation de bases vectorielles et benchmarks LLM. Stage de fin d'études conventionné rémunéré (gratification mensuelle).",
    data_lakehouse: "Entreprise : FinTech Services Maroc\nIntitulé : Stage PFE Data Engineer (Airflow / Kafka)\nProfil recherché : Élève-ingénieur en 5ème année. Maîtrise de Python, SQL, Apache Airflow (création de DAGs), ingestion temps réel avec Apache Kafka et conteneurisation Docker. Stage rémunéré pré-embauche.",
    senior_excluded: "Société : Global Consulting Rabat\nIntitulé : Lead Data Architect (CDI Confirmé - 7+ ans d'expérience)\nExigences : Minimum 7 ans d'ancienneté dans la gestion de clusters Hadoop/Spark. Encadrement d'équipe et direction technique.",
    homonym_ia: "Annonce : J'ai besoin d'un rédacteur web pour articles de blog généralistes. Télétravail occasionnel. Début immédiat."
  };

  // Wire preset buttons
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const key = btn.getAttribute('data-preset');
      if (presets[key] && textarea) {
        textarea.value = presets[key];
        runScoringEvaluation();
      }
    });
  });

  runBtn?.addEventListener('click', runScoringEvaluation);
}

function runScoringEvaluation() {
  const textarea = document.getElementById('sandbox-input-textarea');
  const text = textarea?.value || '';

  const result = window.scoringEngine.evaluateOfferText(text);

  // Update UI Result
  const scoreNum = document.getElementById('sandbox-score-number');
  const verdictBadge = document.getElementById('sandbox-verdict-badge');
  const reasoningText = document.getElementById('sandbox-reasoning-text');
  const detectedChips = document.getElementById('sandbox-detected-skills');
  const missingChips = document.getElementById('sandbox-missing-skills');
  const exclusionsBox = document.getElementById('sandbox-exclusions-list');

  if (scoreNum) scoreNum.textContent = result.score.toString();
  if (verdictBadge) {
    verdictBadge.textContent = result.verdict;
    verdictBadge.className = `badge ${result.badgeClass}`;
  }
  if (reasoningText) reasoningText.textContent = result.reasoning;

  if (detectedChips) {
    detectedChips.innerHTML = '';
    if (result.detectedSkills.length === 0) {
      detectedChips.innerHTML = '<span style="color: var(--text-muted); font-size: 12px;">Aucune compétence clé détectée</span>';
    } else {
      result.detectedSkills.forEach(skill => {
        const span = document.createElement('span');
        span.className = 'skill-chip skill-chip-detected';
        span.textContent = `✓ ${skill}`;
        detectedChips.appendChild(span);
      });
    }
  }

  if (missingChips) {
    missingChips.innerHTML = '';
    if (result.missingSkills.length === 0) {
      missingChips.innerHTML = '<span style="color: var(--text-muted); font-size: 12px;">Profil 100% complet</span>';
    } else {
      result.missingSkills.forEach(skill => {
        const span = document.createElement('span');
        span.className = 'skill-chip skill-chip-missing';
        span.textContent = `— ${skill}`;
        missingChips.appendChild(span);
      });
    }
  }

  if (exclusionsBox) {
    exclusionsBox.innerHTML = '';
    if (result.exclusions.length === 0) {
      exclusionsBox.innerHTML = '<span style="color: var(--status-success); font-size: 12px;">✓ Aucun facteur de blocage détecté</span>';
    } else {
      result.exclusions.forEach(exc => {
        const div = document.createElement('div');
        div.style.color = 'var(--status-danger)';
        div.style.fontSize = '12px';
        div.textContent = `⚠ ${exc}`;
        exclusionsBox.appendChild(div);
      });
    }
  }
}

/* --------------------------------------------------------------------------
   EMAIL GENERATOR & DRY-RUN PREVIEWER
   -------------------------------------------------------------------------- */
function setupEmailPreviewer() {
  const btnHtml = document.getElementById('tab-btn-html');
  const btnPlain = document.getElementById('tab-btn-plain');
  const htmlView = document.getElementById('email-html-view');
  const plainView = document.getElementById('email-plain-view');
  const dryRunBtn = document.getElementById('btn-dry-run-dispatch');

  btnHtml?.addEventListener('click', () => {
    btnHtml.classList.add('active');
    btnPlain?.classList.remove('active');
    htmlView?.classList.remove('hidden');
    plainView?.classList.add('hidden');
  });

  btnPlain?.addEventListener('click', () => {
    btnPlain.classList.add('active');
    btnHtml?.classList.remove('active');
    plainView?.classList.remove('hidden');
    htmlView?.classList.add('hidden');
  });

  dryRunBtn?.addEventListener('click', () => {
    showToast(
      'Simulation Dry-Run Réussie',
      'Candidature personnalisée préparée et consignée dans applied_offers.json (Aucun envoi réel en mode sécurisé).'
    );
  });
}

function loadOfferIntoEmailPreview(offer) {
  const companyEl = document.getElementById('email-preview-company');
  const subjectEl = document.getElementById('email-preview-subject');
  if (companyEl) companyEl.textContent = offer.company;
  if (subjectEl) subjectEl.textContent = `Candidature Stage PFE (IA & Data Engineering) – Anas MOUQUINE – ${offer.company}`;
  showToast('Candidature Générée', `Le modèle de courriel et le CV ATS ont été injectés pour ${offer.company}.`);
}

/* --------------------------------------------------------------------------
   TOAST NOTIFICATION HELPER
   -------------------------------------------------------------------------- */
function showToast(title, message) {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast active';
  toast.innerHTML = `
    <div class="toast-icon">
      <svg fill="none" viewBox="0 0 24 24" stroke="var(--accent-cyan)">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    </div>
    <div class="toast-content">
      <div class="toast-title">${escapeHtml(title)}</div>
      <div class="toast-message">${escapeHtml(message)}</div>
    </div>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.remove('active');
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function debounce(func, wait) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

function escapeHtml(str) {
  if (!str) return '';
  return str.toString()
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
