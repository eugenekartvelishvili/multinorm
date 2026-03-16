# test_search.py
from pprint import pprint

from milvus_client import MilvusApiClient


def main():
    client = MilvusApiClient()

    question = "Какие требования к оперативной памяти?"

    result = client.search(
        text=question,
        mode="hybrid",
        level=[0, 1, 2],
        limit=5,
        use_summary=False,
    )

    print("=== RESULTS ===")
    for i, item in enumerate(result.get("results", []), start=1):
        print(f"\n--- HIT {i} ---")
        pprint(item)

    print("\n=== CONTEXT ===")
    print(result.get("context", ""))


if __name__ == "__main__":
    main()