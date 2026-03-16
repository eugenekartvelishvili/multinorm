# # router.py
# from __future__ import annotations

# import json
# from typing import Any, Dict

# from classifier import classify_question
# from milvus_client import MilvusApiClient

# from answer_generator import generate_answer


# def build_search_payload(question_type: str) -> Dict[str, Any]:
#     """
#     Собирает payload для /search на основе типа вопроса.
#     """

#     if question_type == "fact":
#         return {
#             "mode": "dense",
#             "level": [1, 2],
#             "limit": 5,
#             "use_summary": False,
#         }

#     if question_type == "definition":
#         return {
#             "mode": "hybrid",
#             "level": [1, 2],
#             "limit": 6,
#             "use_summary": True,
#         }

#     if question_type == "procedure":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1, 2],
#             "limit": 8,
#             "use_summary": True,
#         }

#     if question_type == "norm_reference":
#         return {
#             "mode": "sparse",
#             "level": [1, 2],
#             "limit": 8,
#             "use_summary": False,
#         }

#     if question_type == "broad_overview":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1],
#             "limit": 6,
#             "use_summary": True,
#         }

#     # fallback по умолчанию
#     return {
#         "mode": "hybrid",
#         "level": [0, 1, 2],
#         "limit": 5,
#         "use_summary": True,
#     }


# def adaptive_search(question: str) -> Dict[str, Any]:
#     """
#     Полный цикл:
#     вопрос -> классификация -> routing -> search
#     """
#     classification = classify_question(question)
#     question_type = classification["question_type"]

#     payload = build_search_payload(question_type)

#     client = MilvusApiClient()
#     search_result = client.search(
#         text=question,
#         mode=payload["mode"],
#         level=payload["level"],
#         limit=payload["limit"],
#         use_summary=payload["use_summary"],
#     )

#     answer = generate_answer(
#         question=question,
#         context=search_result.get("context", ""),
#         question_type=question_type,
#     )

#     return {
#         "question": question,
#         "classification": classification,
#         "search_payload": payload,
#         "results": search_result.get("results", []),
#         "context": search_result.get("context", ""),
#         "answer": answer
#     }


# if __name__ == "__main__":
#     test_questions = [
#         "Какие требования к оперативной памяти?",
#         "Как у нас проходит закупка оборудования от начала до конца?",
#         "Где прописана процедура ПТП?",
#         "Какие задачи у сотрудников отдела геологии?",
#     ]

#     for q in test_questions:
#         result = adaptive_search(q)

#         print("=" * 100)
#         print("QUESTION:", result["question"])
#         print("CLASSIFICATION:")
#         print(json.dumps(result["classification"], ensure_ascii=False, indent=2))
#         print("SEARCH PAYLOAD:")
#         print(json.dumps(result["search_payload"], ensure_ascii=False, indent=2))
#         print("TOP HITS COUNT:", len(result["results"]))
#         print("CONTEXT:")
#         print(result["context"])
#         print("ANSWER:")
#         print(result["answer"])
#         print()

# # router.py
# from __future__ import annotations

# import json
# import argparse
# from typing import Any, Dict

# from classifier import classify_question
# from milvus_client import MilvusApiClient
# from answer_generator import generate_answer


# def build_search_payload(question_type: str) -> Dict[str, Any]:
#     """
#     Собирает payload для /search на основе типа вопроса.
#     """

#     if question_type == "fact":
#         return {
#             "mode": "dense",
#             "level": [1, 2],
#             "limit": 5,
#             "use_summary": False,
#         }

#     if question_type == "definition":
#         return {
#             "mode": "hybrid",
#             "level": [1, 2],
#             "limit": 6,
#             "use_summary": True,
#         }

#     if question_type == "procedure":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1, 2],
#             "limit": 8,
#             "use_summary": True,
#         }

#     if question_type == "norm_reference":
#         return {
#             "mode": "sparse",
#             "level": [1, 2],
#             "limit": 8,
#             "use_summary": False,
#         }

#     if question_type == "broad_overview":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1],
#             "limit": 6,
#             "use_summary": True,
#         }

#     # fallback по умолчанию
#     return {
#         "mode": "hybrid",
#         "level": [0, 1, 2],
#         "limit": 5,
#         "use_summary": True,
#     }


# def adaptive_search(question: str) -> Dict[str, Any]:
#     """
#     Полный цикл:
#     вопрос -> классификация -> routing -> search -> answer
#     """
#     classification = classify_question(question)
#     question_type = classification["question_type"]

#     payload = build_search_payload(question_type)

#     client = MilvusApiClient()
#     search_result = client.search(
#         text=question,
#         mode=payload["mode"],
#         level=payload["level"],
#         limit=payload["limit"],
#         use_summary=payload["use_summary"],
#     )

#     context = search_result.get("context", "")

#     answer = generate_answer(
#         question=question,
#         context=context,
#         question_type=question_type,
#     )

#     return {
#         "question": question,
#         "classification": classification,
#         "search_payload": payload,
#         "results": search_result.get("results", []),
#         "context": context,
#         "answer": answer,
#     }


# def print_result(result: Dict[str, Any], show_context: bool = True, context_limit: int = 0) -> None:
#     print("=" * 100)
#     print("QUESTION:", result["question"])

#     print("CLASSIFICATION:")
#     print(json.dumps(result["classification"], ensure_ascii=False, indent=2))

#     print("SEARCH PAYLOAD:")
#     print(json.dumps(result["search_payload"], ensure_ascii=False, indent=2))

#     print("TOP HITS COUNT:", len(result["results"]))

#     print("ANSWER:")
#     print(result["answer"])

#     if show_context:
#         print("CONTEXT:")
#         context = result["context"]
#         if context_limit > 0 and len(context) > context_limit:
#             print(context[:context_limit] + "\n...[TRUNCATED]...")
#         else:
#             print(context)

#     print()


# def chat_loop(show_context: bool = False, context_limit: int = 0) -> None:
#     print("💬 Adaptive RAG chat mode. Пустая строка — выход.")
#     while True:
#         try:
#             question = input("\n❓ Вопрос: ").strip()
#         except (EOFError, KeyboardInterrupt):
#             print("\n👋 Выход.")
#             break

#         if not question:
#             print("👋 Выход.")
#             break

#         try:
#             result = adaptive_search(question)
#             print_result(result, show_context=show_context, context_limit=context_limit)
#         except Exception as e:
#             print(f"Ошибка: {e}")


# def run_default_tests(show_context: bool = True, context_limit: int = 3000) -> None:
#     test_questions = [
#         "Какие требования к оперативной памяти?",
#         "Что такое федеральный оператор?",
#         "Как у нас проходит закупка оборудования от начала до конца?",
#         "Где прописана процедура ПТП?",
#         "Какие задачи у сотрудников отдела геологии?",
#     ]

#     for q in test_questions:
#         result = adaptive_search(q)
#         print_result(result, show_context=show_context, context_limit=context_limit)


# def main():
#     parser = argparse.ArgumentParser(description="Adaptive RAG router for Milvus API")
#     parser.add_argument("question", nargs="?", help="Один вопрос для запуска")
#     parser.add_argument("--chat", action="store_true", help="Интерактивный режим")
#     parser.add_argument("--show-context", action="store_true", help="Показывать контекст")
#     parser.add_argument("--context-limit", type=int, default=0, help="Обрезать контекст до N символов (0 = без обрезки)")
#     args = parser.parse_args()

#     if args.chat:
#         chat_loop(show_context=args.show_context, context_limit=args.context_limit)
#         return

#     if args.question:
#         result = adaptive_search(args.question)
#         print_result(result, show_context=args.show_context, context_limit=args.context_limit)
#         return

#     run_default_tests(show_context=True, context_limit=3000)


# if __name__ == "__main__":
#     main()

# # router.py
# from __future__ import annotations

# import json
# import argparse
# from typing import Any, Dict

# from classifier import classify_question
# from milvus_client import MilvusApiClient
# from answer_generator import generate_answer
# from sources import extract_sources


# def build_search_payload(question_type: str) -> Dict[str, Any]:
#     """
#     Собирает payload для /search на основе типа вопроса.
#     """

#     if question_type == "fact":
#         return {
#             "mode": "dense",
#             "level": [1, 2],
#             "limit": 5,
#             "use_summary": False,
#         }

#     if question_type == "definition":
#         return {
#             "mode": "hybrid",
#             "level": [1, 2],
#             "limit": 6,
#             "use_summary": True,
#         }

#     if question_type == "procedure":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1, 2],
#             "limit": 8,
#             "use_summary": True,
#         }

#     if question_type == "norm_reference":
#         return {
#             "mode": "sparse",
#             "level": [1, 2],
#             "limit": 8,
#             "use_summary": False,
#         }

#     if question_type == "broad_overview":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1],
#             "limit": 6,
#             "use_summary": True,
#         }

#     # fallback по умолчанию
#     return {
#         "mode": "hybrid",
#         "level": [0, 1, 2],
#         "limit": 5,
#         "use_summary": True,
#     }


# def format_sources(sources: list[str]) -> str:
#     """
#     Красиво форматирует список источников для ответа.
#     """
#     if not sources:
#         return "Источники: не найдены"

#     lines = ["Источники:"]
#     for src in sources:
#         lines.append(f"• {src}")
#     return "\n".join(lines)


# def adaptive_search(question: str) -> Dict[str, Any]:
#     """
#     Полный цикл:
#     вопрос -> классификация -> routing -> search -> answer -> sources
#     """
#     classification = classify_question(question)
#     question_type = classification["question_type"]

#     payload = build_search_payload(question_type)

#     client = MilvusApiClient()
#     search_result = client.search(
#         text=question,
#         mode=payload["mode"],
#         level=payload["level"],
#         limit=payload["limit"],
#         use_summary=payload["use_summary"],
#     )

#     context = search_result.get("context", "")
#     results = search_result.get("results", [])

#     answer = generate_answer(
#         question=question,
#         context=context,
#         question_type=question_type,
#     )

#     # Ограничиваем число источников, чтобы не было мусора
#     sources = extract_sources(results)[:4]

