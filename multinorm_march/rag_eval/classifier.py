# # classifier.py
# from __future__ import annotations

# import json
# import re
# from typing import Any, Dict

# import requests

# from config import LOCAL_LLM_MODEL


# OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


# def _extract_json(text: str) -> Dict[str, Any]:
#     """
#     Пытаемся извлечь JSON из ответа модели.
#     """
#     text = text.strip()

#     try:
#         return json.loads(text)
#     except Exception:
#         pass

#     match = re.search(r"\{.*\}", text, flags=re.DOTALL)
#     if match:
#         try:
#             return json.loads(match.group(0))
#         except Exception:
#             pass

#     raise ValueError(f"Не удалось извлечь JSON из ответа модели:\n{text}")


# def _post_to_ollama(payload: Dict[str, Any]) -> requests.Response:
#     """
#     Делаем запрос к локальному Ollama БЕЗ использования системных прокси.
#     """
#     session = requests.Session()
#     session.trust_env = False  # критично: не брать HTTP_PROXY/HTTPS_PROXY из окружения

#     return session.post(
#         OLLAMA_URL,
#         json=payload,
#         timeout=120,
#     )


# def classify_question(
#     question: str,
#     model_name: str = LOCAL_LLM_MODEL,
#     temperature: float = 0.0,
# ) -> Dict[str, Any]:
#     """
#     Классифицирует вопрос в один из классов:
#     - fact
#     - definition
#     - procedure
#     - norm_reference
#     - broad_overview
#     """

#     prompt = f"""
# Ты классификатор запросов для корпоративной системы поиска по нормативным документам.

# Тебе нужно отнести вопрос РОВНО к одному из классов:

# 1. fact
#    Это запрос на точный факт, характеристику, требование, ограничение, число, параметр.
#    Примеры:
#    - "Какие требования к оперативной памяти?"
#    - "Сколько времени можно хранить отходы?"
#    - "Кто отвечает за учет отходов?"

# 2. definition
#    Это запрос на определение термина или понятия.
#    Примеры:
#    - "Что такое федеральный оператор?"
#    - "Что означает интегрированная система менеджмента?"

# 3. procedure
#    Это запрос на порядок действий, шаги, как оформить / как сделать / что делать дальше.
#    Примеры:
#    - "Как проходит закупка оборудования?"
#    - "Что делать после обнаружения нового тендера?"
#    - "Как оформить командировку?"

# 4. norm_reference
#    Это запрос на ссылку на нормативный документ, регламент, ГОСТ, пункт, основание.
#    Примеры:
#    - "Где прописана процедура ПТП?"
#    - "На основании какого документа это делается?"
#    - "Какие ГОСТы применяются?"

# 5. broad_overview
#    Это общий обзорный вопрос: функции отдела, общая суть документа, широкое описание темы.
#    Примеры:
#    - "Какие задачи у сотрудников отдела геологии?"
#    - "О чем документ по внешним поставкам?"
#    - "Как устроена система обращения с отходами?"

# Верни ответ ТОЛЬКО в JSON:
# {{
#   "question_type": "fact|definition|procedure|norm_reference|broad_overview",
#   "confidence": 0.0,
#   "reason": "краткое объяснение"
# }}

# Вопрос:
# "{question}"
# """.strip()

#     payload = {
#         "model": model_name,
#         "prompt": prompt,
#         "stream": False,
#         "options": {
#             "temperature": temperature
#         }
#     }

#     response = _post_to_ollama(payload)

#     if response.status_code != 200:
#         print("OLLAMA STATUS:", response.status_code)
#         print("OLLAMA BODY:", response.text)
#         response.raise_for_status()

#     result = response.json()
#     raw = result["response"]

#     data = _extract_json(raw)

#     allowed = {"fact", "definition", "procedure", "norm_reference", "broad_overview"}
#     qtype = str(data.get("question_type", "")).strip()
#     confidence = data.get("confidence", 0.0)
#     reason = str(data.get("reason", "")).strip()

