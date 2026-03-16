# # answer_generator.py
# from __future__ import annotations

# import requests
# from config import LOCAL_LLM_MODEL


# OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


# def generate_answer(question: str, context: str) -> str:
#     """
#     Генерирует финальный ответ LLM на основе retrieved context.
#     """

#     prompt = f"""
# Ты ассистент для поиска информации в корпоративных нормативных документах.

# Твоя задача — ответить на вопрос пользователя, используя ТОЛЬКО информацию из контекста.

# Правила:
# 1. Не придумывай информацию.
# 2. Если в контексте нет ответа — скажи "В документах нет информации по этому вопросу".
# 3. Ответ должен быть кратким и точным.

# КОНТЕКСТ:
# {context}

# ВОПРОС:
# {question}

# ОТВЕТ:
# """

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

#     response = session.post(
#         OLLAMA_URL,
#         json=payload,
#         timeout=120,
#     )

#     if response.status_code != 200:
#         print("OLLAMA ERROR:", response.text)
#         response.raise_for_status()

#     result = response.json()

#     return result["response"].strip()

# # answer_generator.py
# from __future__ import annotations

# import requests
# from config import LOCAL_LLM_MODEL


# OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


# def _post_ollama(prompt: str) -> str:
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

#     response = session.post(
#         OLLAMA_URL,
#         json=payload,
#         timeout=120,
#     )

#     if response.status_code != 200:
#         print("OLLAMA ERROR:", response.text)
#         response.raise_for_status()

#     result = response.json()
#     return result["response"].strip()


# def generate_answer(question: str, context: str, question_type: str) -> str:
#     """
#     Генерирует ответ с учетом типа вопроса.
#     """

#     if question_type == "fact":
#         prompt = f"""
# Ты ассистент по корпоративным нормативным документам.

# Ответь на вопрос ТОЛЬКО по контексту.
# Если ответа нет — напиши: "В документах нет информации по этому вопросу".

# Нужен короткий точный ответ без лишних пояснений.

# КОНТЕКСТ:
# {context}

# ВОПРОС:
# {question}

# ОТВЕТ:
# """.strip()
#         return _post_ollama(prompt)

#     if question_type == "definition":
#         prompt = f"""
# Ты ассистент по корпоративным нормативным документам.

# Найди определение термина ТОЛЬКО в контексте.
# Если точного определения нет — напиши: "В документах нет информации по этому вопросу".

# Дай ответ в формате:
# Термин — определение.

# КОНТЕКСТ:
# {context}

# ВОПРОС:
# {question}

# ОТВЕТ:
# """.strip()
#         return _post_ollama(prompt)

#     if question_type == "procedure":
#         prompt = f"""
# Ты ассистент по корпоративным нормативным документам.

# Ответь на вопрос ТОЛЬКО по контексту.
# Если информации недостаточно — напиши: "В документах нет полной информации по этому вопросу".

# Если в контексте описан процесс, представь ответ в виде шагов.

# КОНТЕКСТ:
# {context}

# ВОПРОС:
# {question}

# ОТВЕТ:
# """.strip()
#         return _post_ollama(prompt)

#     if question_type == "norm_reference":
#         prompt = f"""
# Ты ассистент по корпоративным нормативным документам.

# Пользователь спрашивает, В КАКОМ ДОКУМЕНТЕ или РАЗДЕЛЕ прописана процедура / правило.

# Твоя задача:
# 1. Найти в контексте название документа, раздела, инструкции, положения или пункта.
# 2. Ответить, где именно это прописано.
# 3. Если есть номер документа или раздела — обязательно укажи его.
# 4. Если ничего релевантного нет — напиши: "В документах нет информации по этому вопросу".

# Не пересказывай весь контекст. Скажи кратко:
# - документ
# - раздел / пункт
# - что именно там описано

# КОНТЕКСТ:
# {context}

# ВОПРОС:
# {question}

# ОТВЕТ:
# """.strip()
#         return _post_ollama(prompt)

#     # broad_overview
#     prompt = f"""
# Ты ассистент по корпоративным нормативным документам.

# Ответь на вопрос ТОЛЬКО по контексту.
# Если информации недостаточно — напиши: "В документах нет информации по этому вопросу".