#     # Добавляем источники в конец ответа
#     answer_with_sources = answer.strip()
#     if sources:
#         answer_with_sources += "\n\n" + format_sources(sources)
#     else:
#         answer_with_sources += "\n\nИсточники: не найдены"

#     return {
#         "question": question,
#         "classification": classification,
#         "search_payload": payload,
#         "results": results,
#         "context": context,
#         "answer": answer_with_sources,
#         "sources": sources,
#     }


# def print_result(result: Dict[str, Any], show_context: bool = True, context_limit: int = 0) -> None:
#     print("=" * 100)
#     print("QUESTION:", result["question"])

#     print("CLASSIFICATION:")
#     print(json.dumps(result["classification"], ensure_ascii=False, indent=2))

#     print("SEARCH PAYLOAD:")
#     print(json.dumps(result["search_payload"], ensure_ascii=False, indent=2))

#     print("TOP HITS COUNT:", len(result["results"]))

#     print("ANSWER:")
#     print(result["answer"])

#     # Дополнительно выводим источники отдельно, чтобы было видно в дебаге
#     if result.get("sources"):
#         print("\nSOURCES:")
#         for src in result["sources"]:
#             print(f"- {src}")

#     if show_context:
#         print("\nCONTEXT:")
#         context = result["context"]
#         if context_limit > 0 and len(context) > context_limit:
#             print(context[:context_limit] + "\n...[TRUNCATED]...")
#         else:
#             print(context)

#     print()


# def chat_loop(show_context: bool = False, context_limit: int = 0) -> None:
#     print("💬 Adaptive RAG chat mode. Пустая строка — выход.")
#     while True:
#         try:
#             question = input("\n❓ Вопрос: ").strip()
#         except (EOFError, KeyboardInterrupt):
#             print("\n👋 Выход.")
#             break

#         if not question:
#             print("👋 Выход.")
#             break

#         try:
#             result = adaptive_search(question)
#             print_result(result, show_context=show_context, context_limit=context_limit)
#         except Exception as e:
#             print(f"Ошибка: {e}")


# def run_default_tests(show_context: bool = True, context_limit: int = 3000) -> None:
#     test_questions = [
#         "Какие требования к оперативной памяти?",
#         "Что такое федеральный оператор?",
#         "Как у нас проходит закупка оборудования от начала до конца?",
#         "Где прописана процедура ПТП?",
#         "Какие задачи у сотрудников отдела геологии?",
#     ]

#     for q in test_questions:
#         result = adaptive_search(q)
#         print_result(result, show_context=show_context, context_limit=context_limit)


# def main():
#     parser = argparse.ArgumentParser(description="Adaptive RAG router for Milvus API")
#     parser.add_argument("question", nargs="?", help="Один вопрос для запуска")
#     parser.add_argument("--chat", action="store_true", help="Интерактивный режим")
#     parser.add_argument("--show-context", action="store_true", help="Показывать контекст")
#     parser.add_argument("--context-limit", type=int, default=0, help="Обрезать контекст до N символов (0 = без обрезки)")
#     args = parser.parse_args()

#     if args.chat:
#         chat_loop(show_context=args.show_context, context_limit=args.context_limit)
#         return

#     if args.question:
#         result = adaptive_search(args.question)
#         print_result(result, show_context=args.show_context, context_limit=args.context_limit)
#         return

#     run_default_tests(show_context=True, context_limit=3000)


# if __name__ == "__main__":
#     main()

# 

# # router.py
# from __future__ import annotations

# import json
# import argparse
# from typing import Any, Dict

# from classifier import classify_question
# from milvus_client import MilvusApiClient
# from answer_generator import generate_answer
# from sources import extract_sources


# def build_search_payload(question_type: str) -> Dict[str, Any]:

#     if question_type == "fact":
#         return {
#             "mode": "dense",
#             "level": [1, 2],
#             "limit": 5,
#             "use_summary": False,
#         }

#     if question_type == "definition":
#         return {
#             "mode": "hybrid",
#             "level": [1, 2],
#             "limit": 6,
#             "use_summary": True,
#         }

#     if question_type == "procedure":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1, 2],
#             "limit": 8,
#             "use_summary": True,
#         }

#     if question_type == "norm_reference":
#         return {
#             "mode": "sparse",
#             "level": [1, 2],
#             "limit": 8,
#             "use_summary": False,
#         }

#     if question_type == "broad_overview":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1],
#             "limit": 6,
#             "use_summary": True,
#         }

#     return {
#         "mode": "hybrid",
#         "level": [0, 1, 2],
#         "limit": 5,
#         "use_summary": True,
#     }


# def format_sources(sources: list[str]) -> str:

#     if not sources:
#         return "Источники: не найдены"

#     lines = ["Источники:"]
#     for src in sources:
#         lines.append(f"• {src}")

#     return "\n".join(lines)


# def adaptive_search(question: str) -> Dict[str, Any]:

#     classification = classify_question(question)
#     question_type = classification["question_type"]

#     payload = build_search_payload(question_type)

#     client = MilvusApiClient()

#     search_result = client.search(
#         text=question,
#         mode=payload["mode"],
#         level=payload["level"],
#         limit=payload["limit"],
#         use_summary=payload["use_summary"],
#     )

#     context = search_result.get("context", "")
#     results = search_result.get("results", [])

#     if context.strip():
#         answer = generate_answer(
#             question=question,
#             context=context,
#             question_type=question_type,
#         )
#     else:
#         answer = "В документах нет информации по этому вопросу."

#     # берём максимум 3 источника
#     print("\nDEBUG FIRST RESULT:")
#     print(json.dumps(results[0], ensure_ascii=False, indent=2))
#     sources = extract_sources(results)[:3]

#     answer_with_sources = answer.strip()

#     if sources:
#         answer_with_sources += "\n\n" + format_sources(sources)
#     else:
#         answer_with_sources += "\n\nИсточники: не найдены"

#     return {
#         "question": question,
#         "question_type": question_type,
#         "classification": classification,
#         "search_payload": payload,
#         "results": results,
#         "context": context,
#         "answer": answer_with_sources,
#         "sources": sources,
#     }


# def print_result(result: Dict[str, Any], show_context: bool = True, context_limit: int = 0) -> None:

#     print("=" * 100)

#     print("QUESTION:", result["question"])

#     print("CLASSIFICATION:")
#     print(json.dumps(result["classification"], ensure_ascii=False, indent=2))

#     print("SEARCH PAYLOAD:")
#     print(json.dumps(result["search_payload"], ensure_ascii=False, indent=2))

#     print("TOP HITS COUNT:", len(result["results"]))

#     print("\nANSWER:")
#     print(result["answer"])

#     if show_context:

#         print("\nCONTEXT:")

#         context = result["context"]

#         if context_limit > 0 and len(context) > context_limit:
#             print(context[:context_limit] + "\n...[TRUNCATED]...")
#         else:
#             print(context)

#     print()


# def chat_loop(show_context: bool = False, context_limit: int = 0) -> None:

#     print("💬 Adaptive RAG chat mode. Пустая строка — выход.")

#     while True:

#         try:
#             question = input("\n❓ Вопрос: ").strip()
#         except (EOFError, KeyboardInterrupt):
#             print("\n👋 Выход.")
#             break

#         if not question:
#             print("👋 Выход.")
#             break

#         try:
#             result = adaptive_search(question)
#             print_result(result, show_context=show_context, context_limit=context_limit)
#         except Exception as e:
#             print(f"Ошибка: {e}")


# def run_default_tests(show_context: bool = True, context_limit: int = 3000) -> None:

#     test_questions = [
#         "Какие требования к оперативной памяти?",
#         "Как у нас проходит закупка оборудования от начала до конца?",
#         "Где прописана процедура ПТП?",
#         "Какие задачи у сотрудников отдела геологии?",
#     ]

#     for q in test_questions:
#         result = adaptive_search(q)
#         print_result(result, show_context=show_context, context_limit=context_limit)


# def main():

#     parser = argparse.ArgumentParser(description="Adaptive RAG router for Milvus API")

#     parser.add_argument("question", nargs="?", help="Один вопрос для запуска")

#     parser.add_argument("--chat", action="store_true", help="Интерактивный режим")

#     parser.add_argument("--show-context", action="store_true", help="Показывать контекст")

#     parser.add_argument(
#         "--context-limit",
#         type=int,
#         default=0,
#         help="Обрезать контекст до N символов (0 = без обрезки)",
#     )

#     args = parser.parse_args()

#     if args.chat:
#         chat_loop(show_context=args.show_context, context_limit=args.context_limit)
#         return

#     if args.question:
#         result = adaptive_search(args.question)
#         print_result(result, show_context=args.show_context, context_limit=args.context_limit)
#         return

#     run_default_tests(show_context=True, context_limit=3000)


# if __name__ == "__main__":
#     main()


# # router.py
# from __future__ import annotations

# import json
# import argparse
# import re
# from typing import Any, Dict, List

# from classifier import classify_question
# from milvus_client import MilvusApiClient
# from answer_generator import generate_answer
# from sources import extract_sources


# def build_search_payload(question_type: str) -> Dict[str, Any]:

#     if question_type == "fact":
#         return {
#             "mode": "dense",
#             "level": [1, 2],
#             "limit": 5,
#             "use_summary": False,
#         }

#     if question_type == "definition":
#         return {
#             "mode": "hybrid",
#             "level": [1, 2],
#             "limit": 6,
#             "use_summary": True,
#         }

#     if question_type == "procedure":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1, 2],
#             "limit": 8,
#             "use_summary": True,
#         }

#     if question_type == "norm_reference":
#         return {
#             "mode": "sparse",
#             "level": [1, 2],
#             "limit": 8,
#             "use_summary": False,
#         }

#     if question_type == "broad_overview":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1],
#             "limit": 6,
#             "use_summary": True,
#         }

#     return {
#         "mode": "hybrid",
#         "level": [0, 1, 2],
#         "limit": 5,
#         "use_summary": True,
#     }


# def format_sources(sources: list[str]) -> str:

#     if not sources:
#         return "Источники: не найдены"

#     lines = ["Источники:"]
#     for src in sources:
#         lines.append(f"• {src}")

#     return "\n".join(lines)


