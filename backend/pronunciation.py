import re

# Case numbers like 2024-CV-08472, 2023-CA-12345
_CASE_NUM_RE = re.compile(r"\b(\d{4}-[A-Z]{2}-\d+)\b")

# Statutes like "Section 12.3(a)(ii)", "Section 482.01(3)(a)"
_STATUTE_RE = re.compile(
    r"\b(Section\s+\d+(?:\.\d+)*(?:\([a-zA-Z0-9]+\))*(?:\([a-zA-Z0-9]+\))*)\b",
    re.IGNORECASE,
)

# Highway/interstate like I-95, I-75, I-10
_HIGHWAY_RE = re.compile(r"\b(I-\d{1,3})\b")


def wrap_legal_citations(text: str) -> str:
    """Detect legal citations and wrap them for Mist v2 phonemization."""
    # Case numbers: spell out characters
    def _spell_case(m: re.Match) -> str:
        raw = m.group(1)
        # "2024-CV-08472" → "2024 C V 08472"
        parts = raw.split("-")
        spelled = []
        for p in parts:
            if p.isalpha():
                spelled.append(" ".join(p))
            else:
                spelled.append(p)
        spelled_str = " ".join(spelled)
        return f"{{phonemizeBetweenBrackets}}{spelled_str}{{/phonemizeBetweenBrackets}}"

    text = _CASE_NUM_RE.sub(_spell_case, text)

    # Statutes: wrap as-is
    def _wrap_statute(m: re.Match) -> str:
        return f"{{phonemizeBetweenBrackets}}{m.group(1)}{{/phonemizeBetweenBrackets}}"

    text = _STATUTE_RE.sub(_wrap_statute, text)

    # Highways: wrap as-is
    def _wrap_highway(m: re.Match) -> str:
        return f"{{phonemizeBetweenBrackets}}{m.group(1)}{{/phonemizeBetweenBrackets}}"

    text = _HIGHWAY_RE.sub(_wrap_highway, text)

    return text


def has_legal_citations(text: str) -> bool:
    """Return True if text contains any detectable legal citation."""
    return bool(_CASE_NUM_RE.search(text) or _STATUTE_RE.search(text) or _HIGHWAY_RE.search(text))