# Для обзорного вопроса дай краткое, структурированное summary.

# КОНТЕКСТ:
# {context}

# ВОПРОС:
# {question}

# ОТВЕТ:
# """.strip()
#     return _post_ollama(prompt)

# # answer_generator.py
# from __future__ import annotations

# import requests
# from config import LOCAL_LLM_MODEL


# OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


# def _post_ollama(prompt: str) -> str:
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

#     response = session.post(
#         OLLAMA_URL,
#         json=payload,
#         timeout=120,
#     )

#     if response.status_code != 200:
#         print("OLLAMA ERROR:", response.text)
#         response.raise_for_status()

#     result = response.json()
#     return result["response"].strip()


# def generate_answer(question: str, context: str, question_type: str) -> str:
#     """
#     Генерирует ответ с учетом типа вопроса.
#     """

#     base_rules = """
# Ты ассистент по корпоративным нормативным документам.

# Строгие правила:
# 1. Отвечай ТОЛЬКО на основе предоставленного контекста.
# 2. НИЧЕГО не придумывай и не добавляй от себя.
# 3. Если в контексте нет ответа, напиши:
#    "В документах нет информации по этому вопросу."
# 4. Если в контексте есть список требований, правил, шагов или подпунктов,
#    НЕ пересказывай его кратко — выведи его в виде списка.
# 5. Сохраняй структуру текста:
#    - пункты
#    - подпункты
#    - нумерацию
# 6. Не используй внешние знания.
# """.strip()

#     if question_type == "fact":
#         prompt = f"""
# {base_rules}

# Тип вопроса: точный факт / требование / параметр.

# Формат ответа:
# - если ответ короткий и одиночный — дай короткий точный ответ;
# - если в контексте ответ задан списком требований или условий —
#   выведи соответствующие пункты списком;
# - не делай лишних пояснений.

# КОНТЕКСТ:
# {context}

# ВОПРОС:
# {question}

# ОТВЕТ:
# """.strip()
#         return _post_ollama(prompt)

#     if question_type == "definition":
#         prompt = f"""
# {base_rules}

# Тип вопроса: определение термина.

# Формат ответа:
# - "Термин — определение"
# - если есть несколько уточняющих элементов в определении, можно дать их в одной-двух строках;
# - если точного определения нет, напиши:
#   "В документах нет информации по этому вопросу."

# КОНТЕКСТ:
# {context}

# ВОПРОС:
# {question}

# ОТВЕТ:
# """.strip()
#         return _post_ollama(prompt)

#     if question_type == "procedure":
#         prompt = f"""
# {base_rules}

# Тип вопроса: порядок действий / процедура.

# Формат ответа:
# - представь ответ в виде шагов или пунктов;
# - если шаги явно перечислены в контексте, сохрани их порядок;
# - если информации недостаточно для полного процесса, напиши:
#   "В документах нет полной информации по этому вопросу."

# КОНТЕКСТ:
# {context}

# ВОПРОС:
# {question}

# ОТВЕТ:
# """.strip()
#         return _post_ollama(prompt)

#     if question_type == "norm_reference":
#         prompt = f"""
# {base_rules}

# Тип вопроса: ссылка на нормативный документ / раздел / пункт.

# Твоя задача:
# 1. Не пересказывать весь контекст.
# 2. Кратко указать:
#    - в каком документе это прописано;
#    - в каком разделе / пункте / подпункте это описано;
#    - что именно там регулируется.
# 3. Если в контексте нет явного указания, напиши:
#    "В документах нет информации по этому вопросу."

# Формат ответа:
# Документ: ...
# Раздел / пункт: ...
# Содержание: ...

# КОНТЕКСТ:
# {context}

# ВОПРОС:
# {question}

# ОТВЕТ:
# """.strip()
#         return _post_ollama(prompt)

#     # broad_overview
#     prompt = f"""
# {base_rules}

# Тип вопроса: общий обзор.

# Формат ответа:
# - дай краткий, но структурированный обзор;
# - если в контексте есть перечень задач / функций / обязанностей,
#   выведи их списком;
# - не сокращай смысл до одной общей фразы, если есть явные пункты.

# КОНТЕКСТ:
# {context}

# ВОПРОС:
# {question}

# ОТВЕТ:
# """.strip()
#     return _post_ollama(prompt)