# def _natural_number_key(value: str) -> List[Any]:
#     """
#     Сортировка номеров типа:
#     8, 8.1, 8.2, 10.4.3
#     """
#     if value is None:
#         return [999999]
#     parts = re.split(r"[^\d]+", str(value))
#     nums = [int(p) for p in parts if p.isdigit()]
#     return nums if nums else [999999]


# def _build_context_from_rows(rows: List[Dict[str, Any]]) -> str:
#     blocks = []

#     for row in rows:
#         number = row.get("number")
#         title = row.get("title")
#         text = row.get("text", "")

#         header = ""
#         if number and title:
#             header = f"## {number} {title}"
#         elif title:
#             header = f"## {title}"
#         elif number:
#             header = f"## {number}"

#         if header:
#             blocks.append(f"{header}\n{text}".strip())
#         else:
#             blocks.append(str(text).strip())

#     return "\n\n".join(b for b in blocks if b.strip())


# def _maybe_expand_context(
#     client: MilvusApiClient,
#     question_type: str,
#     results: List[Dict[str, Any]],
#     fallback_context: str,
# ) -> str:
#     """
#     Если top-hit — section level=1, пытаемся через /query подтянуть весь раздел:
#     level 1 + все level 2 внутри section_id.
#     Это особенно полезно для требований, правил, процедур.
#     """

#     if not results:
#         return fallback_context

#     top = results[0]
#     top_level = top.get("level")
#     top_section_id = top.get("section_id")
#     top_doc_id = top.get("doc_id")

#     if top_level != 1 or not top_section_id or not top_doc_id:
#         return fallback_context

#     if question_type not in {"fact", "procedure", "broad_overview"}:
#         return fallback_context

#     try:
#         query_result = client.query(
#             collection="documents",
#             filter_expr=f"doc_id == '{top_doc_id}' && section_id == '{top_section_id}' && level in [1, 2]",
#             limit=50,
#             output_fields=[
#                 "doc_id",
#                 "section_id",
#                 "level",
#                 "title",
#                 "number",
#                 "text",
#             ],
#         )

#         rows = query_result.get("results", [])
#         if not rows:
#             return fallback_context

#         rows.sort(key=lambda x: (_natural_number_key(x.get("number")), x.get("level", 999)))

#         expanded_context = _build_context_from_rows(rows)
#         if expanded_context.strip():
#             return expanded_context

#         return fallback_context

#     except Exception:
#         return fallback_context


# def adaptive_search(question: str) -> Dict[str, Any]:

#     classification = classify_question(question)
#     question_type = classification["question_type"]

#     payload = build_search_payload(question_type)

#     client = MilvusApiClient()

#     search_result = client.search(
#         text=question,
#         mode=payload["mode"],
#         level=payload["level"],
#         limit=payload["limit"],
#         use_summary=payload["use_summary"],
#     )

#     raw_context = search_result.get("context", "")
#     results = search_result.get("results", [])

#     context = _maybe_expand_context(
#         client=client,
#         question_type=question_type,
#         results=results,
#         fallback_context=raw_context,
#     )

#     if context.strip():
#         answer = generate_answer(
#             question=question,
#             context=context,
#             question_type=question_type,
#         )
#     else:
#         answer = "В документах нет информации по этому вопросу."

#     sources = extract_sources(results)[:3]

#     answer_with_sources = answer.strip()

#     if sources:
#         answer_with_sources += "\n\n" + format_sources(sources)
#     else:
#         answer_with_sources += "\n\nИсточники: не найдены"

#     return {
#         "question": question,
#         "question_type": question_type,
#         "classification": classification,
#         "search_payload": payload,
#         "results": results,
#         "context": context,
#         "answer": answer_with_sources,
#         "sources": sources,
#     }


# def print_result(result: Dict[str, Any], show_context: bool = True, context_limit: int = 0) -> None:

#     print("=" * 100)

#     print("QUESTION:", result["question"])

#     print("CLASSIFICATION:")
#     print(json.dumps(result["classification"], ensure_ascii=False, indent=2))

#     print("SEARCH PAYLOAD:")
#     print(json.dumps(result["search_payload"], ensure_ascii=False, indent=2))

#     print("TOP HITS COUNT:", len(result["results"]))

#     print("\nANSWER:")
#     print(result["answer"])

#     if show_context:

#         print("\nCONTEXT:")

#         context = result["context"]

#         if context_limit > 0 and len(context) > context_limit:
#             print(context[:context_limit] + "\n...[TRUNCATED]...")
#         else:
#             print(context)

#     print()


# def chat_loop(show_context: bool = False, context_limit: int = 0) -> None:

#     print("💬 Adaptive RAG chat mode. Пустая строка — выход.")

#     while True:

#         try:
#             question = input("\n❓ Вопрос: ").strip()
#         except (EOFError, KeyboardInterrupt):
#             print("\n👋 Выход.")
#             break

#         if not question:
#             print("👋 Выход.")
#             break

#         try:
#             result = adaptive_search(question)
#             print_result(result, show_context=show_context, context_limit=context_limit)
#         except Exception as e:
#             print(f"Ошибка: {e}")


# def run_default_tests(show_context: bool = True, context_limit: int = 3000) -> None:

#     test_questions = [
#         "Какие требования к оперативной памяти?",
#         "Какие требования к транспортированию отходов?",
#         "Как у нас проходит закупка оборудования от начала до конца?",
#         "Где прописана процедура ПТП?",
#         "Какие задачи у сотрудников отдела геологии?",
#     ]

#     for q in test_questions:
#         result = adaptive_search(q)
#         print_result(result, show_context=show_context, context_limit=context_limit)


# def main():

#     parser = argparse.ArgumentParser(description="Adaptive RAG router for Milvus API")

#     parser.add_argument("question", nargs="?", help="Один вопрос для запуска")

#     parser.add_argument("--chat", action="store_true", help="Интерактивный режим")

#     parser.add_argument("--show-context", action="store_true", help="Показывать контекст")

#     parser.add_argument(
#         "--context-limit",
#         type=int,
#         default=0,
#         help="Обрезать контекст до N символов (0 = без обрезки)",
#     )

#     args = parser.parse_args()

#     if args.chat:
#         chat_loop(show_context=args.show_context, context_limit=args.context_limit)
#         return

#     if args.question:
#         result = adaptive_search(args.question)
#         print_result(result, show_context=args.show_context, context_limit=args.context_limit)
#         return

#     run_default_tests(show_context=True, context_limit=3000)


# if __name__ == "__main__":
#     main()


# # router.py
# from __future__ import annotations

# import json
# import argparse
# import re
# from typing import Any, Dict, List

# from classifier import classify_question
# from milvus_client import MilvusApiClient
# from answer_generator import generate_answer
# from sources import extract_sources


# def build_search_payload(question_type: str, answer_mode: str) -> Dict[str, Any]:
#     """
#     Собирает payload для /search на основе типа вопроса и ожидаемого формата ответа.
#     """

#     if question_type == "fact":
#         if answer_mode == "list":
#             return {
#                 "mode": "hybrid",
#                 "level": [1, 2],
#                 "limit": 8,
#                 "use_summary": True,
#             }
#         return {
#             "mode": "dense",
#             "level": [1, 2],
#             "limit": 5,
#             "use_summary": False,
#         }

#     if question_type == "definition":
#         return {
#             "mode": "hybrid",
#             "level": [1, 2],
#             "limit": 6,
#             "use_summary": True,
#         }

#     if question_type == "procedure":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1, 2],
#             "limit": 8,
#             "use_summary": True,
#         }

#     if question_type == "norm_reference":
#         return {
#             "mode": "sparse",
#             "level": [1, 2],
#             "limit": 8,
#             "use_summary": False,
#         }

#     if question_type == "broad_overview":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1],
#             "limit": 6,
#             "use_summary": True,
#         }

#     return {
#         "mode": "hybrid",
#         "level": [0, 1, 2],
#         "limit": 5,
#         "use_summary": True,
#     }


# def format_sources(sources: list[str]) -> str:
#     if not sources:
#         return "Источники: не найдены"

#     lines = ["Источники:"]
#     for src in sources:
#         lines.append(f"• {src}")
#     return "\n".join(lines)


# def _natural_number_key(value: str) -> List[Any]:
#     """
#     Сортировка номеров типа:
#     8, 8.1, 8.2, 10.4.3
#     """
#     if value is None:
#         return [999999]
#     parts = re.split(r"[^\d]+", str(value))
#     nums = [int(p) for p in parts if p.isdigit()]
#     return nums if nums else [999999]


# def _build_context_from_rows(rows: List[Dict[str, Any]]) -> str:
#     blocks = []

#     for row in rows:
#         number = row.get("number")
#         title = row.get("title")
#         text = row.get("text", "")

#         header = ""
#         if number and title:
#             header = f"## {number} {title}"
#         elif title:
#             header = f"## {title}"
#         elif number:
#             header = f"## {number}"

#         if header:
#             blocks.append(f"{header}\n{text}".strip())
#         else:
#             blocks.append(str(text).strip())

#     return "\n\n".join(b for b in blocks if b.strip())


# def _maybe_expand_context(
#     client: MilvusApiClient,
#     question_type: str,
#     answer_mode: str,
#     results: List[Dict[str, Any]],
#     fallback_context: str,
# ) -> str:
#     """
#     Если top-hit — section level=1, пытаемся через /query подтянуть весь раздел:
#     level 1 + все level 2 внутри section_id.
#     Это особенно полезно для списков требований, правил, процедур и обзорных вопросов.
#     """

#     if not results:
#         return fallback_context

#     top = results[0]
#     top_level = top.get("level")
#     top_section_id = top.get("section_id")
#     top_doc_id = top.get("doc_id")

#     if top_level != 1 or not top_section_id or not top_doc_id:
#         return fallback_context

#     # Расширяем контекст, если ожидается список/шаги или если это procedural/overview запрос
#     should_expand = (
#         question_type in {"procedure", "broad_overview"}
#         or answer_mode in {"list", "steps"}
#         or (question_type == "fact" and answer_mode == "list")
#     )

#     if not should_expand:
#         return fallback_context

