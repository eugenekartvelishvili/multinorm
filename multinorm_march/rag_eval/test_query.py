# test_query.py
from pprint import pprint

from milvus_client import MilvusApiClient


def main():
    client = MilvusApiClient()

    result = client.query(
        collection="documents",
        filter_expr="level == 0",
        limit=5,
        output_fields=["doc_id", "title", "level", "number"],
    )

    print("=== QUERY RESULTS ===")
    for row in result.get("results", []):
        pprint(row)


if __name__ == "__main__":
    main()