# # answer_generator.py
# from __future__ import annotations

# import requests
# from config import LOCAL_LLM_MODEL


# OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


# def _post_ollama(prompt: str) -> str:
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

#     response = session.post(
#         OLLAMA_URL,
#         json=payload,
#         timeout=120,
#     )

#     if response.status_code != 200:
#         print("OLLAMA ERROR:", response.text)
#         response.raise_for_status()

#     result = response.json()
#     return result["response"].strip()


# def generate_answer(question: str, context: str, question_type: str, answer_mode: str) -> str:
#     base_rules = """
# Ты ассистент по корпоративным нормативным документам.

# Строгие правила:
# 1. Отвечай ТОЛЬКО на основе предоставленного контекста.
# 2. НИЧЕГО не придумывай и не добавляй от себя.
# 3. Если в контексте нет ответа, напиши:
#    "В документах нет информации по этому вопросу."
# 4. Если в контексте есть список требований, правил, шагов или подпунктов,
#    НЕ пересказывай его кратко — выведи его в виде списка.
# 5. Сохраняй структуру текста:
#    - пункты
#    - подпункты
#    - нумерацию
# 6. Не используй внешние знания.
# """.strip()

#     mode_instruction = {
#         "single": """
# Ожидается один точный ответ.
# Если в контексте ответ одиночный — дай короткий точный ответ.
# Если в контексте вместо одного факта найден список, верни только релевантный пункт или пункты.
# """,
#         "list": """
# Ожидается список.
# Если в контексте есть перечень требований / обязанностей / условий / правил,
# верни его списком.
# Не сворачивай несколько пунктов в один абзац.
# """,
#         "steps": """
# Ожидается пошаговый ответ.
# Если в контексте есть процесс, выведи шаги по порядку.
# """,
#         "reference": """
# Ожидается ссылка на документ / раздел / пункт.
# Ответь кратко:
# Документ: ...
# Раздел / пункт: ...
# Содержание: ...
# """,
#         "summary": """
# Ожидается краткий обзор.
# Если в контексте есть явные пункты, можно вывести их списком.
# """,
#     }.get(answer_mode, "Дай точный структурированный ответ.")

#     type_instruction = {
#         "fact": "Тип вопроса: факт / параметр / требование.",
#         "definition": "Тип вопроса: определение термина.",
#         "procedure": "Тип вопроса: порядок действий / процедура.",
#         "norm_reference": "Тип вопроса: ссылка на нормативный документ / раздел / пункт.",
#         "broad_overview": "Тип вопроса: обзорный вопрос.",
#     }.get(question_type, "Тип вопроса: общий.")

#     prompt = f"""
# {base_rules}

# {type_instruction}

# Формат ответа:
# {mode_instruction}

# КОНТЕКСТ:
# {context}

# ВОПРОС:
# {question}

# ОТВЕТ:
# """.strip()

#     return _post_ollama(prompt)

# # answer_generator.py
# from __future__ import annotations

# import requests
# from config import LOCAL_LLM_MODEL


# OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


# def _post_ollama(prompt: str) -> str:
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

#     response = session.post(
#         OLLAMA_URL,
#         json=payload,
#         timeout=120,
#     )

#     if response.status_code != 200:
#         print("OLLAMA ERROR:", response.text)
#         response.raise_for_status()

#     result = response.json()
#     return result["response"].strip()


# def generate_answer(question: str, context: str, question_type: str, answer_mode: str) -> str:
#     base_rules = """
# Ты ассистент по корпоративным нормативным документам.

# Строгие правила:
# 1. Отвечай ТОЛЬКО на основе предоставленного контекста.
# 2. НИЧЕГО не придумывай и не добавляй от себя.
# 3. Если в контексте нет ответа, напиши:
#    "В документах нет информации по этому вопросу."
# 4. Если в контексте есть список требований, правил, шагов или подпунктов,
#    НЕ пересказывай его кратко — выведи его в виде списка.
# 5. Сохраняй структуру текста:
#    - пункты
#    - подпункты
#    - нумерацию
# 6. Не используй внешние знания.
# """.strip()

#     if question_type == "norm_reference":
#         prompt = f"""
# {base_rules}

# Тип вопроса: ссылка на нормативный документ / раздел / пункт.

