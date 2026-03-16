# Multinorm Milvus API — DB Query

## Назначение

Endpoint `/query` предназначен для прямого обращения к Milvus как к базе данных  
(без semantic-поиска и без embedding).

Используется для:
- получения документа по `doc_id`
- выборки по `level`
- фильтрации по разделам
- восстановления структуры документа
- получения оглавления
- выборки по UUID

---

# Endpoint

POST /query

---

# Тело запроса

```json
{
  "collection": "documents",
  "filter": "level == 2",
  "limit": 10,
  "output_fields": ["title", "number"]
}
```

---

# Параметры

| Поле | Тип | Обязательное | Описание |
|------|------|-------------|----------|
| collection | string | да | Имя коллекции (обычно `documents`) |
| filter | string | нет | Milvus boolean expression |
| limit | int | нет | Максимальное количество записей |
| output_fields | array[string] | нет | Список полей для возврата |

---

# Поведение по умолчанию

Если `output_fields` **не указан**, возвращаются **все scalar-поля коллекции**  
(кроме векторных).

---

# Схема документа (коллекция `documents`)

Каждая запись содержит:

```json
{
  "text": "Текст фрагмента документа",
  "level": 2,
  "doc_id": "UUID документа",
  "section_id": "UUID раздела",
  "main_section_id": "UUID главного раздела",
  "subsection_id": "UUID подраздела",
  "title": "Заголовок раздела",
  "number": "4.13"
}
```

---

# Описание полей

| Поле | Тип | Описание |
|------|------|----------|
| text | string | Текст фрагмента |
| level | int | Уровень вложенности (0, 1, 2) |
| doc_id | string (UUID) | ID документа |
| section_id | string (UUID) | ID раздела |
| main_section_id | string (UUID) | ID главного раздела |
| subsection_id | string (UUID) | ID подраздела |
| title | string | Заголовок раздела |
| number | string | Номер раздела |

---

# Поддерживаемые операторы фильтрации (Milvus)

| Операция | Пример |
|----------|--------|
| Равенство | `level == 2` |
| Неравенство | `level != 0` |
| IN | `level in [0,1,2]` |
| AND | `level == 2 && doc_id == 'uuid'` |
| OR | `level == 0 || level == 1` |

⚠ Строковые значения должны быть в одинарных кавычках.

---

# Примеры запросов

## 1. Получить документ по `doc_id`

```json
{
  "collection": "documents",
  "filter": "doc_id == '7b794703-0883-48e6-a1bb-b08e8ea9e330'",
  "limit": 50
}
```

---

## 2. Получить все пункты уровня 0

```json
{
  "collection": "documents",
  "filter": "level == 0",
  "limit": 20
}
```

---

## 3. Получить уровни 1 и 2

```json
{
  "collection": "documents",
  "filter": "level in [1, 2]",
  "limit": 50
}
```

---

## 4. Получить конкретный раздел

```json
{
  "collection": "documents",
  "filter": "section_id == '52b9436b-8719-49b4-a893-636412a0114b'",
  "limit": 20
}
```

---

## 5. Вернуть только нужные поля

```json
{
  "collection": "documents",
  "filter": "level == 2",
  "limit": 10,
  "output_fields": ["title", "number"]
}
```

---

# Пример ответа

```json
{
  "collection": "documents",
  "filter": "level == 2",
  "limit": 10,
  "results": [
    {
      "text": "...",
      "level": 2,
      "doc_id": "7b794703-0883-48e6-a1bb-b08e8ea9e330",
      "section_id": "52b9436b-8719-49b4-a893-636412a0114b",
      "main_section_id": "fc691ce7-ce51-4ff1-a031-a47889bd8138",
      "subsection_id": "05b9a65e-2721-4746-8b43-3ed28c2a09e6",
      "title": "4.13 ...",
      "number": "4.13"
    }
  ]
}
```

---

# Ограничения

- Фильтрация работает только по scalar-полям
- Векторные поля не участвуют
- UUID обязательно в кавычках
- При отсутствии `filter` будет возвращено ограниченное количество записей (`limit`)

---

# Когда использовать `/query`

Использовать если нужно:

✔ получить конкретный документ  
✔ собрать иер