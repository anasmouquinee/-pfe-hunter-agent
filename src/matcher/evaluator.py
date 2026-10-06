"""Scoring and filtering engine strictly tailored for Anas Mouqine's AI & Data PFE profile."""

import re
from typing import List
from src.config import config
from src.models.offer import JobOffer


class OfferEvaluator:
    """Evaluates, filters, and scores scraped job offers strictly for AI & Data Engineering."""

    PFE_KEYWORDS = [
        r'\bpfe\b', r'projet de fin d[\'’]études', r'stage pfe',
        r'stagiaire pfe', r'end-of-studies', r'graduation internship'
    ]

    AI_CORE_KEYWORDS = [
        r'\bia\b', r'\bai\b', r'intelligence artificielle', r'artificial intelligence',
        r'machine learning', r'\bml\b', r'deep learning', r'\bdl\b',
        r'data science', r'data scientist', r'data engineer', r'data engineering',
        r'ingénieur data', r'ingénieur données', r'ingénierie des données',
        r'llm', r'large language model', r'genai', r'ia générative', r'generative ai',
        r'\brag\b', r'retrieval-augmented generation', r'langchain', r'llamaindex',
        r'agentic', r'multi-agent', r'computer vision', r'vision par ordinateur',
        r'\bnlp\b', r'traitement du langage', r'neural network', r'réseaux de neurones',
        r'pytorch', r'tensorflow', r'transformers', r'hugging face', r'scikit-learn',
        r'big data', r'apache airflow', r'apache kafka', r'lakehouse'
    ]

    NON_AI_DISQUALIFIERS = [
        r'\bsap\b', r'\bhybris\b', r'servicenow', r'salesforce', r'odoo',
        r'helpdesk', r'support informatique', r'support it', r'technicien support',
        r'câblage', r'cablage', r'maintenance informatique',
        r'comptable', r'commercial', r'téléconseiller', r'vendeur',
        r'community manager', r'graphiste', r'wordpress', r'magento'
    ]

    DISQUALIFY_KEYWORDS = [
        r'\bcdi\b', r'\bcdd\b', r'senior\b', r'lead\b', r'directeur\b',
        r'5 ans d[\'’]expérience', r'7 ans d[\'’]expérience'
    ]

    REMUNERATION_KEYWORDS = [
        r'rémunér[ée]', r'remuner[ee]', r'gratification', r'indemnité',
        r'indemnite', r'bourse de stage', r'stage payé', r'stipend'
    ]

    def is_ai_offer(self, offer: JobOffer) -> bool:
        """Strictly verifies if the offer is focused on AI, ML, Data Science, or Data Engineering."""
        title_lower = offer.title.lower()
        full_text = f"{offer.title} {offer.description}".lower()

        # 1. Reject non-AI enterprise software/roles if present in title
        for pattern in self.NON_AI_DISQUALIFIERS:
            if re.search(pattern, title_lower):
                return False

        # 2. Reject if description is contaminated with non-AI keywords and lacks strong AI presence
        has_non_ai = any(re.search(pattern, full_text) for pattern in self.NON_AI_DISQUALIFIERS)
        
        # 3. Must match at least one AI core keyword
        matched_ai = [kw for kw in self.AI_CORE_KEYWORDS if re.search(kw, full_text)]
        if not matched_ai:
            return False

        # If non-AI keyword was found in description, require at least 2 distinct AI signals to prevent false positives
        if has_non_ai and len(matched_ai) < 2:
            return False

        return True

    def is_pfe_offer(self, offer: JobOffer) -> bool:
        """Determines if the offer is a genuine student PFE internship in AI."""
        text = f"{offer.title} {offer.description}".lower()

        # Check for explicit senior / permanent contract disqualifiers
        for pattern in self.DISQUALIFY_KEYWORDS:
            if re.search(pattern, text) and not any(re.search(pfe, text) for pfe in self.PFE_KEYWORDS):
                return False

        # Must be relevant to AI
        if not self.is_ai_offer(offer):
            return False

        # Check for PFE keywords in title or description
        for pattern in self.PFE_KEYWORDS:
            if re.search(pattern, text):
                return True

        # Fallback: title contains "stage" or "intern" and AI domain
        if "stage" in text or "stagiaire" in text or "intern" in text:
            if self.is_ai_offer(offer):
                return True

        return False

    def is_target_location(self, offer: JobOffer) -> bool:
        """Checks if the offer is in Casablanca, Settat, or Remote."""
        loc = f"{offer.location} {offer.description}".lower()
        targets = [c.lower() for c in config.target_cities]
        return any(city in loc for city in targets) or "maroc" in loc

    def detect_remuneration(self, offer: JobOffer) -> bool:
        """Detects if the offer mentions remuneration, gratification, or stipend."""
        text = f"{offer.title} {offer.description}".lower()
        for pattern in self.REMUNERATION_KEYWORDS:
            if re.search(pattern, text):
                return True
        return False

    def evaluate(self, offer: JobOffer) -> JobOffer:
        """Enriches the offer with match score, remuneration flag, and skill tags."""
        text = f"{offer.title} {offer.description}".lower()

        # 1. Remuneration check
        offer.is_remunerated = self.detect_remuneration(offer)

        # 2. Skill matching
        matched_skills: List[str] = []
        for skill in config.candidate.core_skills:
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text):
                if skill not in matched_skills:
                    matched_skills.append(skill)
        offer.matched_skills = matched_skills

        # 3. AI Relevance Verification
        is_ai = self.is_ai_offer(offer)
        is_pfe = self.is_pfe_offer(offer)

        if not is_ai or not is_pfe:
            # Not an AI PFE offer
            offer.score = 15
            return offer

        # 4. Score calculation for genuine AI PFE offers (0 to 100)
        base_score = 45
        skill_score = min(len(matched_skills) * 8, 40)
        remuneration_bonus = 10 if offer.is_remunerated else 0
        location_bonus = 5 if self.is_target_location(offer) else 0

        offer.score = min(base_score + skill_score + remuneration_bonus + location_bonus, 100)
        return offer