#     try:
#         query_result = client.query(
#             collection="documents",
#             filter_expr=f"doc_id == '{top_doc_id}' && section_id == '{top_section_id}' && level in [1, 2]",
#             limit=50,
#             output_fields=[
#                 "doc_id",
#                 "section_id",
#                 "level",
#                 "title",
#                 "number",
#                 "text",
#             ],
#         )

#         rows = query_result.get("results", [])
#         if not rows:
#             return fallback_context

#         rows.sort(key=lambda x: (_natural_number_key(x.get("number")), x.get("level", 999)))

#         expanded_context = _build_context_from_rows(rows)
#         if expanded_context.strip():
#             return expanded_context

#         return fallback_context

#     except Exception:
#         return fallback_context


# def adaptive_search(question: str) -> Dict[str, Any]:
#     classification = classify_question(question)
#     question_type = classification["question_type"]
#     answer_mode = classification["answer_mode"]

#     payload = build_search_payload(question_type, answer_mode)

#     client = MilvusApiClient()

#     search_result = client.search(
#         text=question,
#         mode=payload["mode"],
#         level=payload["level"],
#         limit=payload["limit"],
#         use_summary=payload["use_summary"],
#     )

#     raw_context = search_result.get("context", "")
#     results = search_result.get("results", [])

#     context = _maybe_expand_context(
#         client=client,
#         question_type=question_type,
#         answer_mode=answer_mode,
#         results=results,
#         fallback_context=raw_context,
#     )

#     if context.strip():
#         answer = generate_answer(
#             question=question,
#             context=context,
#             question_type=question_type,
#             answer_mode=answer_mode,
#         )
#     else:
#         answer = "В документах нет информации по этому вопросу."

#     sources = extract_sources(results)[:3]

#     answer_with_sources = answer.strip()

#     if sources:
#         answer_with_sources += "\n\n" + format_sources(sources)
#     else:
#         answer_with_sources += "\n\nИсточники: не найдены"

#     return {
#         "question": question,
#         "question_type": question_type,
#         "answer_mode": answer_mode,
#         "classification": classification,
#         "search_payload": payload,
#         "results": results,
#         "context": context,
#         "answer": answer_with_sources,
#         "sources": sources,
#     }


# def print_result(result: Dict[str, Any], show_context: bool = True, context_limit: int = 0) -> None:
#     print("=" * 100)

#     print("QUESTION:", result["question"])

#     print("CLASSIFICATION:")
#     print(json.dumps(result["classification"], ensure_ascii=False, indent=2))

#     print("SEARCH PAYLOAD:")
#     print(json.dumps(result["search_payload"], ensure_ascii=False, indent=2))

#     print("TOP HITS COUNT:", len(result["results"]))

#     print("\nANSWER:")
#     print(result["answer"])

#     if show_context:
#         print("\nCONTEXT:")
#         context = result["context"]

#         if context_limit > 0 and len(context) > context_limit:
#             print(context[:context_limit] + "\n...[TRUNCATED]...")
#         else:
#             print(context)

#     print()


# def chat_loop(show_context: bool = False, context_limit: int = 0) -> None:
#     print("💬 Adaptive RAG chat mode. Пустая строка — выход.")

#     while True:
#         try:
#             question = input("\n❓ Вопрос: ").strip()
#         except (EOFError, KeyboardInterrupt):
#             print("\n👋 Выход.")
#             break

#         if not question:
#             print("👋 Выход.")
#             break

#         try:
#             result = adaptive_search(question)
#             print_result(result, show_context=show_context, context_limit=context_limit)
#         except Exception as e:
#             print(f"Ошибка: {e}")


# def run_default_tests(show_context: bool = True, context_limit: int = 3000) -> None:
#     test_questions = [
#         "Какие требования к оперативной памяти?",
#         "Какие требования к транспортированию отходов?",
#         "Как у нас проходит закупка оборудования от начала до конца?",
#         "Где прописана процедура ПТП?",
#         "Какие задачи у сотрудников отдела геологии?",
#     ]

#     for q in test_questions:
#         result = adaptive_search(q)
#         print_result(result, show_context=show_context, context_limit=context_limit)


# def main():
#     parser = argparse.ArgumentParser(description="Adaptive RAG router for Milvus API")

#     parser.add_argument("question", nargs="?", help="Один вопрос для запуска")
#     parser.add_argument("--chat", action="store_true", help="Интерактивный режим")
#     parser.add_argument("--show-context", action="store_true", help="Показывать контекст")
#     parser.add_argument(
#         "--context-limit",
#         type=int,
#         default=0,
#         help="Обрезать контекст до N символов (0 = без обрезки)",
#     )

#     args = parser.parse_args()

#     if args.chat:
#         chat_loop(show_context=args.show_context, context_limit=args.context_limit)
#         return

#     if args.question:
#         result = adaptive_search(args.question)
#         print_result(result, show_context=args.show_context, context_limit=args.context_limit)
#         return

#     run_default_tests(show_context=True, context_limit=3000)


# if __name__ == "__main__":
#     main()


# # router.py
# from __future__ import annotations

# import json
# import argparse
# import re
# from typing import Any, Dict, List

# import requests

# from config import LOCAL_LLM_MODEL
# from classifier import classify_question
# from milvus_client import MilvusApiClient
# from answer_generator import generate_answer
# from sources import extract_sources


# OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


# def rewrite_query(question: str) -> str:
#     """
#     Безопасный query rewrite.

#     Правила:
#     - нельзя добавлять новые сущности
#     - нельзя менять аббревиатуры
#     - если rewrite подозрительный → возвращаем исходный вопрос
#     """

#     prompt = f"""
#     Переформулируй вопрос для поиска по нормативным документам.

#     Правила:
#     1. Сохрани исходный смысл.
#     2. Сделай формулировку чуть более формальной.
#     3. НЕ добавляй новые слова, которых нет в вопросе.
#     4. НЕ добавляй документы, ГОСТы, стандарты.
#     5. НЕ меняй аббревиатуры.
#     6. Верни одну короткую строку.

#     Вопрос:
#     {question}

#     Переформулированный запрос:
#     """.strip()

#     payload = {
#         "model": LOCAL_LLM_MODEL,
#         "prompt": prompt,
#         "stream": False,
#         "options": {
#             "temperature": 0
#         }
#     }

#     session = requests.Session()
#     session.trust_env = False

#     response = session.post(OLLAMA_URL, json=payload, timeout=120)
#     response.raise_for_status()

#     result = response.json()
#     rewritten = result["response"].strip()

#     if not rewritten:
#         return question

#     # --- SAFETY CHECKS ---

#     q_tokens = set(question.lower().split())
#     r_tokens = set(rewritten.lower().split())

#     # если появились новые токены → отменяем rewrite
#     if len(r_tokens - q_tokens) > 2:
#         return question

#     # если rewrite слишком длинный → отменяем
#     if len(rewritten) > len(question) * 1.5:
#         return question

#     # если модель вставила ГОСТ / стандарт
#     forbidden = ["гост", "iso", "стандарт", "регламент"]
#     if any(f in rewritten.lower() for f in forbidden):
#         return question

#     return rewritten


# def build_search_payload(question_type: str, answer_mode: str) -> Dict[str, Any]:
#     if question_type == "fact":
#         if answer_mode == "list":
#             return {
#                 "mode": "hybrid",
#                 "level": [1, 2],
#                 "limit": 8,
#                 "use_summary": True,
#             }
#         return {
#             "mode": "dense",
#             "level": [1, 2],
#             "limit": 5,
#             "use_summary": False,
#         }

#     if question_type == "definition":
#         return {
#             "mode": "hybrid",
#             "level": [1, 2],
#             "limit": 6,
#             "use_summary": True,
#         }

#     if question_type == "procedure":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1, 2],
#             "limit": 8,
#             "use_summary": True,
#         }

#     if question_type == "norm_reference":
#         return {
#             "mode": "hybrid",
#             "level": [1, 2],
#             "limit": 5,
#             "use_summary": True,
#         }

#     if question_type == "broad_overview":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1],
#             "limit": 6,
#             "use_summary": True,
#         }

#     return {
#         "mode": "hybrid",
#         "level": [0, 1, 2],
#         "limit": 5,
#         "use_summary": True,
#     }


# def format_sources(sources: list[str]) -> str:
#     if not sources:
#         return "Источники: не найдены"

#     lines = ["Источники:"]
#     for src in sources:
#         lines.append(f"• {src}")
#     return "\n".join(lines)


# def _natural_number_key(value: str) -> List[Any]:
#     if value is None:
#         return [999999]
#     parts = re.split(r"[^\d]+", str(value))
#     nums = [int(p) for p in parts if p.isdigit()]
#     return nums if nums else [999999]


# def _build_context_from_rows(rows: List[Dict[str, Any]]) -> str:
#     blocks = []

#     for row in rows:
#         number = row.get("number")
#         title = row.get("title")
#         text = row.get("text", "")

#         header = ""
#         if number and title:
#             header = f"## {number} {title}"
#         elif title:
#             header = f"## {title}"
#         elif number:
#             header = f"## {number}"

#         if header:
#             blocks.append(f"{header}\n{text}".strip())
#         else:
#             blocks.append(str(text).strip())

#     return "\n\n".join(b for b in blocks if b.strip())


# def _extract_important_tokens(question: str) -> list[str]:
#     """
#     Важные токены для norm_reference:
#     - коды документов
#     - аббревиатуры
#     """
#     tokens = set()

#     doc_codes = re.findall(r"\b[А-ЯA-Z]{2,}-\d{2}(?:-\w+)?\b", question, flags=re.UNICODE)
#     for t in doc_codes:
#         tokens.add(t.strip())

#     abbrevs = re.findall(r"\b[А-ЯA-Z]{2,6}\b", question, flags=re.UNICODE)
#     for t in abbrevs:
#         tokens.add(t.strip())

#     return sorted(tokens)


# def _results_contain_important_token(results: list[dict], tokens: list[str]) -> bool:
#     if not tokens or not results:
#         return False

#     corpus = []
#     for r in results:
#         corpus.append(str(r.get("title", "")))
#         corpus.append(str(r.get("text", "")))

#     joined = "\n".join(corpus).lower()

