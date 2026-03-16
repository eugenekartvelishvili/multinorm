# # sources.py

# from typing import List, Dict


# def extract_sources(results: List[Dict]) -> List[str]:
#     """
#     Извлекает список источников из результатов поиска.
#     """

#     sources = set()

#     for r in results:
#         title = r.get("title")
#         number = r.get("number")

#         if title and number:
#             sources.add(f"{title}, раздел {number}")

#         elif title:
#             sources.add(title)

#     return sorted(sources)

# # sources.py

# from typing import List, Dict


# def extract_sources(results: List[Dict]) -> List[str]:
#     """
#     Извлекает источники в формате:
#     Документ — раздел (номер)

#     Источники:
#     - дедуплицируются
#     - сортируются по score (от более релевантных к менее релевантным)
#     """

#     prepared = []

#     for r in results:
#         doc_title = (
#             r.get("doc_title")
#             or r.get("document_title")
#             or r.get("doc_name")
#             or r.get("doc_id")
#             or "Неизвестный документ"
#         )

#         section_title = r.get("title")
#         number = r.get("number")
#         score = r.get("score", 0.0)

#         try:
#             score = float(score)
#         except Exception:
#             score = 0.0

#         if section_title and number:
#             source = f"{doc_title} — {section_title} (раздел {number})"
#         elif section_title:
#             source = f"{doc_title} — {section_title}"
#         else:
#             source = str(doc_title)

#         prepared.append({
#             "source": source,
#             "score": score,
#         })

#     # сортировка по убыванию релевантности
#     prepared.sort(key=lambda x: x["score"], reverse=True)

#     # дедупликация с сохранением порядка после сортировки
#     final_sources = []
#     seen = set()

#     for item in prepared:
#         src = item["source"]
#         if src not in seen:
#             seen.add(src)
#             final_sources.append(src)

#     return final_sources

# sources.py

from typing import List, Dict

from milvus_client import MilvusApiClient


def extract_sources(results: List[Dict]) -> List[str]:
    """
    Формирует источники в формате:
    Название документа — Заголовок раздела (раздел N)

    Для doc_id подтягивает название документа через /query.
    Использует локальный кэш, чтобы не дергать API повторно.
    """

    client = MilvusApiClient()
    doc_title_cache: Dict[str, str] = {}

    prepared = []

    for r in results:
        doc_id = r.get("doc_id")
        section_title = r.get("title")
        number = r.get("number")
        score = r.get("score", 0.0)

        try:
            score = float(score)
        except Exception:
            score = 0.0

        # получаем название документа из кэша или через query
        if doc_id:
            if doc_id not in doc_title_cache:
                doc_title_cache[doc_id] = client.get_document_title_by_doc_id(str(doc_id))
            doc_title = doc_title_cache[doc_id]
        else:
            doc_title = "Неизвестный документ"

        if section_title and number:
            source = f"{doc_title} — {section_title} (раздел {number})"
        elif section_title:
            source = f"{doc_title} — {section_title}"
        else:
            source = doc_title

        prepared.append({
            "source": source,
            "score": score,
        })

    # сортируем по убыванию релевантности
    prepared.sort(key=lambda x: x["score"], reverse=True)

    # дедупликация с сохранением порядка
    final_sources = []
    seen = set()

    for item in prepared:
        src = item["source"]
        if src not in seen:
            seen.add(src)
            final_sources.append(src)

    return final_sources