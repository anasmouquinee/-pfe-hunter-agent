/**
 * SCORING ENGINE MODULE
 * Provides client-side AI & NLP matching simulation matching Anas Mouquine's profile.
 * Supports configurable category weights and missing skills detection.
 */

class ScoringEngine {
  constructor() {
    // Core profile target keywords for Anas Mouquine (EMSI Casablanca - IA & Data)
    this.targetSkills = [
      { name: 'Python', category: 'core', weight: 15 },
      { name: 'Intelligence Artificielle', aliases: ['ia', 'ai', 'artificial intelligence'], category: 'ai', weight: 15 },
      { name: 'Machine Learning', aliases: ['ml', 'deep learning', 'pytorch', 'tensorflow', 'scikit-learn'], category: 'ai', weight: 15 },
      { name: 'RAG & LLM', aliases: ['rag', 'llm', 'llms', 'langchain', 'prompt engineering', 'vector db'], category: 'ai', weight: 15 },
      { name: 'Data Engineering', aliases: ['etl', 'elt', 'pipeline', 'data pipeline'], category: 'data', weight: 15 },
      { name: 'Apache Airflow', aliases: ['airflow', 'dags'], category: 'data', weight: 12 },
      { name: 'Apache Kafka', aliases: ['kafka', 'streaming', 'real-time data'], category: 'data', weight: 10 },
      { name: 'Bases de Données (SQL / Neo4j)', aliases: ['sql', 'postgresql', 'neo4j', 'mysql', 'mongodb'], category: 'data', weight: 10 },
      { name: 'Docker & CI/CD', aliases: ['docker', 'github actions', 'ci/cd', 'linux'], category: 'devops', weight: 8 },
      { name: 'FastAPI / API REST', aliases: ['fastapi', 'rest api', 'api', 'flask'], category: 'backend', weight: 8 }
    ];

    // Seniority & Incompatibility exclusion terms
    this.exclusionPatterns = [
      { pattern: /\b(cdi|cdd)\s+(senior|confirm[eé]|expert|lead)\b/i, reason: 'Poste exigeant un profil Senior / Confirmé (Incompatible PFE)' },
      { pattern: /\b([5-9]|\d{2})\+?\s*(ans?|ann[eé]es?)\s+(d['\u2019]exp[eé]rience|d['\u2019]anciennet[eé])\b/i, reason: 'Expérience professionnelle minimale requise supérieure à 5 ans' },
      { pattern: /\b(directeur|manager|lead architect|head of)\b/i, reason: 'Intitulé de poste de management ou direction' },
      { pattern: /\bstage\s+(ouvrier|d['\u2019]observation|1[eè]re\s+ann[eé]e)\b/i, reason: 'Stage d\'initiation ou d\'observation (non éligible PFE 5ème année)' }
    ];

    // Remuneration indicators
    this.remunerationPatterns = [
      /\b(r[eé]mun[eé]r[eé]|gratifi[eé]|indemnit[eé]|prime\s+de\s+stage|salaire)\b/i
    ];
  }

  evaluateOfferText(text, weights = null) {
    if (!text || text.trim().length < 15) {
      return {
        score: 0,
        isEligible: false,
        detectedSkills: [],
        missingSkills: [],
        exclusions: ['Description de poste trop succincte pour une évaluation IA fiable'],
        isRemunerated: false,
        verdict: 'DONNÉES INSUFFISANTES',
        badgeClass: 'badge-danger',
        reasoning: 'Veuillez saisir un texte d\'offre ou coller une description complète pour déclencher l\'analyse.'
      };
    }

    const cleanText = text.toLowerCase();
    const exclusions = [];

    // 1. Verify Exclusion Rules
    for (const rule of this.exclusionPatterns) {
      if (rule.pattern.test(cleanText)) {
        exclusions.push(rule.reason);
      }
    }

    // 2. Check False-Positive Homonym: French "j'ai" vs "IA"
    const hasFalsePositiveIA = /\bj['\u2019]ai\b/i.test(cleanText) &&
      !/\bintelligence\s+artificielle\b/i.test(cleanText) &&
      !/\b(machine\s+learning|python|llm|deep\s+learning)\b/i.test(cleanText);

    if (hasFalsePositiveIA) {
      exclusions.push('Détection de faux-positif linguistique : présence de la forme verbale "j\'ai" confondue avec le sigle IA');
    }

    // 3. Detect Skills & Calculate Match Score with Configurable Weights
    const detectedSkills = [];
    const missingSkills = [];
    let earnedWeight = 0;
    let maxWeight = 0;

    for (const skill of this.targetSkills) {
      // Determine multiplier based on passed custom weights
      let multiplier = 1.0;
      if (weights) {
        if (typeof weights[skill.category] === 'number') {
          multiplier = weights[skill.category];
        } else if (typeof weights[skill.name] === 'number') {
          multiplier = weights[skill.name];
        }
      }

      const activeWeight = skill.weight * multiplier;
      maxWeight += activeWeight;
      let matched = false;

      // Check primary name
      if (cleanText.includes(skill.name.toLowerCase())) {
        matched = true;
      } else if (skill.aliases) {
        // Check aliases with regex word boundary
        for (const alias of skill.aliases) {
          const regex = new RegExp(`\\b${alias}\\b`, 'i');
          if (regex.test(cleanText)) {
            matched = true;
            break;
          }
        }
      }

      if (matched) {
        detectedSkills.push(skill.name);
        earnedWeight += activeWeight;
      } else {
        missingSkills.push(skill.name);
      }
    }

    // Baseline stage bonus if explicitly mentions PFE or stage fin d'études
    const isPfeMentioned = /\b(pfe|stage\s+de\s+fin\s+d['\u2019][eé]tudes?|stagiaire\s+pfe)\b/i.test(cleanText);
    let rawScore = maxWeight > 0 ? Math.round((earnedWeight / maxWeight) * 100) : 0;

    if (isPfeMentioned) rawScore = Math.min(100, rawScore + 10);
    const isRemunerated = this.remunerationPatterns.some(p => p.test(cleanText));
    if (isRemunerated) rawScore = Math.min(100, rawScore + 5);

    // If exclusions triggered, clamp score
    let finalScore = rawScore;
    let isEligible = true;
    let verdict = 'QUALIFIÉ POUR CANDIDATURE PFE';
    let badgeClass = 'badge-success';

    if (exclusions.length > 0) {
      finalScore = Math.min(35, rawScore);
      isEligible = false;
      verdict = 'REJET AUTOMATIQUE - CRITÈRES NON RESPECTÉS';
      badgeClass = 'badge-danger';
    } else if (finalScore < 50) {
      isEligible = false;
      verdict = 'FAIBLE CORRESPONDANCE TECHNIQUE';
      badgeClass = 'badge-warning';
    } else if (finalScore >= 80) {
      verdict = 'CANDIDATURE PRIORITAIRE - MATCH ÉLEVÉ';
      badgeClass = 'badge-cyan';
    }

    // Generate Explanatory Reasoning
    let reasoning = '';
    if (!isEligible) {
      reasoning = `L'offre a été écartée car elle présente ${exclusions.length} motif(s) d'exclusion bloquant(s) : ${exclusions.join(' ; ')}. Le bot protège votre temps et votre réputation en évitant d'y candidater.`;
    } else {
      reasoning = `L'offre correspond à ${finalScore}% aux compétences cibles d'Anas Mouquine. Les technologies requises (${detectedSkills.slice(0, 4).join(', ')}) s'alignent parfaitement avec la formation IA & Data Engineering de l'EMSI. Recommandation : expédition de candidature personnalisée avec cv_ats_pfe.pdf.`;
    }

    return {
      score: finalScore,
      isEligible: isEligible,
      detectedSkills: detectedSkills,
      missingSkills: missingSkills,
      exclusions: exclusions,
      isRemunerated: isRemunerated,
      isPfe: isPfeMentioned,
      verdict: verdict,
      badgeClass: badgeClass,
      reasoning: reasoning
    };
  }
}

// Global singleton instance
window.scoringEngine = new ScoringEngine();