#     if qtype not in allowed:
#         raise ValueError(f"LLM вернула неизвестный question_type: {qtype}")

#     try:
#         confidence = float(confidence)
#     except Exception:
#         confidence = 0.0

#     confidence = max(0.0, min(1.0, confidence))

#     return {
#         "question_type": qtype,
#         "confidence": confidence,
#         "reason": reason,
#         "raw_response": raw,
#     }


# if __name__ == "__main__":
#     test_questions = [
#         "Какие требования к оперативной памяти?",
#         "Что такое федеральный оператор?",
#         "Как у нас проходит закупка оборудования от начала до конца?",
#         "Где прописана процедура ПТП?",
#         "Какие задачи у сотрудников отдела геологии?",
#     ]

#     for q in test_questions:
#         result = classify_question(q)
#         print("=" * 80)
#         print("QUESTION:", q)
#         print(json.dumps(result, ensure_ascii=False, indent=2))


# # classifier.py
# from __future__ import annotations

# import json
# import re
# from typing import Any, Dict

# import requests

# from config import LOCAL_LLM_MODEL


# OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


# def _extract_json(text: str) -> Dict[str, Any]:
#     text = text.strip()

#     try:
#         return json.loads(text)
#     except Exception:
#         pass

#     match = re.search(r"\{.*\}", text, flags=re.DOTALL)
#     if match:
#         try:
#             return json.loads(match.group(0))
#         except Exception:
#             pass

#     raise ValueError(f"Не удалось извлечь JSON из ответа модели:\n{text}")


# def _post_to_ollama(payload: Dict[str, Any]) -> requests.Response:
#     session = requests.Session()
#     session.trust_env = False

#     return session.post(
#         OLLAMA_URL,
#         json=payload,
#         timeout=120,
#     )


# def _heuristic_answer_mode(question: str) -> str | None:
#     """
#     Простые безопасные эвристики поверх LLM:
#     - 'какие требования', 'список требований' => list
#     - 'как', 'порядок', 'этапы' => steps
#     """
#     q = question.lower().strip()

#     if any(x in q for x in [
#         "какие требования",
#         "какой список требований",
#         "перечень требований",
#         "какие обязанности",
#         "какие задачи",
#         "какие функции",
#         "какие правила",
#         "какие условия",
#         "какие документы",
#     ]):
#         return "list"

#     if any(x in q for x in [
#         "как ",
#         "каким образом",
#         "порядок",
#         "этапы",
#         "что делать",
#         "как проходит",
#         "как оформить",
#     ]):
#         return "steps"

#     return None


# def classify_question(
#     question: str,
#     model_name: str = LOCAL_LLM_MODEL,
#     temperature: float = 0.0,
# ) -> Dict[str, Any]:
#     """
#     Классифицирует вопрос:
#     - question_type: fact | definition | procedure | norm_reference | broad_overview
#     - answer_mode: single | list | steps | reference | summary
#     """

#     prompt = f"""
# Ты классификатор запросов для корпоративной системы поиска по нормативным документам.

# Нужно определить ДВЕ вещи:

# 1. question_type:
# - fact — точный факт, параметр, числовое требование, ограничение
# - definition — определение термина
# - procedure — порядок действий / процесс
# - norm_reference — в каком документе / разделе / пункте это прописано
# - broad_overview — обзор темы, функций, задач, обязанностей

# 2. answer_mode:
# - single — ожидается один короткий ответ / один параметр / один факт
# - list — ожидается список требований / условий / обязанностей / задач / правил
# - steps — ожидается пошаговая процедура
# - reference — ожидается ссылка на документ / раздел / пункт
# - summary — ожидается краткое обзорное описание

# Примеры:
# - "Какие требования к оперативной памяти?" =>
#   question_type=fact, answer_mode=single