#     for token in tokens:
#         if token.lower() in joined:
#             return True

#     return False


# def _run_search(client: MilvusApiClient, query_text: str, payload: dict) -> dict:
#     return client.search(
#         text=query_text,
#         mode=payload["mode"],
#         level=payload["level"],
#         limit=payload["limit"],
#         use_summary=payload["use_summary"],
#     )


# def _build_reference_context(results: List[Dict[str, Any]], sources: List[str]) -> str:
#     """
#     Короткий контекст для norm_reference:
#     только карточки кандидатов, без длинной простыни.
#     """
#     blocks = []

#     for i, row in enumerate(results[:5]):
#         title = row.get("title", "")
#         number = row.get("number", "")
#         text = str(row.get("text", "")).strip()
#         source = sources[i] if i < len(sources) else "Неизвестный источник"

#         short_text = text
#         if len(short_text) > 500:
#             short_text = short_text[:500] + "..."

#         block = (
#             f"Источник: {source}\n"
#             f"Раздел: {title}\n"
#             f"Номер: {number}\n"
#             f"Фрагмент: {short_text}"
#         )
#         blocks.append(block)

#     return "\n\n".join(blocks)


# def _maybe_expand_context(
#     client: MilvusApiClient,
#     question_type: str,
#     answer_mode: str,
#     results: List[Dict[str, Any]],
#     fallback_context: str,
# ) -> str:
#     if not results:
#         return fallback_context

#     top = results[0]
#     top_level = top.get("level")
#     top_section_id = top.get("section_id")
#     top_doc_id = top.get("doc_id")

#     if top_level != 1 or not top_section_id or not top_doc_id:
#         return fallback_context

#     should_expand = (
#         question_type in {"procedure", "broad_overview"}
#         or answer_mode in {"list", "steps"}
#         or (question_type == "fact" and answer_mode == "list")
#     )

#     if not should_expand:
#         return fallback_context

#     try:
#         query_result = client.query(
#             collection="documents",
#             filter_expr=f"doc_id == '{top_doc_id}' && section_id == '{top_section_id}' && level in [1, 2]",
#             limit=50,
#             output_fields=[
#                 "doc_id",
#                 "section_id",
#                 "level",
#                 "title",
#                 "number",
#                 "text",
#             ],
#         )

#         rows = query_result.get("results", [])
#         if not rows:
#             return fallback_context

#         rows.sort(key=lambda x: (_natural_number_key(x.get("number")), x.get("level", 999)))

#         expanded_context = _build_context_from_rows(rows)
#         if expanded_context.strip():
#             return expanded_context

#         return fallback_context

#     except Exception:
#         return fallback_context


# def adaptive_search(question: str) -> Dict[str, Any]:
#     classification = classify_question(question)
#     question_type = classification["question_type"]
#     answer_mode = classification["answer_mode"]

#     payload = build_search_payload(question_type, answer_mode)
#     client = MilvusApiClient()

#     important_tokens = _extract_important_tokens(question)

#     if question_type == "norm_reference":
#         primary_query = question
#         primary_result = _run_search(client, primary_query, payload)
#         primary_results = primary_result.get("results", [])

#         if important_tokens and not _results_contain_important_token(primary_results, important_tokens):
#             rewritten_query = rewrite_query(question)
#             rewritten_result = _run_search(client, rewritten_query, payload)
#             rewritten_results = rewritten_result.get("results", [])

#             if _results_contain_important_token(rewritten_results, important_tokens):
#                 search_query = rewritten_query
#                 search_result = rewritten_result
#             else:
#                 search_query = primary_query
#                 search_result = primary_result
#         else:
#             search_query = primary_query
#             search_result = primary_result
#     else:
#         search_query = rewrite_query(question)
#         search_result = _run_search(client, search_query, payload)

#     raw_context = search_result.get("context", "")
#     results = search_result.get("results", [])

#     all_sources = extract_sources(results)
#     sources = all_sources[:3]

#     if question_type == "norm_reference":
#         context = _build_reference_context(results, all_sources)
#     else:
#         context = _maybe_expand_context(
#             client=client,
#             question_type=question_type,
#             answer_mode=answer_mode,
#             results=results,
#             fallback_context=raw_context,
#         )

#     if context.strip():
#         answer = generate_answer(
#             question=question,
#             context=context,
#             question_type=question_type,
#             answer_mode=answer_mode,
#         )
#     else:
#         answer = "В документах нет информации по этому вопросу."

#     answer_with_sources = answer.strip()

#     if sources:
#         answer_with_sources += "\n\n" + format_sources(sources)
#     else:
#         answer_with_sources += "\n\nИсточники: не найдены"

#     return {
#         "question": question,
#         "search_query": search_query,
#         "question_type": question_type,
#         "answer_mode": answer_mode,
#         "classification": classification,
#         "search_payload": payload,
#         "results": results,
#         "context": context,
#         "answer": answer_with_sources,
#         "sources": sources,
#     }


# def print_result(result: Dict[str, Any], show_context: bool = True, context_limit: int = 0) -> None:
#     print("=" * 100)

#     print("QUESTION:", result["question"])
#     print("SEARCH QUERY:", result["search_query"])

#     print("CLASSIFICATION:")
#     print(json.dumps(result["classification"], ensure_ascii=False, indent=2))

#     print("SEARCH PAYLOAD:")
#     print(json.dumps(result["search_payload"], ensure_ascii=False, indent=2))

#     print("TOP HITS COUNT:", len(result["results"]))

#     print("\nANSWER:")
#     print(result["answer"])

#     if show_context:
#         print("\nCONTEXT:")
#         context = result["context"]

#         if context_limit > 0 and len(context) > context_limit:
#             print(context[:context_limit] + "\n...[TRUNCATED]...")
#         else:
#             print(context)

#     print()


# def chat_loop(show_context: bool = False, context_limit: int = 0) -> None:
#     print("💬 Adaptive RAG chat mode. Пустая строка — выход.")

#     while True:
#         try:
#             question = input("\n❓ Вопрос: ").strip()
#         except (EOFError, KeyboardInterrupt):
#             print("\n👋 Выход.")
#             break

#         if not question:
#             print("👋 Выход.")
#             break

#         try:
#             result = adaptive_search(question)
#             print_result(result, show_context=show_context, context_limit=context_limit)
#         except Exception as e:
#             print(f"Ошибка: {e}")


# def run_default_tests(show_context: bool = True, context_limit: int = 3000) -> None:
#     test_questions = [
#         "Какие требования к оперативной памяти?",
#         "Какие требования к транспортированию отходов?",
#         "Как у нас проходит закупка оборудования от начала до конца?",
#         "Где прописана процедура ПТП?",
#         "Какие задачи у сотрудников отдела геологии?",
#     ]

#     for q in test_questions:
#         result = adaptive_search(q)
#         print_result(result, show_context=show_context, context_limit=context_limit)


# def main():
#     parser = argparse.ArgumentParser(description="Adaptive RAG router for Milvus API")

#     parser.add_argument("question", nargs="?", help="Один вопрос для запуска")
#     parser.add_argument("--chat", action="store_true", help="Интерактивный режим")
#     parser.add_argument("--show-context", action="store_true", help="Показывать контекст")
#     parser.add_argument(
#         "--context-limit",
#         type=int,
#         default=0,
#         help="Обрезать контекст до N символов (0 = без обрезки)",
#     )

#     args = parser.parse_args()

#     if args.chat:
#         chat_loop(show_context=args.show_context, context_limit=args.context_limit)
#         return

#     if args.question:
#         result = adaptive_search(args.question)
#         print_result(result, show_context=args.show_context, context_limit=args.context_limit)
#         return

#     run_default_tests(show_context=True, context_limit=3000)


# if __name__ == "__main__":
#     main()


# # router.py
# from __future__ import annotations

# import json
# import argparse
# import re
# from typing import Any, Dict, List

# import requests

# from config import LOCAL_LLM_MODEL
# from classifier import classify_question
# from milvus_client import MilvusApiClient
# from answer_generator import generate_answer
# from sources import extract_sources


# OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


# def rewrite_query(question: str) -> str:
#     prompt = f"""
# Переформулируй вопрос для поиска по нормативным документам.

# Правила:
# 1. Сохрани исходный смысл.
# 2. Сделай формулировку чуть более формальной.
# 3. НЕ добавляй новые слова, которых нет в вопросе.
# 4. НЕ добавляй документы, ГОСТы, стандарты.
# 5. НЕ меняй аббревиатуры.
# 6. Верни одну короткую строку.

# Вопрос:
# {question}

# Переформулированный запрос:
# """.strip()

#     payload = {
#         "model": LOCAL_LLM_MODEL,
#         "prompt": prompt,
#         "stream": False,
#         "options": {"temperature": 0},
#     }

#     session = requests.Session()
#     session.trust_env = False

#     response = session.post(OLLAMA_URL, json=payload, timeout=120)
#     response.raise_for_status()

#     result = response.json()
#     rewritten = result["response"].strip()

#     if not rewritten:
#         return question

#     q_tokens = set(question.lower().split())
#     r_tokens = set(rewritten.lower().split())

#     if len(r_tokens - q_tokens) > 2:
#         return question

#     if len(rewritten) > len(question) * 1.5:
#         return question

#     forbidden = ["гост", "iso", "стандарт", "регламент"]
#     if any(f in rewritten.lower() for f in forbidden):
#         return question

#     return rewritten


# def build_search_payload(question_type: str, answer_mode: str) -> Dict[str, Any]:
#     if question_type == "fact":
#         if answer_mode == "list":
#             return {
#                 "mode": "hybrid",
#                 "level": [1, 2],
#                 "limit": 8,
#                 "use_summary": True,
#             }
#         return {
#             "mode": "dense",
#             "level": [1, 2],
#             "limit": 5,
#             "use_summary": False,
#         }

#     if question_type == "definition":
#         return {
#             "mode": "hybrid",
#             "level": [1, 2],
#             "limit": 6,
#             "use_summary": True,
#         }

#     if question_type == "procedure":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1, 2],
#             "limit": 10,
#             "use_summary": True,
#         }

