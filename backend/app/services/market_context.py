"""
Market context detector and currency configuration for universal startup analysis.
Defaults to India when no explicit geography is provided by the user.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import re


@dataclass
class MarketContext:
    country: str
    region_type: str  # "India" or "International"
    currency_code: str  # e.g., "INR", "USD", "GBP", "EUR"
    currency_symbol: str  # e.g., "₹", "$", "£", "€"
    is_india: bool
    relevant_factors: List[str] = field(default_factory=list)
    section_titles: Dict[int, str] = field(default_factory=dict)
    
    # Financial scaling brackets for BattleScore
    tam_benchmark_local: float = 1_000_000_000.0  # e.g. ₹1000 Cr ($120M) or $1B
    rev_y3_benchmark_local: float = 100_000_000.0  # e.g. ₹10 Cr ($1.2M) or $10M


# Common geography dictionaries
COUNTRY_CURRENCY_MAP = {
    "india": ("India", "INR", "₹"),
    "bharat": ("India", "INR", "₹"),
    "us": ("United States", "USD", "$"),
    "usa": ("United States", "USD", "$"),
    "united states": ("United States", "USD", "$"),
    "america": ("United States", "USD", "$"),
    "uk": ("United Kingdom", "GBP", "£"),
    "united kingdom": ("United Kingdom", "GBP", "£"),
    "britain": ("United Kingdom", "GBP", "£"),
    "england": ("United Kingdom", "GBP", "£"),
    "europe": ("Europe", "EUR", "€"),
    "eu": ("Europe", "EUR", "€"),
    "germany": ("Germany", "EUR", "€"),
    "france": ("France", "EUR", "€"),
    "canada": ("Canada", "CAD", "C$"),
    "australia": ("Australia", "AUD", "A$"),
    "singapore": ("Singapore", "SGD", "S$"),
    "uae": ("United Arab Emirates", "AED", "AED"),
    "dubai": ("United Arab Emirates", "AED", "AED"),
    "japan": ("Japan", "JPY", "¥"),
}


def detect_market_context(idea: Any) -> MarketContext:
    """
    Analyzes StartupIdea to detect target geography and currency.
    If no explicit foreign geography is specified, defaults to India (India-First default).
    """
    # 1. Gather all text fields from the idea
    text_fields = []
    
    target_market = getattr(idea, "target_market", None) or getattr(idea, "geography", None)
    if target_market:
        text_fields.append(str(target_market).lower())
        
    company_name = getattr(idea, "company_name", "")
    business_concept = getattr(idea, "business_concept", "")
    problem_statement = getattr(idea, "problem_statement", "") or ""
    target_users = getattr(idea, "target_users", "") or ""
    revenue_model = getattr(idea, "revenue_model", "") or ""
    industry = getattr(idea, "industry", "") or ""
    
    full_text = f"{target_market or ''} {company_name} {business_concept} {problem_statement} {target_users} {revenue_model} {industry}".lower()

    # 2. Check for explicit international geography first
    detected_country = None
    currency_code = "INR"
    currency_symbol = "₹"
    is_india = True
    
    # Check if target_market was explicitly given
    if target_market:
        clean_target = str(target_market).strip().lower()
        for key, val in COUNTRY_CURRENCY_MAP.items():
            if re.search(rf"\b{re.escape(key)}\b", clean_target):
                detected_country, currency_code, currency_symbol = val
                is_india = (key in ["india", "bharat"])
                break

    # If not found in target_market, scan full text for explicit foreign countries
    if not detected_country:
        # Check non-Indian keys first
        for key, val in COUNTRY_CURRENCY_MAP.items():
            if key in ["india", "bharat"]:
                continue
            pattern = rf"\b{re.escape(key)}\b"
            if re.search(pattern, full_text):
                detected_country, currency_code, currency_symbol = val
                is_india = False
                break

    # If still not found, check for explicit India mentions or apply India-first default
    if not detected_country:
        detected_country = "India"
        currency_code = "INR"
        currency_symbol = "₹"
        is_india = True

    # 3. Detect contextually relevant factors for the business (Rule 5)
    relevant_factors = []
    business_lower = full_text.lower()
    
    if is_india:
        # UPI / digital payments relevance
        if any(w in business_lower for w in ["pay", "transact", "checkout", "commerce", "subscription", "b2c", "consumer", "fintech", "wallet", "booking", "cab", "ride", "food", "order"]):
            relevant_factors.append("UPI & Digital Payments Ecosystem")
        # WhatsApp conversational/onboarding relevance
        if any(w in business_lower for w in ["chat", "customer service", "communication", "b2c", "local", "booking", "notification", "student", "community", "whatsapp"]):
            relevant_factors.append("WhatsApp-first engagement and notifications")
        # Aadhaar / eKYC relevance
        if any(w in business_lower for w in ["identity", "verify", "kyc", "student id", "fintech", "lending", "credit", "background check", "onboarding", "driver", "compliance"]):
            relevant_factors.append("Aadhaar / DigiLocker / eKYC verification")
        # GST & Invoicing relevance
        if any(w in business_lower for w in ["b2b", "invoice", "vendor", "enterprise", "merchant", "supplier", "distributor", "tax", "gst"]):
            relevant_factors.append("GST compliance and input tax credit workflow")
        # Tier 1/2/3 city segmentation
        if any(w in business_lower for w in ["tier", "expansion", "offline", "retail", "vernacular", "regional", "logistics", "delivery", "college", "campus"]):
            relevant_factors.append("Tier 1/2/3 market purchasing power segmentation")
        # Regional languages
        if any(w in business_lower for w in ["vernacular", "language", "bharat", "rural", "semi-urban", "regional"]):
            relevant_factors.append("Multilingual / vernacular UX")
        # Distribution network
        if any(w in business_lower for w in ["fmcg", "offline", "retail", "distribution", "dealer", "franchise", "kirana", "agent"]):
            relevant_factors.append("Kirana / local distributor channels")
    else:
        # International factors
        if "United States" in detected_country:
            relevant_factors.extend(["Stripe / ACH / Credit Card processing", "State-by-state compliance / US Sales Tax", "GDPR / CCPA privacy frameworks"])
        elif "Europe" in detected_country or "United Kingdom" in detected_country:
            relevant_factors.extend(["GDPR privacy & data residency", "SEPA / Open Banking", "VAT compliance"])
        else:
            relevant_factors.append(f"{detected_country} local payment rails and commercial regulations")

    # 4. Generate dynamic 21-section titles (Rule 17)
    sec_4_title = "India Market Opportunity" if is_india else f"{detected_country} Market Opportunity"
    sec_7_title = "Indian Competitor Analysis" if is_india else f"{detected_country} Competitor Analysis"
    sec_14_title = "India Go-To-Market Strategy" if is_india else f"{detected_country} Go-To-Market Strategy"

    section_titles = {
        1: "Executive Summary",
        2: "Business Concept",
        3: "Problem & Customer",
        4: sec_4_title,
        5: "Customer Behavior",
        6: "Value Proposition & USP",
        7: sec_7_title,
        8: "Feature Gaps",
        9: "Business Model",
        10: "Pricing Strategy",
        11: "Financial & Unit Economics",
        12: "MVP",
        13: "Validation Strategy",
        14: sec_14_title,
        15: "Success Metrics",
        16: "Risks & Mitigation",
        17: "Challenged Assumptions",
        18: "Failure Scenarios",
        19: "Execution Roadmap",
        20: "Final Recommendation",
        21: "Sources & Citations",
    }

    # 5. Financial benchmarks for Battle Score normalization
    if is_india:
        # In INR: ₹1,000 Crore (~$120M) TAM benchmark, ₹10 Crore (~$1.2M) Year 3 Rev benchmark
        tam_benchmark = 10_000_000_000.0  # ₹1,000 Cr
        rev_y3_benchmark = 100_000_000.0  # ₹10 Cr
    elif currency_code == "USD":
        tam_benchmark = 1_000_000_000.0   # $1B
        rev_y3_benchmark = 10_000_000.0    # $10M
    elif currency_code == "GBP":
        tam_benchmark = 800_000_000.0     # £800M
        rev_y3_benchmark = 8_000_000.0     # £8M
    elif currency_code == "EUR":
        tam_benchmark = 900_000_000.0     # €900M
        rev_y3_benchmark = 9_000_000.0     # €9M
    else:
        tam_benchmark = 1_000_000_000.0
        rev_y3_benchmark = 10_000_000.0

    return MarketContext(
        country=detected_country,
        region_type="India" if is_india else "International",
        currency_code=currency_code,
        currency_symbol=currency_symbol,
        is_india=is_india,
        relevant_factors=relevant_factors,
        section_titles=section_titles,
        tam_benchmark_local=tam_benchmark,
        rev_y3_benchmark_local=rev_y3_benchmark
    )


def format_currency_amount(amount: Optional[float], currency_symbol: str = "₹", currency_code: str = "INR") -> str:
    """
    Format monetary amounts nicely depending on currency.
    For INR: formats with Lakhs / Crores if large, else comma formatting.
    For USD/others: formats with standard thousands/millions/billions.
    """
    if amount is None or amount == 0:
        return "Insufficient verified data; requires validation."
    
    try:
        val = float(amount)
    except (ValueError, TypeError):
        return "Insufficient verified data; requires validation."

    if currency_code == "INR":
        if val >= 100_000_000:
            cr = val / 10_000_000
            return f"{currency_symbol}{cr:,.2f} Cr"
        elif val >= 100_000:
            lakh = val / 100_000
            return f"{currency_symbol}{lakh:,.2f} Lakh"
        else:
            return f"{currency_symbol}{val:,.0f}"
    else:
        if val >= 1_000_000_000:
            return f"{currency_symbol}{val / 1_000_000_000:,.2f}B"
        elif val >= 1_000_000:
            return f"{currency_symbol}{val / 1_000_000:,.2f}M"
        elif val >= 1_000:
            return f"{currency_symbol}{val:,.0f}"
        else:
            return f"{currency_symbol}{val:,.2f}"
