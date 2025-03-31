def count_unique_pairs(n, k, arr):
    seen = set()
    pairs = set()

    for num in arr:
        complement = k - num
        if complement in seen:
            pairs.add(tuple(sorted((num, complement))))
        seen.add(num)

    return len(pairs)

n, k = map(int, input().split())
arr = list(map(int, input().split()))

print(count_unique_pairs(n, k, arr))