#     if question_type == "norm_reference":
#         return {
#             "mode": "hybrid",
#             "level": [1, 2],
#             "limit": 5,
#             "use_summary": True,
#         }

#     if question_type == "broad_overview":
#         return {
#             "mode": "hybrid",
#             "level": [0, 1],
#             "limit": 6,
#             "use_summary": True,
#         }

#     return {
#         "mode": "hybrid",
#         "level": [0, 1, 2],
#         "limit": 5,
#         "use_summary": True,
#     }


# def format_sources(sources: list[str]) -> str:
#     if not sources:
#         return "Источники: не найдены"

#     lines = ["Источники:"]
#     for src in sources:
#         lines.append(f"• {src}")
#     return "\n".join(lines)


# def _natural_number_key(value: str) -> List[Any]:
#     if value is None:
#         return [999999]
#     parts = re.split(r"[^\d]+", str(value))
#     nums = [int(p) for p in parts if p.isdigit()]
#     return nums if nums else [999999]


# def _build_context_from_rows(rows: List[Dict[str, Any]]) -> str:
#     blocks = []

#     for row in rows:
#         number = row.get("number")
#         title = row.get("title")
#         text = row.get("text", "")

#         header = ""
#         if number and title:
#             header = f"## {number} {title}"
#         elif title:
#             header = f"## {title}"
#         elif number:
#             header = f"## {number}"

#         if header:
#             blocks.append(f"{header}\n{text}".strip())
#         else:
#             blocks.append(str(text).strip())

#     return "\n\n".join(b for b in blocks if b.strip())


# def _extract_important_tokens(question: str) -> list[str]:
#     tokens = set()

#     doc_codes = re.findall(r"\b[А-ЯA-Z]{2,}-\d{2}(?:-\w+)?\b", question, flags=re.UNICODE)
#     for t in doc_codes:
#         tokens.add(t.strip())

#     abbrevs = re.findall(r"\b[А-ЯA-Z]{2,6}\b", question, flags=re.UNICODE)
#     for t in abbrevs:
#         tokens.add(t.strip())

#     return sorted(tokens)


# def _results_contain_important_token(results: list[dict], tokens: list[str]) -> bool:
#     if not tokens or not results:
#         return False

#     corpus = []
#     for r in results:
#         corpus.append(str(r.get("title", "")))
#         corpus.append(str(r.get("text", "")))

#     joined = "\n".join(corpus).lower()

#     for token in tokens:
#         if token.lower() in joined:
#             return True

#     return False


# def _run_search(client: MilvusApiClient, query_text: str, payload: dict) -> dict:
#     return client.search(
#         text=query_text,
#         mode=payload["mode"],
#         level=payload["level"],
#         limit=payload["limit"],
#         use_summary=payload["use_summary"],
#     )


# def _build_reference_context(results: List[Dict[str, Any]], sources: List[str]) -> str:
#     blocks = []

#     for i, row in enumerate(results[:5]):
#         title = row.get("title", "")
#         number = row.get("number", "")
#         text = str(row.get("text", "")).strip()
#         source = sources[i] if i < len(sources) else "Неизвестный источник"

#         short_text = text[:500] + "..." if len(text) > 500 else text

#         block = (
#             f"Источник: {source}\n"
#             f"Раздел: {title}\n"
#             f"Номер: {number}\n"
#             f"Фрагмент: {short_text}"
#         )
#         blocks.append(block)

#     return "\n\n".join(blocks)


# def _procedure_doc_score(question: str, row: Dict[str, Any]) -> float:
#     q = question.lower()
#     title = str(row.get("title", "")).lower()
#     text = str(row.get("text", "")).lower()
#     score = float(row.get("score", 0.0) or 0.0)

#     bonus = 0.0

#     positive = [
#         "порядок",
#         "внешн",
#         "постав",
#         "закуп",
#         "приобрет",
#         "получение",
#         "согласование",
#         "действий",
#     ]

#     negative = [
#         "верификац",
#         "контроль",
#         "приемк",
#         "архив",
#         "регистрац",
#         "перечень программного обеспечения",
#     ]

#     for p in positive:
#         if p in title:
#             bonus += 2.5
#         elif p in text:
#             bonus += 0.3

#     for p in negative:
#         if p in title:
#             bonus -= 2.0
#         elif p in text:
#             bonus -= 0.2

#     if "от начала до конца" in q:
#         if "верификац" in title:
#             bonus -= 3.0

#     return score + bonus


# def _select_best_procedure_doc(question: str, results: List[Dict[str, Any]]) -> str | None:
#     if not results:
#         return None

#     best_doc_id = None
#     best_score = float("-inf")

#     for row in results:
#         doc_id = row.get("doc_id")
#         if not doc_id:
#             continue

#         row_score = _procedure_doc_score(question, row)
#         if row_score > best_score:
#             best_score = row_score
#             best_doc_id = doc_id

#     return best_doc_id


# def _filter_procedure_rows(rows: List[Dict[str, Any]], question: str) -> List[Dict[str, Any]]:
#     """
#     Оставляем только procedural-части документа.
#     """
#     selected = []

#     positive = [
#         "порядок",
#         "внешн",
#         "постав",
#         "закуп",
#         "приобрет",
#         "получение",
#         "согласование",
#         "действий",
#         "верификация",
#     ]

#     negative_hard = [
#         "список рассылки",
#         "перечень программного обеспечения",
#         "термины",
#         "сокращения",
#         "приложение",
#     ]

#     for row in rows:
#         title = str(row.get("title", "")).lower()
#         text = str(row.get("text", "")).lower()
#         level = row.get("level")

#         if any(bad in title for bad in negative_hard):
#             continue

#         if level == 1:
#             if any(p in title for p in positive):
#                 selected.append(row)
#                 continue

#         if level == 2:
#             if any(p in title for p in positive) or any(p in text for p in positive):
#                 selected.append(row)
#                 continue

#     # fallback: если ничего не выбрали, оставим исходные
#     if not selected:
#         return rows

#     return selected


# def _build_procedure_context(
#     client: MilvusApiClient,
#     question: str,
#     results: List[Dict[str, Any]],
#     fallback_context: str,
# ) -> str:
#     """
#     Для procedure берём лучший ДОКУМЕНТ, а не один section.
#     Потом вытягиваем все level 1/2 этого документа и фильтруем по procedural-частям.
#     """
#     best_doc_id = _select_best_procedure_doc(question, results)
#     if not best_doc_id:
#         return fallback_context

#     try:
#         query_result = client.query(
#             collection="documents",
#             filter_expr=f"doc_id == '{best_doc_id}' && level in [1, 2]",
#             limit=200,
#             output_fields=[
#                 "doc_id",
#                 "section_id",
#                 "level",
#                 "title",
#                 "number",
#                 "text",
#             ],
#         )

#         rows = query_result.get("results", [])
#         if not rows:
#             return fallback_context

#         rows = _filter_procedure_rows(rows, question)
#         rows.sort(key=lambda x: (_natural_number_key(x.get("number")), x.get("level", 999)))

#         context = _build_context_from_rows(rows)
#         return context if context.strip() else fallback_context

#     except Exception:
#         return fallback_context


# def _maybe_expand_context(
#     client: MilvusApiClient,
#     question: str,
#     question_type: str,
#     answer_mode: str,
#     results: List[Dict[str, Any]],
#     fallback_context: str,
# ) -> str:
#     if not results:
#         return fallback_context

#     if question_type == "procedure" or answer_mode == "steps":
#         return _build_procedure_context(client, question, results, fallback_context)

#     should_expand = (
#         question_type in {"broad_overview"}
#         or answer_mode in {"list"}
#         or (question_type == "fact" and answer_mode == "list")
#     )

#     if not should_expand:
#         return fallback_context

#     top = results[0]
#     top_level = top.get("level")
#     top_section_id = top.get("section_id")
#     top_doc_id = top.get("doc_id")

#     if top_level != 1 or not top_section_id or not top_doc_id:
#         return fallback_context

#     try:
#         query_result = client.query(
#             collection="documents",
#             filter_expr=f"doc_id == '{top_doc_id}' && section_id == '{top_section_id}' && level in [1, 2]",
#             limit=50,
#             output_fields=[
#                 "doc_id",
#                 "section_id",
#                 "level",
#                 "title",
#                 "number",
#                 "text",
#             ],
#         )

#         rows = query_result.get("results", [])
#         if not rows:
#             return fallback_context

#         rows.sort(key=lambda x: (_natural_number_key(x.get("number")), x.get("level", 999)))

#         expanded_context = _build_context_from_rows(rows)
#         if expanded_context.strip():
#             return expanded_context

#         return fallback_context

#     except Exception:
#         return fallback_context


# def adaptive_search(question: str) -> Dict[str, Any]:
#     classification = classify_question(question)
#     question_type = classification["question_type"]
#     answer_mode = classification["answer_mode"]

#     payload = build_search_payload(question_type, answer_mode)
#     client = MilvusApiClient()

#     important_tokens = _extract_important_tokens(question)

#     if question_type == "norm_reference":
#         primary_query = question
#         primary_result = _run_search(client, primary_query, payload)
#         primary_results = primary_result.get("results", [])

#         if important_tokens and not _results_contain_important_token(primary_results, important_tokens):
#             rewritten_query = rewrite_query(question)
#             rewritten_result = _run_search(client, rewritten_query, payload)
#             rewritten_results = rewritten_result.get("results", [])

#             if _results_contain_important_token(rewritten_results, important_tokens):
#                 search_query = rewritten_query
#                 search_result = rewritten_result
#             else:
#                 search_query = primary_query
#                 search_result = primary_result
#         else:
#             search_query = primary_query
#             search_result = primary_result
#     else:
#         search_query = rewrite_query(question)
#         search_result = _run_search(client, search_query, payload)

#     raw_context = search_result.get("context", "")
#     results = search_result.get("results", [])

#     all_sources = extract_sources(results)
#     sources = all_sources[:3]

#     if question_type == "norm_reference":
#         context = _build_reference_context(results, all_sources)
#     else:
#         context = _maybe_expand_context(
#             client=client,
#             question=question,
#             question_type=question_type,
#             answer_mode=answer_mode,
#             results=results,
#             fallback_context=raw_context,
#         )

