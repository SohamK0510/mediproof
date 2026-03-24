from __future__ import annotations
 
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
 
 
# ---------------------------------------------------------------------------
# Rule definition
# ---------------------------------------------------------------------------
@dataclass
class Rule:
    """A single named medical misinformation rule."""
    name: str
    patterns: List[str]
    user_message: str
    # If True, a single match immediately sets risk to High
    auto_high: bool = False
    # Compiled patterns (populated at class load time)
    _compiled: List[re.Pattern] = field(default_factory=list, repr=False)
 
    def compile(self) -> None:
        self._compiled = [
            re.compile(p, re.IGNORECASE | re.DOTALL) for p in self.patterns
        ]
 
    def match(self, text: str) -> Optional[str]:
        """Return the first matching snippet, or None."""
        for pattern in self._compiled:
            m = pattern.search(text)
            if m:
                return m.group(0)
        return None
 
 
# ---------------------------------------------------------------------------
# Rule catalogue
# ---------------------------------------------------------------------------
_RULES: List[Rule] = [
    Rule(
        name="chronic_disease_cure",
        patterns=[
            r"\bcures?\b.{0,40}\b(diabetes|cancer|hiv|aids|dengue|covid(?:-19)?|coronavirus|asthma|arthritis|hypertension|alzheimer|parkinson|epilepsy)\b",
            r"\b(diabetes|cancer|hiv|aids|dengue|covid(?:-19)?|coronavirus|asthma|arthritis|hypertension|alzheimer|parkinson|epilepsy)\b.{0,40}\bcures?\b",
            r"\b(eliminate[sd]?|reverse[sd]?|get rid of)\b.{0,30}\b(diabetes|cancer|hiv|aids|dengue|covid(?:-19)?|coronavirus|asthma|arthritis|hypertension)\b",
            r"\bpermanently\b.{0,20}\b(heal|fix|remove|cure)\b.{0,30}\b(disease|condition|illness|disorder)\b",
            r"\b(completely\s+cure|natural\s+cure|herbal\s+cure|instant\s+cure|cure)\b.{0,30}\b(cancer|aids|diabetes|hiv|dengue|covid(?:-19)?)\b",
            r"\b(cure for|remedy for|treatment for|natural cure for|herbal cure for)\s+(cancer|aids|diabetes|hiv|dengue|covid(?:-19)?|asthma|arthritis)\b",
        ],
        user_message=(
            "This claim suggests a cure for a serious chronic disease. "
            "Chronic conditions like cancer, diabetes, and HIV currently have no guaranteed cures. "
            "Always follow evidence-based treatment plans from qualified physicians."
        ),
        auto_high=True,
    ),
    Rule(
        name="stop_medication",
        patterns=[
            r"\b(stop|quit|avoid|replace|ditch|skip)\b.{0,40}\b(medication|medicine|meds|insulin|drugs?|treatment|prescription|chemotherapy|chemo|dialysis)\b",
            r"\b(don['']?t|no need|never).{0,30}(take|use|need).{0,30}(medication|medicine|meds|drugs?|prescription)\b",
            r"\b(natural|herbal|home)\s+(remedy|remedies|cure|treatment)\b.{0,40}\breplace[sd]?\b",
            r"\bstop taking\b.{0,30}\b(medication|medicine|meds|insulin|drugs?|treatment)\b",
            r"\bdo not take\b.{0,30}\b(medication|medicine|drugs?)\b",
        ],
        user_message=(
            "This claim advises stopping or replacing prescribed medication. "
            "Discontinuing prescribed treatments without medical supervision can be dangerous. "
            "Never alter medication schedules without consulting your doctor."
        ),
        auto_high=True,
    ),
    Rule(
        name="guaranteed_instant_cure",
        patterns=[
            r"\bguaranteed?\b.{0,30}\b(cure|heal|fix|result|recovery|relief)\b",
            r"\binstant(ly)?\b.{0,30}\b(cure|relief|heal|result|recovery)\b",
            r"\b100\s*%\s*(cure|guaranteed?|effective|result|success)\b",
            r"\b(miracle|magic(al)?)\s+(cure|remedy|treatment|pill|drug|herb)\b",
            r"\bdoctors\b.{0,30}\b(don['']?t want you to know|hate this|are hiding)\b",
            r"\bpermanent (cure|remedy|healing|solution)\b",
            r"\b(works|cures)\s+in\s+(days|hours|minutes|overnight)\b",
        ],
        user_message=(
            "This claim makes absolute or miraculous cure guarantees. "
            "No medical treatment offers a 100% guaranteed or instant cure. "
            "Such language is a common indicator of health misinformation."
        ),
        auto_high=False,
    ),
    Rule(
        name="vaccine_misinformation",
        patterns=[
            r"\bvaccine[sd]?\b.{0,50}\b(caus(e[sd]?|ing)|lead[sd]? to|result[sd]? in)\b.{0,40}\b(autism|cancer|infertility|death|paralysis|microchip|dna|5g)\b",
            r"\b(don['']?t|never|avoid)\b.{0,20}\bvaccinat(e|ion|ing)\b",
            r"\bvaccines?\b.{0,30}\b(toxic|poison(ous)?|dangerous|harmful|kill(s|ing)?)\b",
            r"\b(unvaccinat(ed)?|natural\s+immunity)\b.{0,30}\b(better|safer|healthier|superior)\b",
        ],
        user_message=(
            "This claim contains vaccine misinformation. "
            "Vaccines undergo rigorous clinical trials and safety reviews before approval. "
            "Claims linking vaccines to autism, infertility, or microchips are scientifically unfounded."
        ),
        auto_high=True,
    ),
    Rule(
        name="supplement_overdose",
        patterns=[
            r"\b(megadose|high.?dose|large.?dose|massive.?dose)\b.{0,30}\b(vitamin|supplement|mineral|herb)\b",
            r"\b(vitamin\s+[cdek]|zinc|magnesium)\b.{0,40}\b(cures?|prevents?|kill[sd]?|destroys?)\b.{0,30}\b(cancer|covid|virus|bacteria|disease)\b",
            r"\btake\b.{0,20}\b\d+\s*(gram[sd]?|mg|g)\b.{0,20}\b(vitamin\s+c|zinc|selenium)\b",
        ],
        user_message=(
            "This claim promotes high-dose supplements as treatments. "
            "Excessive supplementation can cause toxicity and adverse effects. "
            "Supplement dosages should be discussed with a healthcare provider."
        ),
        auto_high=False,
    ),
    Rule(
        name="self_diagnosis_or_treatment",
        patterns=[
            r"\b(diagnose|treat|cure|heal)\b.{0,20}\byourself\b",
            r"\bno need\b.{0,30}\b(doctor|physician|hospital|specialist|medical|clinic)\b",
            r"\b(doctors?|hospitals?|pharma|big\s+pharma)\b.{0,30}\b(lie|liar|hiding|scam|fraud|corrupt)\b",
        ],
        user_message=(
            "This claim discourages professional medical consultation. "
            "Self-diagnosis and self-treatment can delay necessary care. "
            "Please consult a qualified healthcare professional for any health concerns."
        ),
        auto_high=False,
    ),
]
 
