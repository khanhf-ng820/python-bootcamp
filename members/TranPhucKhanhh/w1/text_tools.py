"""W1 word frequency utilities."""


def word_count(text: str) -> dict[str, int]:
    """Count case-insensitive words separated by non-letter characters."""
    text = text.lower()

    tmp = ""
    dict = {}
    for char in text:
        if char.islower() == 0:
            if tmp == "":
                continue

            if tmp in dict:
                dict[tmp] += 1
            else:
                dict[tmp] = 1

            tmp = ""
        else:
            tmp += char

    if tmp != "":
        if tmp in dict:
            dict[tmp] += 1
        else:
            dict[tmp] = 1

    return dict


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return up to k words ordered by frequency, then alphabetically."""
    return sorted(word_count(text).items(), key=lambda item: (-item[1], item[0]))[:k]