# - "Какие требования к транспортированию отходов?" =>
#   question_type=fact, answer_mode=list

# - "Как проходит закупка оборудования?" =>
#   question_type=procedure, answer_mode=steps

# - "Где прописана процедура ПТП?" =>
#   question_type=norm_reference, answer_mode=reference

# - "Какие задачи у сотрудников отдела геологии?" =>
#   question_type=broad_overview, answer_mode=list

# Верни ТОЛЬКО JSON:
# {{
#   "question_type": "fact|definition|procedure|norm_reference|broad_overview",
#   "answer_mode": "single|list|steps|reference|summary",
#   "confidence": 0.0,
#   "reason": "краткое объяснение"
# }}

# Вопрос:
# "{question}"
# """.strip()

#     payload = {
#         "model": model_name,
#         "prompt": prompt,
#         "stream": False,
#         "options": {
#             "temperature": temperature
#         }
#     }

#     response = _post_to_ollama(payload)

#     if response.status_code != 200:
#         print("OLLAMA STATUS:", response.status_code)
#         print("OLLAMA BODY:", response.text)
#         response.raise_for_status()

#     result = response.json()
#     raw = result["response"]

#     data = _extract_json(raw)

#     allowed_types = {"fact", "definition", "procedure", "norm_reference", "broad_overview"}
#     allowed_modes = {"single", "list", "steps", "reference", "summary"}

#     qtype = str(data.get("question_type", "")).strip()
#     answer_mode = str(data.get("answer_mode", "")).strip()
#     confidence = data.get("confidence", 0.0)
#     reason = str(data.get("reason", "")).strip()

#     if qtype not in allowed_types:
#         raise ValueError(f"LLM вернула неизвестный question_type: {qtype}")

#     if answer_mode not in allowed_modes:
#         answer_mode = "summary"

#     # безопасная эвристическая коррекция
#     heuristic_mode = _heuristic_answer_mode(question)
#     if heuristic_mode is not None:
#         answer_mode = heuristic_mode

#     try:
#         confidence = float(confidence)
#     except Exception:
#         confidence = 0.0

#     confidence = max(0.0, min(1.0, confidence))

#     return {
#         "question_type": qtype,
#         "answer_mode": answer_mode,
#         "confidence": confidence,
#         "reason": reason,
#         "raw_response": raw,
#     }


# if __name__ == "__main__":
#     test_questions = [
#         "Какие требования к оперативной памяти?",
#         "Какие требования к транспортированию отходов?",
#         "Как у нас проходит закупка оборудования от начала до конца?",
#         "Где прописана процедура ПТП?",
#         "Какие задачи у сотрудников отдела геологии?",
#     ]

#     for q in test_questions:
#         result = classify_question(q)
#         print("=" * 80)
#         print("QUESTION:", q)
#         print(json.dumps(result, ensure_ascii=False, indent=2))


# classifier.py
from __future__ import annotations

import json
import re
from typing import Any, Dict

import requests

from config import LOCAL_LLM_MODEL


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


def _extract_json(text: str) -> Dict[str, Any]:
    text = text.strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass

    raise ValueError(f"Не удалось извлечь JSON из ответа модели:\n{text}")


def _post_to_ollama(payload: Dict[str, Any]) -> requests.Response:
    session = requests.Session()
    session.trust_env = False

    return session.post(
        OLLAMA_URL,
        json=payload,
        timeout=120,
    )


def _heuristic_answer_mode(question: str) -> str | None:
    q = question.lower().strip()

    if any(x in q for x in [
        "какие требования",
        "какой список требований",
        "перечень требований",
        "какие обязанности",
        "какие задачи",
        "какие функции",
        "какие правила",
        "какие условия",
        "какие документы",
        "какой список",
        "перечень",
    ]):
        return "list"

    if any(x in q for x in [
        "как ",
        "каким образом",
        "порядок",
        "этапы",
        "что делать",
        "как проходит",
        "как оформить",
        "какие шаги",
        "шаги процесса",
        "от начала до конца",
    ]):
        return "steps"

    if any(x in q for x in [
        "где прописана",
        "где указана",
        "в каком документе",
        "на основании какого документа",
        "каким документом регулируется",
        "какой пункт",
        "какой раздел",
        "где описана",
    ]):
        return "reference"

    return None


