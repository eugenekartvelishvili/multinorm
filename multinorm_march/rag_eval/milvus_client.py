# # milvus_client.py
# from __future__ import annotations

# import requests
# from typing import Any, Dict, List, Optional

# from config import API_URL


# class MilvusApiClient:
#     def __init__(self, base_url: str = API_URL, timeout: int = 30):
#         self.base_url = base_url.rstrip("/")
#         self.timeout = timeout

#     def search(
#         self,
#         text: str,
#         mode: str = "hybrid",
#         level: Optional[List[int]] = None,
#         limit: int = 5,
#         use_summary: bool = False,
#     ) -> Dict[str, Any]:
#         """
#         Поиск через /search
#         """
#         if level is None:
#             level = [0, 1, 2]

#         payload = {
#             "text": text,
#             "mode": mode,
#             "level": level,
#             "limit": limit,
#             "use_summary": use_summary,
#         }

#         response = requests.post(
#             f"{self.base_url}/search",
#             json=payload,
#             timeout=self.timeout,
#         )
#         response.raise_for_status()
#         return response.json()

#     def query(
#         self,
#         collection: str = "documents",
#         filter_expr: Optional[str] = None,
#         limit: int = 10,
#         output_fields: Optional[List[str]] = None,
#     ) -> Dict[str, Any]:
#         """
#         Прямой запрос через /query
#         """
#         payload: Dict[str, Any] = {
#             "collection": collection,
#             "limit": limit,
#         }

#         if filter_expr:
#             payload["filter"] = filter_expr

#         if output_fields:
#             payload["output_fields"] = output_fields

#         response = requests.post(
#             f"{self.base_url}/query",
#             json=payload,
#             timeout=self.timeout,
#         )
#         response.raise_for_status()
#         return response.json()

# milvus_client.py
from __future__ import annotations

import requests
from typing import Any, Dict, List, Optional

from config import API_URL


class MilvusApiClient:
    def __init__(self, base_url: str = API_URL, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def search(
        self,
        text: str,
        mode: str = "hybrid",
        level: Optional[List[int]] = None,
        limit: int = 5,
        use_summary: bool = False,
    ) -> Dict[str, Any]:
        if level is None:
            level = [0, 1, 2]

        payload = {
            "text": text,
            "mode": mode,
            "level": level,
            "limit": limit,
            "use_summary": use_summary,
        }

        response = requests.post(
            f"{self.base_url}/search",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def query(
        self,
        collection: str = "documents",
        filter_expr: Optional[str] = None,
        limit: int = 10,
        output_fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "collection": collection,
            "limit": limit,
        }

        if filter_expr:
            payload["filter"] = filter_expr

        if output_fields:
            payload["output_fields"] = output_fields

        response = requests.post(
            f"{self.base_url}/query",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_document_title_by_doc_id(self, doc_id: str) -> str:
        """
        Пытаемся получить человекочитаемое название документа по doc_id.
        Сначала ищем level == 0, потом fallback на любую запись документа.
        """
        # 1) сначала пробуем level 0
        result = self.query(
            collection="documents",
            filter_expr=f"doc_id == '{doc_id}' && level == 0",
            limit=5,
            output_fields=["doc_id", "title", "level", "number"],
        )

        rows = result.get("results", [])
        if rows:
            row = rows[0]
            title = row.get("title")
            if title and str(title).strip():
                return str(title).strip()

        # 2) fallback: любая запись документа
        result = self.query(
            collection="documents",
            filter_expr=f"doc_id == '{doc_id}'",
            limit=5,
            output_fields=["doc_id", "title", "level", "number"],
        )

        rows = result.get("results", [])
        if rows:
            for row in rows:
                title = row.get("title")
                if title and str(title).strip():
                    return str(title).strip()

        return doc_id