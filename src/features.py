import re

SENIOR = re.compile(r"\b(senior|sr\.?|lead|principal|staff|head|manager)\b", re.I)
JUNIOR = re.compile(r"\b(intern|internship|junior|fresher|trainee|graduate|entry)\b", re.I)
YEARS = re.compile(r"(\d+)\s*(?:\+|-|–|to)?\s*(\d+)?\s*\+?\s*(?:years|year|yrs|yr)", re.I)


def job_years(title, text):
    """Guess the years of experience a job wants. None if unknown."""
    found = YEARS.findall(text or "")
    if found:
        return min(int(a) for a, _ in found)
    if SENIOR.search(title or ""):
        return 6
    if JUNIOR.search(title or ""):
        return 0
    return None


def level_match(candidate_years, job_yrs):
    """1.0 = same level, 0.0 = far apart, 0.5 = unknown."""
    if job_yrs is None:
        return 0.5
    return max(0.0, 1 - abs(candidate_years - job_yrs) / 5)


def location_match(wanted, job_location):
    """1.0 = wanted city, 0.5 = India/Worldwide, 0.0 = other city."""
    loc = (job_location or "").lower()
    if any(w in loc for w in wanted):
        return 1.0
    if loc.strip() in ("india", "worldwide", ""):
        return 0.5
    return 0.0


if __name__ == "__main__":
    print(job_years("Senior Machine Learning Engineer", "Experience: 8 Years"))
    print(job_years("NLP Engineer", "Experience : 1-2 years"))
    print(job_years("Data Scientist", "We need a data scientist"))
    print(job_years("Data Science Intern", "internship"))
    print(level_match(0, 8), level_match(3, 4), level_match(2, None))
    print(location_match(["pune"], "Pune, Maharashtra"),
          location_match(["pune"], "India"),
          location_match(["pune"], "Chennai, Tamil Nadu"))