# Твоя задача:
# 1. Выбери ОДИН самый релевантный источник из контекста.
# 2. Ответь максимально кратко.
# 3. Не пересказывай весь текст раздела.
# 4. Не перечисляй много вариантов, если один источник явно лучший.
# 5. Если релевантного источника нет, напиши:
#    "В документах нет информации по этому вопросу."

# Формат ответа строго такой:

# Документ: ...
# Раздел / пункт: ...
# Кратко: ...

# КОНТЕКСТ:
# {context}

# ВОПРОС:
# {question}

# ОТВЕТ:
# """.strip()
#         return _post_ollama(prompt)

#     mode_instruction = {
#         "single": """
# Ожидается один точный ответ.
# Если в контексте ответ одиночный — дай короткий точный ответ.
# Если в контексте вместо одного факта найден список, верни только релевантный пункт или пункты.
# """,
#         "list": """
# Ожидается список.
# Если в контексте есть перечень требований / обязанностей / условий / правил,
# верни его списком.
# Не сворачивай несколько пунктов в один абзац.
# """,
#         "steps": """
# Ожидается пошаговый ответ.
# Если в контексте есть процесс, выведи шаги по порядку.
# """,
#         "summary": """
# Ожидается краткий обзор.
# Если в контексте есть явные пункты, можно вывести их списком.
# """,
#     }.get(answer_mode, "Дай точный структурированный ответ.")

#     type_instruction = {
#         "fact": "Тип вопроса: факт / параметр / требование.",
#         "definition": "Тип вопроса: определение термина.",
#         "procedure": "Тип вопроса: порядок действий / процедура.",
#         "broad_overview": "Тип вопроса: обзорный вопрос.",
#     }.get(question_type, "Тип вопроса: общий.")

#     prompt = f"""
# {base_rules}

# {type_instruction}

# Формат ответа:
# {mode_instruction}

# КОНТЕКСТ:
# {context}

# ВОПРОС:
# {question}

# ОТВЕТ:
# """.strip()

#     return _post_ollama(prompt)


# answer_generator.py
from __future__ import annotations

import re
import requests
from config import LOCAL_LLM_MODEL


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


