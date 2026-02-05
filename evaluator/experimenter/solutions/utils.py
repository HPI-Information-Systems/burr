def extract_between(s: str, start: str, end: str) -> str | None:
    try:
        start_idx = s.index(start) + len(start)
        end_idx = s.index(end, start_idx)
        return s[start_idx:end_idx]
    except ValueError:
        return None