# Compile all patterns once at module load
for _rule in _RULES:
    _rule.compile()


_SERIOUS_DISEASE_KEYWORDS = [
    "dengue",
    "cancer",
    "hiv",
    "aids",
    "diabetes",
    "covid",
    "covid-19",
    "coronavirus",
]

_CURE_PHRASE_REGEX = re.compile(
    r"\b(completely\s+cure|guaranteed\s+cure|natural\s+cure|herbal\s+cure|instant\s+cure|cure)\b",
    re.IGNORECASE,
)

_SERIOUS_DISEASE_CURE_REGEX = re.compile(
    r"(\b(completely\s+cure|guaranteed\s+cure|natural\s+cure|herbal\s+cure|instant\s+cure|cure)\b.{0,50}\b(dengue|cancer|hiv|aids|diabetes|covid(?:-19)?|coronavirus)\b)"
    r"|(\b(dengue|cancer|hiv|aids|diabetes|covid(?:-19)?|coronavirus)\b.{0,50}\b(completely\s+cure|guaranteed\s+cure|natural\s+cure|herbal\s+cure|instant\s+cure|cure)\b)",
    re.IGNORECASE | re.DOTALL,
)

_MIRACLE_GUARANTEE_REGEX = re.compile(
    r"\b(miracle\s+cure|magic\s+cure|guaranteed\s+cure|100\s*%\s*cure)\b",
    re.IGNORECASE,
)

