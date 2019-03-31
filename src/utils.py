from collections import Counter


def contains_any(xs: list, ys: list):
    for x in xs:
        if isinstance(x, float):
            return False
        for y in ys:
            if y.lower() in x.lower():
                return True
    return False


def compare_name(s):
    try:
        return int(s.split("-")[0])
    except:
        return 0


# map: keyword -> number of occurrences
def find_keywords(lines: list, keywords: list, most_relevant_keywords: set):
    text = " ".join(lines).lower()
    found = Counter()
    found_most_relevant = Counter()

    for group in keywords:
        for keyword in group:
            if keyword in text:
                found.update([keyword])

    for keyword in most_relevant_keywords:
        if keyword in text:
            found_most_relevant.update([keyword])

    return found, found_most_relevant


def is_like_number(s: str):
    if isinstance(s, float):
        # NaN
        return False
    for c in s:
        if c.isdigit():
            return True
    return False


def find_most_dense_region(lines: list, keywords: list, most_relevant_keywords: set, region_size: int):
    start = 0
    end = region_size
    result_start = -1
    result_end = -1

    found, found_most_relevant = find_keywords(lines[start:end], keywords, most_relevant_keywords)
    # result_found = found
    count = len(found)
    result_count = count
    while end < len(lines):
        if start > 0:
            missed_keywords, missed_most_relevant = find_keywords([lines[start - 1]], keywords, most_relevant_keywords)
            new_keywords, new_most_relevant = find_keywords([lines[end - 1]], keywords, most_relevant_keywords)
            found = found - missed_keywords + new_keywords
            found_most_relevant = found_most_relevant - missed_most_relevant + new_most_relevant

            group_count = 0
            checked_groups = set()
            for kw in found:
                for i, group in enumerate(keywords):
                    if i not in checked_groups and kw in group:
                        group_count += 1
                        checked_groups.add(i)

            count = 2 * len(found_most_relevant) + group_count

        if count >= result_count:
            # result_found = found
            result_count = count
            result_start = start
            result_end = end

        start += 1
        end += 1

    # for kw in result_found:
    # keywords_hits[kw] += 1

    return result_count, result_start, result_end