def classify_question(
    question: str,
    model_name: str = LOCAL_LLM_MODEL,
    temperature: float = 0.0,
) -> Dict[str, Any]:
    prompt = f"""
Ты классификатор запросов для корпоративной системы поиска по нормативным документам.

Нужно определить ДВЕ вещи:

1. question_type:
- fact — точный факт, параметр, числовое требование, ограничение
- definition — определение термина
- procedure — порядок действий / процесс
- norm_reference — в каком документе / разделе / пункте это прописано
- broad_overview — обзор темы, функций, задач, обязанностей

2. answer_mode:
- single — ожидается один короткий ответ / один параметр / один факт
- list — ожидается список требований / условий / обязанностей / задач / правил
- steps — ожидается пошаговая процедура
- reference — ожидается ссылка на документ / раздел / пункт
- summary — ожидается краткое обзорное описание

Примеры:
- "Какие требования к оперативной памяти?" =>
  question_type=fact, answer_mode=single

- "Какие требования к транспортированию отходов?" =>
  question_type=fact, answer_mode=list

- "Как проходит закупка оборудования?" =>
  question_type=procedure, answer_mode=steps

- "Где прописана процедура ПТП?" =>
  question_type=norm_reference, answer_mode=reference

- "Какие задачи у сотрудников отдела геологии?" =>
  question_type=broad_overview, answer_mode=list

Верни ТОЛЬКО JSON:
{{
  "question_type": "fact|definition|procedure|norm_reference|broad_overview",
  "answer_mode": "single|list|steps|reference|summary",
  "confidence": 0.0,
  "reason": "краткое объяснение"
}}

Вопрос:
"{question}"
""".strip()

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }

    response = _post_to_ollama(payload)

    if response.status_code != 200:
        print("OLLAMA STATUS:", response.status_code)
        print("OLLAMA BODY:", response.text)
        response.raise_for_status()

    result = response.json()
    raw = result["response"]

    data = _extract_json(raw)

    allowed_types = {"fact", "definition", "procedure", "norm_reference", "broad_overview"}
    allowed_modes = {"single", "list", "steps", "reference", "summary"}

    qtype = str(data.get("question_type", "")).strip()
    answer_mode = str(data.get("answer_mode", "")).strip()
    confidence = data.get("confidence", 0.0)
    reason = str(data.get("reason", "")).strip()

    if qtype not in allowed_types:
        raise ValueError(f"LLM вернула неизвестный question_type: {qtype}")

    if answer_mode not in allowed_modes:
        answer_mode = "summary"

    heuristic_mode = _heuristic_answer_mode(question)
    if heuristic_mode is not None:
        answer_mode = heuristic_mode

    try:
        confidence = float(confidence)
    except Exception:
        confidence = 0.0

    confidence = max(0.0, min(1.0, confidence))

    return {
        "question_type": qtype,
        "answer_mode": answer_mode,
        "confidence": confidence,
        "reason": reason,
        "raw_response": raw,
    }


if __name__ == "__main__":
    test_questions = [
        "Какие требования к оперативной памяти?",
        "Какие требования к транспортированию отходов?",
        "Как у нас проходит закупка оборудования от начала до конца?",
        "Где прописана процедура ПТП?",
        "Какие задачи у сотрудников отдела геологии?",
    ]

    for q in test_questions:
        result = classify_question(q)
        print("=" * 80)
        print("QUESTION:", q)
        print(json.dumps(result, ensure_ascii=False, indent=2))