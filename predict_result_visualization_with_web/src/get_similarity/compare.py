
def hash_compare(hashes_A, hashes_B):
    result = []

    for hash_A in hashes_A:
        for hash_B in hashes_B:
            diff = hash_A["hash"] - hash_B["hash"]
            if diff < 5:
                result.append({"count": hash_A["count"], "sec": hash_A["sec"]})
                break
    return result