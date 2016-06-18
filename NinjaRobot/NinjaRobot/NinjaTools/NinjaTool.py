import heapq


def get_top_n(items, n):
    if len(items) <= n:
        return items

    heap = []
    for item in items:
        if len(heap) >= n:
            top_item = heap[0]
            if top_item < item:
                heapq.heappop(heap)
                heapq.heappush(heap, item)
        else:
            heapq.heappush(heap, item)

    return heap