#     if context.strip():
#         answer = generate_answer(
#             question=question,
#             context=context,
#             question_type=question_type,
#             answer_mode=answer_mode,
#         )
#     else:
#         answer = "В документах нет информации по этому вопросу."

#     answer_with_sources = answer.strip()

#     if sources:
#         answer_with_sources += "\n\n" + format_sources(sources)
#     else:
#         answer_with_sources += "\n\nИсточники: не найдены"

#     return {
#         "question": question,
#         "search_query": search_query,
#         "question_type": question_type,
#         "answer_mode": answer_mode,
#         "classification": classification,
#         "search_payload": payload,
#         "results": results,
#         "context": context,
#         "answer": answer_with_sources,
#         "sources": sources,
#     }


# def print_result(result: Dict[str, Any], show_context: bool = True, context_limit: int = 0) -> None:
#     print("=" * 100)

#     print("QUESTION:", result["question"])
#     print("SEARCH QUERY:", result["search_query"])

#     print("CLASSIFICATION:")
#     print(json.dumps(result["classification"], ensure_ascii=False, indent=2))

#     print("SEARCH PAYLOAD:")
#     print(json.dumps(result["search_payload"], ensure_ascii=False, indent=2))

#     print("TOP HITS COUNT:", len(result["results"]))

#     print("\nANSWER:")
#     print(result["answer"])

#     if show_context:
#         print("\nCONTEXT:")
#         context = result["context"]

#         if context_limit > 0 and len(context) > context_limit:
#             print(context[:context_limit] + "\n...[TRUNCATED]...")
#         else:
#             print(context)

#     print()


# def chat_loop(show_context: bool = False, context_limit: int = 0) -> None:
#     print("💬 Adaptive RAG chat mode. Пустая строка — выход.")

#     while True:
#         try:
#             question = input("\n❓ Вопрос: ").strip()
#         except (EOFError, KeyboardInterrupt):
#             print("\n👋 Выход.")
#             break

#         if not question:
#             print("👋 Выход.")
#             break

#         try:
#             result = adaptive_search(question)
#             print_result(result, show_context=show_context, context_limit=context_limit)
#         except Exception as e:
#             print(f"Ошибка: {e}")


# def run_default_tests(show_context: bool = True, context_limit: int = 3000) -> None:
#     test_questions = [
#         "Какие требования к оперативной памяти?",
#         "Какие требования к транспортированию отходов?",
#         "Как у нас проходит закупка оборудования от начала до конца?",
#         "Где прописана процедура ПТП?",
#         "Какие задачи у сотрудников отдела геологии?",
#     ]

#     for q in test_questions:
#         result = adaptive_search(q)
#         print_result(result, show_context=show_context, context_limit=context_limit)


# def main():
#     parser = argparse.ArgumentParser(description="Adaptive RAG router for Milvus API")

#     parser.add_argument("question", nargs="?", help="Один вопрос для запуска")
#     parser.add_argument("--chat", action="store_true", help="Интерактивный режим")
#     parser.add_argument("--show-context", action="store_true", help="Показывать контекст")
#     parser.add_argument(
#         "--context-limit",
#         type=int,
#         default=0,
#         help="Обрезать контекст до N символов (0 = без обрезки)",
#     )

#     args = parser.parse_args()

#     if args.chat:
#         chat_loop(show_context=args.show_context, context_limit=args.context_limit)
#         return

#     if args.question:
#         result = adaptive_search(args.question)
#         print_result(result, show_context=args.show_context, context_limit=args.context_limit)
#         return

#     run_default_tests(show_context=True, context_limit=3000)


# if __name__ == "__main__":
#     main()


# router.py
from __future__ import annotations

import json
import argparse
import re
from typing import Any, Dict, List, Tuple

import requests

from config import LOCAL_LLM_MODEL
from classifier import classify_question
from milvus_client import MilvusApiClient
from answer_generator import generate_answer
from sources import extract_sources


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


def rewrite_query(question: str) -> str:
    prompt = f"""
Переформулируй вопрос для поиска по нормативным документам.

Правила:
1. Сохрани исходный смысл.
2. Сделай формулировку чуть более формальной.
3. НЕ добавляй новые слова, которых нет в вопросе.
4. НЕ добавляй документы, ГОСТы, стандарты.
5. НЕ меняй аббревиатуры.
6. Верни одну короткую строку.

Вопрос:
{question}

Переформулированный запрос:
""".strip()

    payload = {
        "model": LOCAL_LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0},
    }

    session = requests.Session()
    session.trust_env = False

    response = session.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    result = response.json()
    rewritten = result["response"].strip()

    if not rewritten:
        return question

    q_tokens = set(question.lower().split())
    r_tokens = set(rewritten.lower().split())

    if len(r_tokens - q_tokens) > 2:
        return question

    if len(rewritten) > len(question) * 1.5:
        return question

    forbidden = ["гост", "iso", "стандарт", "регламент"]
    if any(f in rewritten.lower() for f in forbidden):
        return question

    return rewritten


def build_search_payload(question_type: str, answer_mode: str) -> Dict[str, Any]:
    if question_type == "fact":
        if answer_mode == "list":
            return {
                "mode": "hybrid",
                "level": [1, 2],
                "limit": 8,
                "use_summary": True,
            }
        return {
            "mode": "dense",
            "level": [1, 2],
            "limit": 5,
            "use_summary": False,
        }

    if question_type == "definition":
        return {
            "mode": "hybrid",
            "level": [1, 2],
            "limit": 6,
            "use_summary": True,
        }

    if question_type == "procedure":
        return {
            "mode": "hybrid",
            "level": [0, 1, 2],
            "limit": 10,
            "use_summary": True,
        }

    if question_type == "norm_reference":
        return {
            "mode": "hybrid",
            "level": [1, 2],
            "limit": 5,
            "use_summary": True,
        }

    if question_type == "broad_overview":
        return {
            "mode": "hybrid",
            "level": [0, 1],
            "limit": 6,
            "use_summary": True,
        }

    return {
        "mode": "hybrid",
        "level": [0, 1, 2],
        "limit": 5,
        "use_summary": True,
    }


def format_sources(sources: list[str]) -> str:
    if not sources:
        return "Источники: не найдены"

    lines = ["Источники:"]
    for src in sources:
        lines.append(f"• {src}")
    return "\n".join(lines)


def _natural_number_key(value: str) -> List[Any]:
    if value is None:
        return [999999]
    parts = re.split(r"[^\d]+", str(value))
    nums = [int(p) for p in parts if p.isdigit()]
    return nums if nums else [999999]


def _build_context_from_rows(rows: List[Dict[str, Any]]) -> str:
    blocks = []

    for row in rows:
        number = row.get("number")
        title = row.get("title")
        text = row.get("text", "")

        header = ""
        if number and title:
            header = f"## {number} {title}"
        elif title:
            header = f"## {title}"
        elif number:
            header = f"## {number}"

        if header:
            blocks.append(f"{header}\n{text}".strip())
        else:
            blocks.append(str(text).strip())

    return "\n\n".join(b for b in blocks if b.strip())


def _build_sources_from_rows(rows: List[Dict[str, Any]], max_sources: int = 3) -> List[str]:
    """
    Строим источники не из raw retrieval hits, а из реально использованных rows.
    """
    seen = set()
    out = []

    for row in rows:
        title = str(row.get("title", "")).strip()
        number = str(row.get("number", "")).strip()

        if not title and not number:
            continue

        if number and title:
            src = f"{title} (раздел {number})"
        elif title:
            src = title
        else:
            src = f"раздел {number}"

        if src not in seen:
            seen.add(src)
            out.append(src)

        if len(out) >= max_sources:
            break

    return out


def _extract_important_tokens(question: str) -> list[str]:
    tokens = set()

    doc_codes = re.findall(r"\b[А-ЯA-Z]{2,}-\d{2}(?:-\w+)?\b", question, flags=re.UNICODE)
    for t in doc_codes:
        tokens.add(t.strip())

    abbrevs = re.findall(r"\b[А-ЯA-Z]{2,6}\b", question, flags=re.UNICODE)
    for t in abbrevs:
        tokens.add(t.strip())

    return sorted(tokens)


def _results_contain_important_token(results: list[dict], tokens: list[str]) -> bool:
    if not tokens or not results:
        return False

    corpus = []
    for r in results:
        corpus.append(str(r.get("title", "")))
        corpus.append(str(r.get("text", "")))

    joined = "\n".join(corpus).lower()

    for token in tokens:
        if token.lower() in joined:
            return True

    return False


def _run_search(client: MilvusApiClient, query_text: str, payload: dict) -> dict:
    return client.search(
        text=query_text,
        mode=payload["mode"],
        level=payload["level"],
        limit=payload["limit"],
        use_summary=payload["use_summary"],
    )


def _build_reference_context(results: List[Dict[str, Any]], sources: List[str]) -> str:
    blocks = []

    for i, row in enumerate(results[:5]):
        title = row.get("title", "")
        number = row.get("number", "")
        text = str(row.get("text", "")).strip()
        source = sources[i] if i < len(sources) else "Неизвестный источник"

        short_text = text[:500] + "..." if len(text) > 500 else text

        block = (
            f"Источник: {source}\n"
            f"Раздел: {title}\n"
            f"Номер: {number}\n"
            f"Фрагмент: {short_text}"
        )
        blocks.append(block)

    return "\n\n".join(blocks)


def _procedure_doc_score(question: str, row: Dict[str, Any]) -> float:
    q = question.lower()
    title = str(row.get("title", "")).lower()
    text = str(row.get("text", "")).lower()
    score = float(row.get("score", 0.0) or 0.0)

    bonus = 0.0

    positive = [
        "порядок",
        "внешн",
        "постав",
        "закуп",
        "приобрет",
        "получение",
        "согласование",
        "действий",
    ]

    negative = [
        "верификац",
        "контроль",
        "приемк",
        "архив",
        "регистрац",
        "перечень программного обеспечения",
    ]

    for p in positive:
        if p in title:
            bonus += 2.5
        elif p in text:
            bonus += 0.3

    for p in negative:
        if p in title:
            bonus -= 2.0
        elif p in text:
            bonus -= 0.2

    if "от начала до конца" in q:
        if "верификац" in title:
            bonus -= 3.0

    return score + bonus