_STOP_MEDICATION_REGEX = re.compile(
    r"\b(stop|quit|avoid|replace|ditch|skip|do\s*not\s*take|don't\s*take|never\s*take)\b.{0,45}\b(medication|medicine|meds|insulin|drugs?|treatment|prescription|chemotherapy|chemo|dialysis)\b",
    re.IGNORECASE | re.DOTALL,
)

_ANTI_VACCINE_REGEX = re.compile(
    r"\b(vaccines?\s+(cause|causes|causing|lead to|results? in)\s+(autism|infertility|death|paralysis|microchip|dna|5g)|don't\s+vaccinate|never\s+vaccinate|avoid\s+vaccinat(e|ion|ing)|vaccines?\s+(are\s+)?(toxic|poison(ous)?|dangerous|harmful))\b",
    re.IGNORECASE,
)

_NATURAL_HERBAL_SERIOUS_REGEX = re.compile(
    r"\b(natural|herbal)\b.{0,20}\b(cure|remedy|treatment)\b.{0,50}\b(dengue|cancer|hiv|aids|diabetes|covid(?:-19)?|coronavirus)\b",
    re.IGNORECASE | re.DOTALL,
)

_SUSPICIOUS_KEYWORD_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("natural cure", re.compile(r"\bnatural\s+cure\b", re.IGNORECASE)),
    ("herbal cure", re.compile(r"\bherbal\s+cure\b", re.IGNORECASE)),
    ("stop medication", re.compile(r"\bstop\s+(taking\s+)?(medication|medicine|meds|drugs?|insulin|treatment|prescription)\b", re.IGNORECASE)),
    ("vaccine causes autism", re.compile(r"\bvaccines?\s+(cause|causes|causing|lead\s+to|results?\s+in)\s+autism\b", re.IGNORECASE)),
    ("permanent cure", re.compile(r"\bpermanent\s+cure\b", re.IGNORECASE)),
    ("miracle", re.compile(r"\bmiracle\b", re.IGNORECASE)),
    ("guaranteed", re.compile(r"\bguaranteed?\b", re.IGNORECASE)),
    ("instant", re.compile(r"\binstant(ly)?\b", re.IGNORECASE)),
    ("cure", re.compile(r"\bcures?\b", re.IGNORECASE)),
]

_SUSPICIOUS_DISEASE_KEYWORDS = tuple(dict.fromkeys(_SERIOUS_DISEASE_KEYWORDS))


def extract_suspicious_keywords(claim: str) -> List[str]:
    """
    Extract suspicious misinformation keywords/phrases from a claim.

    Matching is case-insensitive and returns unique values in detection order.
    Extend by appending new entries to `_SUSPICIOUS_KEYWORD_PATTERNS`
    or `_SUSPICIOUS_DISEASE_KEYWORDS`.
    """
    if not isinstance(claim, str):
        return []

    text = claim.strip()
    if not text:
        return []

    matches: List[Tuple[int, str]] = []

    for label, pattern in _SUSPICIOUS_KEYWORD_PATTERNS:
        for found in pattern.finditer(text):
            matches.append((found.start(), label))

    lowered = text.lower()
    for disease in _SUSPICIOUS_DISEASE_KEYWORDS:
        disease_idx = lowered.find(disease)
        if disease_idx >= 0:
            matches.append((disease_idx, disease))

    if not matches:
        return []

    matches.sort(key=lambda item: item[0])

    ordered_unique: List[str] = []
    seen: set[str] = set()
    for _, token in matches:
        normalized = token.lower().strip()
        if normalized in seen:
            continue
        seen.add(normalized)
        ordered_unique.append(normalized)

    return ordered_unique
 
 
# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def apply_medical_rules(text: str) -> Dict:
    """
    Evaluate a health claim against all registered rules.
 
    Returns:
        {
            "risk_level":   "Low" | "Medium" | "High",
            "explanation":  str  (human-readable, safe to display in UI),
            "triggered_rules": [{"name": str, "message": str}, ...]
        }
    """
    triggered: List[Tuple[Rule, str]] = []
 
    for rule in _RULES:
        snippet = rule.match(text)
        if snippet is not None:
            triggered.append((rule, snippet))
 
    if not triggered:
        return {
            "risk_level": "Low",
            "explanation": "No high-risk medical patterns detected in this claim.",
            "triggered_rules": [],
        }
 
    # Determine risk level
    has_auto_high = any(rule.auto_high for rule, _ in triggered)
 
    if has_auto_high or len(triggered) >= 2:
        risk_level = "High"
    else:
        risk_level = "Medium"
 
    # Build explanation: use the most severe rule's message as headline,
    # then list all triggered rule names for context.
    primary_rule = next(
        (rule for rule, _ in triggered if rule.auto_high), triggered[0][0]
    )
    explanation = primary_rule.user_message
 
    if len(triggered) > 1:
        additional = [r.name.replace("_", " ").title() for r, _ in triggered[1:]]
        explanation += (
            f" Additionally, the following risk patterns were also detected: "
            + ", ".join(additional) + "."
        )
 
    return {
        "risk_level": risk_level,
        "explanation": explanation,
        "triggered_rules": [
            {"name": rule.name, "message": rule.user_message}
            for rule, _ in triggered
        ],
    }


# ---------------------------------------------------------------------------
# Alias for simplified risk detection
# ---------------------------------------------------------------------------

def detect_medical_risk(claim: str) -> Dict[str, str]:
    """
    Simplified medical risk detection API.
    
    Evaluates a health claim and returns only the risk level and explanation.
    For comprehensive rule information, use apply_medical_rules() instead.
    
    Args:
        claim: A health-related claim or statement to evaluate.
    
    Returns:
        {
            "risk_level": "Low" | "Medium" | "High",
            "explanation": str (human-readable explanation)
        }
    
    Examples:
        >>> detect_medical_risk("Vaccines cause autism")
        {"risk_level": "High", "explanation": "..."}
        
        >>> detect_medical_risk("Regular exercise reduces cardiovascular risk")
        {"risk_level": "Low", "explanation": "..."}
    """
    result = apply_medical_rules(claim)
    text = claim or ""
    lowered = text.lower()

    risk_rank = {"Low": 0, "Medium": 1, "High": 2}
    final_risk = result["risk_level"]
    reasons: List[str] = []

    cure_phrase_detected = bool(_CURE_PHRASE_REGEX.search(text))
    serious_disease_keyword_detected = any(
        keyword in lowered for keyword in _SERIOUS_DISEASE_KEYWORDS
    )
    serious_cure_claim_detected = bool(_SERIOUS_DISEASE_CURE_REGEX.search(text))
    miracle_or_guarantee_detected = bool(_MIRACLE_GUARANTEE_REGEX.search(text))
    stop_medication_detected = bool(_STOP_MEDICATION_REGEX.search(text))
    anti_vaccine_detected = bool(_ANTI_VACCINE_REGEX.search(text))
    natural_herbal_serious_detected = bool(_NATURAL_HERBAL_SERIOUS_REGEX.search(text))

    if serious_cure_claim_detected or (
        cure_phrase_detected and serious_disease_keyword_detected
    ):
        if risk_rank[final_risk] < risk_rank["Medium"]:
            final_risk = "Medium"
        reasons.append(
            "The claim suggests a cure for a serious disease (such as dengue, cancer, HIV, diabetes, or COVID), which is medically high-risk and often misleading without robust clinical evidence."
        )

    if miracle_or_guarantee_detected:
        if risk_rank[final_risk] < risk_rank["High"]:
            final_risk = "High"
        reasons.append(
            "Miracle or guaranteed cure language is a common misinformation marker because medical outcomes cannot be guaranteed for all patients."
        )

    if stop_medication_detected:
        if risk_rank[final_risk] < risk_rank["High"]:
            final_risk = "High"
        reasons.append(
            "Advising people to stop prescribed medication can cause serious harm and should only occur under clinician supervision."
        )

    if anti_vaccine_detected:
        if risk_rank[final_risk] < risk_rank["High"]:
            final_risk = "High"
        reasons.append(
            "Anti-vaccine claims can reduce vaccine uptake and increase preventable illness risk."
        )

    if natural_herbal_serious_detected:
        if risk_rank[final_risk] < risk_rank["High"]:
            final_risk = "High"
        reasons.append(
            "Promoting herbal or natural cures as replacements for evidence-based care in serious diseases can delay life-saving treatment."
        )

    explanation = result["explanation"]
    if reasons:
        explanation = " ".join(reasons)

    return {
        "risk_level": final_risk,
        "explanation": explanation,
    }