def _post_ollama(prompt: str) -> str:
    payload = {
        "model": LOCAL_LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    session = requests.Session()
    session.trust_env = False

    response = session.post(
        OLLAMA_URL,
        json=payload,
        timeout=120,
    )

    if response.status_code != 200:
        print("OLLAMA ERROR:", response.text)
        response.raise_for_status()

    result = response.json()
    return result["response"].strip()


def _clean_line(line: str) -> str:
    line = re.sub(r"\s+", " ", line).strip()
    line = line.strip("•-–— ")
    return line


def _extract_procedure_steps_from_context(context: str) -> list[str]:
    """
    Детерминированно вытаскиваем procedural-строки из контекста.
    Ищем:
    - нумерованные пункты
    - строки с процедурными словами
    """
    lines = [l.strip() for l in context.splitlines() if l.strip()]
    steps: list[str] = []

    procedural_markers = [
        "согласование",
        "приобрет",
        "закуп",
        "получение",
        "поставка",
        "верификац",
        "контроль",
        "приемк",
        "подтверждение",
        "регистрац",
        "направляется",
        "организует",
        "осуществляется",
        "проводится",
        "проверка",
        "подписание",
    ]

    for line in lines:
        low = line.lower()

        if low.startswith("##"):
            continue

        # 1) явная нумерация: 1. / 1) / 7.12 / 7.1
        if re.match(r"^\d+(\.\d+)*[\)\.]?\s+", line):
            cleaned = _clean_line(line)
            if len(cleaned) >= 10:
                steps.append(cleaned)
            continue

        # 2) строки с процедурными маркерами
        if any(marker in low for marker in procedural_markers):
            cleaned = _clean_line(line)
            if len(cleaned) >= 20:
                steps.append(cleaned)

    # дедупликация
    unique_steps = []
    seen = set()

    for step in steps:
        key = step.lower()
        if key not in seen:
            seen.add(key)
            unique_steps.append(step)

    return unique_steps


def _build_procedure_answer(context: str) -> str:
    steps = _extract_procedure_steps_from_context(context)

    if not steps:
        return "В документах нет полной информации по этому вопросу."

    # отсечь явный мусор / слишком длинные простыни
    filtered = []
    for s in steps:
        if len(s) > 600:
            s = s[:600].rstrip() + "..."
        filtered.append(s)

    # ограничим разумным числом шагов
    filtered = filtered[:10]

    lines = ["В контексте описана только часть процесса.", "Найдены следующие шаги:"]
    for i, step in enumerate(filtered, start=1):
        lines.append(f"{i}. {step}")

    return "\n".join(lines)


def generate_answer(question: str, context: str, question_type: str, answer_mode: str) -> str:
    base_rules = """
Ты ассистент по корпоративным нормативным документам.

Строгие правила:
1. Отвечай ТОЛЬКО на основе предоставленного контекста.
2. НИЧЕГО не придумывай и не добавляй от себя.
3. Если в контексте нет ответа, напиши:
   "В документах нет информации по этому вопросу."
4. Если в контексте есть список требований, правил, шагов или подпунктов,
   НЕ пересказывай его кратко — выведи его в виде списка.
5. Сохраняй структуру текста:
   - пункты
   - подпункты
   - нумерацию
6. Не используй внешние знания.
""".strip()

    # --- PROCEDURE: ДЕЛАЕМ БЕЗ СВОБОДНОЙ ГЕНЕРАЦИИ ---
    if question_type == "procedure" or answer_mode == "steps":
        return _build_procedure_answer(context)

    # --- NORM REFERENCE ---
    if question_type == "norm_reference":
        prompt = f"""
{base_rules}

Тип вопроса: ссылка на нормативный документ / раздел / пункт.

Твоя задача:
1. Выбери ОДИН самый релевантный источник из контекста.
2. Ответь максимально кратко.
3. Не пересказывай весь текст раздела.
4. Не перечисляй много вариантов, если один источник явно лучший.
5. Если релевантного источника нет, напиши:
   "В документах нет информации по этому вопросу."

Формат ответа строго такой:

Документ: ...
Раздел / пункт: ...
Кратко: одно короткое предложение по сути, что именно там описано.

КОНТЕКСТ:
{context}

ВОПРОС:
{question}

ОТВЕТ:
""".strip()
        return _post_ollama(prompt)

    # --- DEFINITION ---
    if question_type == "definition":
        prompt = f"""
{base_rules}

Тип вопроса: определение термина.

Формат ответа:
- "Термин — определение"
- если есть несколько уточняющих элементов в определении, можно дать их в одной-двух строках;
- если точного определения нет, напиши:
  "В документах нет информации по этому вопросу."

КОНТЕКСТ:
{context}

ВОПРОС:
{question}

ОТВЕТ:
""".strip()
        return _post_ollama(prompt)

    # --- FACT / SINGLE ---
    if answer_mode == "single":
        prompt = f"""
{base_rules}

Тип вопроса: факт / параметр / требование.

Формат ответа:
- если ответ одиночный — дай короткий точный ответ;
- если в контексте есть несколько близких пунктов, выбери только релевантный;
- не превращай короткий ответ в длинный список без необходимости.

КОНТЕКСТ:
{context}

ВОПРОС:
{question}

ОТВЕТ:
""".strip()
        return _post_ollama(prompt)

    # --- LIST ---
    if answer_mode == "list":
        prompt = f"""
{base_rules}

Тип вопроса: список требований / условий / обязанностей / правил.

Формат ответа:
- выведи список;
- не сворачивай несколько пунктов в один абзац;
- если в контексте есть нумерация, сохрани её по смыслу;
- не добавляй пункты, которых нет в контексте.

КОНТЕКСТ:
{context}

ВОПРОС:
{question}

ОТВЕТ:
""".strip()
        return _post_ollama(prompt)

    # --- SUMMARY / FALLBACK ---
    prompt = f"""
{base_rules}

Тип вопроса: обзорный вопрос.

Формат ответа:
- дай краткий, но структурированный обзор;
- если в контексте есть явные пункты, можно вывести их списком;
- не добавляй сведений, которых нет в контексте.

КОНТЕКСТ:
{context}

ВОПРОС:
{question}

ОТВЕТ:
""".strip()

    return _post_ollama(prompt)