def _select_best_procedure_doc(question: str, results: List[Dict[str, Any]]) -> str | None:
    if not results:
        return None

    best_doc_id = None
    best_score = float("-inf")

    for row in results:
        doc_id = row.get("doc_id")
        if not doc_id:
            continue

        row_score = _procedure_doc_score(question, row)
        if row_score > best_score:
            best_score = row_score
            best_doc_id = doc_id

    return best_doc_id


def _filter_procedure_rows(rows: List[Dict[str, Any]], question: str) -> List[Dict[str, Any]]:
    """
    Оставляем только procedural-части документа.
    Жёстче режем мусор: требования к ПО, бумаге, компьютерам и т.д.
    """
    selected = []

    positive_title = [
        "порядок",
        "внешн",
        "постав",
        "закуп",
        "приобрет",
        "получение",
        "согласование",
        "действий",
        "верификац",
        "оценка, выбор",
    ]

    positive_text = [
        "порядок действий",
        "осуществляется",
        "организует",
        "проводится",
        "основанием для проведения",
        "деятельность по внешней поставке",
        "подготовке и проведению процедур по поставке",
        "заключению договоров",
        "анализу их исполнения",
        "получение товара",
        "входной контроль",
        "подтверждением приемки",
    ]

    negative_hard = [
        "список рассылки",
        "перечень программного обеспечения",
        "термины",
        "сокращения",
        "приложение",
        "требования к компьютерам",
        "требования к бумаге",
        "требования к принтерам",
        "требования к поставляемому программному обеспечению",
        "требования к оргтехнике",
        "по должно быть",
        "объем оперативной памяти",
        "жесткий диск",
        "диагонали монитора",
    ]

    for row in rows:
        title = str(row.get("title", "")).lower()
        text = str(row.get("text", "")).lower()
        level = row.get("level")

        if any(bad in title for bad in negative_hard):
            continue
        if any(bad in text for bad in negative_hard):
            continue

        if level == 1:
            if any(p in title for p in positive_title):
                selected.append(row)
                continue

        if level == 2:
            if any(p in title for p in positive_title) or any(p in text for p in positive_text):
                selected.append(row)
                continue

    if not selected:
        return rows

    return selected


def _build_procedure_context(
    client: MilvusApiClient,
    question: str,
    results: List[Dict[str, Any]],
    fallback_context: str,
) -> Tuple[str, List[str]]:
    """
    Для procedure берём лучший ДОКУМЕНТ, а не один section.
    Потом вытягиваем все level 1/2 этого документа и фильтруем по procedural-частям.
    """
    best_doc_id = _select_best_procedure_doc(question, results)
    if not best_doc_id:
        return fallback_context, []

    try:
        query_result = client.query(
            collection="documents",
            filter_expr=f"doc_id == '{best_doc_id}' && level in [1, 2]",
            limit=200,
            output_fields=[
                "doc_id",
                "section_id",
                "level",
                "title",
                "number",
                "text",
            ],
        )

        rows = query_result.get("results", [])
        if not rows:
            return fallback_context, []

        rows = _filter_procedure_rows(rows, question)
        rows.sort(key=lambda x: (_natural_number_key(x.get("number")), x.get("level", 999)))

        context = _build_context_from_rows(rows)
        sources = _build_sources_from_rows(rows, max_sources=3)

        if context.strip():
            return context, sources

        return fallback_context, []

    except Exception:
        return fallback_context, []


def _maybe_expand_context(
    client: MilvusApiClient,
    question: str,
    question_type: str,
    answer_mode: str,
    results: List[Dict[str, Any]],
    fallback_context: str,
) -> Tuple[str, List[str]]:
    if not results:
        return fallback_context, []

    if question_type == "procedure" or answer_mode == "steps":
        return _build_procedure_context(client, question, results, fallback_context)

    should_expand = (
        question_type in {"broad_overview"}
        or answer_mode in {"list"}
        or (question_type == "fact" and answer_mode == "list")
    )

    if not should_expand:
        return fallback_context, []

    top = results[0]
    top_level = top.get("level")
    top_section_id = top.get("section_id")
    top_doc_id = top.get("doc_id")

    if top_level != 1 or not top_section_id or not top_doc_id:
        return fallback_context, []

    try:
        query_result = client.query(
            collection="documents",
            filter_expr=f"doc_id == '{top_doc_id}' && section_id == '{top_section_id}' && level in [1, 2]",
            limit=50,
            output_fields=[
                "doc_id",
                "section_id",
                "level",
                "title",
                "number",
                "text",
            ],
        )

        rows = query_result.get("results", [])
        if not rows:
            return fallback_context, []

        rows.sort(key=lambda x: (_natural_number_key(x.get("number")), x.get("level", 999)))

        expanded_context = _build_context_from_rows(rows)
        expanded_sources = _build_sources_from_rows(rows, max_sources=3)

        if expanded_context.strip():
            return expanded_context, expanded_sources

        return fallback_context, []

    except Exception:
        return fallback_context, []


def adaptive_search(question: str) -> Dict[str, Any]:
    classification = classify_question(question)
    question_type = classification["question_type"]
    answer_mode = classification["answer_mode"]

    payload = build_search_payload(question_type, answer_mode)
    client = MilvusApiClient()

    important_tokens = _extract_important_tokens(question)

    if question_type == "norm_reference":
        primary_query = question
        primary_result = _run_search(client, primary_query, payload)
        primary_results = primary_result.get("results", [])

        if important_tokens and not _results_contain_important_token(primary_results, important_tokens):
            rewritten_query = rewrite_query(question)
            rewritten_result = _run_search(client, rewritten_query, payload)
            rewritten_results = rewritten_result.get("results", [])

            if _results_contain_important_token(rewritten_results, important_tokens):
                search_query = rewritten_query
                search_result = rewritten_result
            else:
                search_query = primary_query
                search_result = primary_result
        else:
            search_query = primary_query
            search_result = primary_result
    else:
        search_query = rewrite_query(question)
        search_result = _run_search(client, search_query, payload)

    raw_context = search_result.get("context", "")
    results = search_result.get("results", [])

    all_sources = extract_sources(results)
    sources = all_sources[:3]

    if question_type == "norm_reference":
        context = _build_reference_context(results, all_sources)
    elif question_type == "procedure" or answer_mode == "steps":
        context, expanded_sources = _maybe_expand_context(
            client=client,
            question=question,
            question_type=question_type,
            answer_mode=answer_mode,
            results=results,
            fallback_context=raw_context,
        )
        if expanded_sources:
            sources = expanded_sources
    else:
        context, expanded_sources = _maybe_expand_context(
            client=client,
            question=question,
            question_type=question_type,
            answer_mode=answer_mode,
            results=results,
            fallback_context=raw_context,
        )
        if expanded_sources:
            sources = expanded_sources

    if context.strip():
        answer = generate_answer(
            question=question,
            context=context,
            question_type=question_type,
            answer_mode=answer_mode,
        )
    else:
        answer = "В документах нет информации по этому вопросу."

    answer_with_sources = answer.strip()

    if sources:
        answer_with_sources += "\n\n" + format_sources(sources)
    else:
        answer_with_sources += "\n\nИсточники: не найдены"

    return {
        "question": question,
        "search_query": search_query,
        "question_type": question_type,
        "answer_mode": answer_mode,
        "classification": classification,
        "search_payload": payload,
        "results": results,
        "context": context,
        "answer": answer_with_sources,
        "sources": sources,
    }


def print_result(result: Dict[str, Any], show_context: bool = True, context_limit: int = 0) -> None:
    print("=" * 100)

    print("QUESTION:", result["question"])
    print("SEARCH QUERY:", result["search_query"])

    print("CLASSIFICATION:")
    print(json.dumps(result["classification"], ensure_ascii=False, indent=2))

    print("SEARCH PAYLOAD:")
    print(json.dumps(result["search_payload"], ensure_ascii=False, indent=2))

    print("TOP HITS COUNT:", len(result["results"]))

    print("\nANSWER:")
    print(result["answer"])

    if show_context:
        print("\nCONTEXT:")
        context = result["context"]

        if context_limit > 0 and len(context) > context_limit:
            print(context[:context_limit] + "\n...[TRUNCATED]...")
        else:
            print(context)

    print()


def chat_loop(show_context: bool = False, context_limit: int = 0) -> None:
    print("💬 Adaptive RAG chat mode. Пустая строка — выход.")

    while True:
        try:
            question = input("\n❓ Вопрос: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Выход.")
            break

        if not question:
            print("👋 Выход.")
            break

        try:
            result = adaptive_search(question)
            print_result(result, show_context=show_context, context_limit=context_limit)
        except Exception as e:
            print(f"Ошибка: {e}")


def run_default_tests(show_context: bool = True, context_limit: int = 3000) -> None:
    test_questions = [
        "Какие требования к оперативной памяти?",
        "Какие требования к транспортированию отходов?",
        "Как у нас проходит закупка оборудования от начала до конца?",
        "Где прописана процедура ПТП?",
        "Какие задачи у сотрудников отдела геологии?",
    ]

    for q in test_questions:
        result = adaptive_search(q)
        print_result(result, show_context=show_context, context_limit=context_limit)


def main():
    parser = argparse.ArgumentParser(description="Adaptive RAG router for Milvus API")

    parser.add_argument("question", nargs="?", help="Один вопрос для запуска")
    parser.add_argument("--chat", action="store_true", help="Интерактивный режим")
    parser.add_argument("--show-context", action="store_true", help="Показывать контекст")
    parser.add_argument(
        "--context-limit",
        type=int,
        default=0,
        help="Обрезать контекст до N символов (0 = без обрезки)",
    )

    args = parser.parse_args()

    if args.chat:
        chat_loop(show_context=args.show_context, context_limit=args.context_limit)
        return

    if args.question:
        result = adaptive_search(args.question)
        print_result(result, show_context=args.show_context, context_limit=args.context_limit)
        return

    run_default_tests(show_context=True, context_limit=3000)


if __name__ == "__main__":
    main()