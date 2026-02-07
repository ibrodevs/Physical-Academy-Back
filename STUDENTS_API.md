# Students API Documentation

## Base URL

```
http://localhost:8000/api/students/
```

## Language Support

All endpoints support language parameter: `?lang=ru` (default), `?lang=kg`, `?lang=en`

---

## 1. Student Support

**GET** `/api/students/support/?lang=ru`

**Response:**

```json
[
  {
    "id": 1,
    "text": "<p>Text content in selected language...</p>"
  }
]
```

---

## 2. Students Council

**GET** `/api/students/council/?lang=ru`

**Response:**

```json
[
  {
    "id": 1,
    "text": "<p>Council text content...</p>"
  }
]
```

---

## 3. Student Exchange Programs

**GET** `/api/students/exchange/?lang=ru`

**Response:**

```json
[
  {
    "id": 1,
    "name": "Exchange Program Name",
    "desc": "Program description",
    "photo": "http://localhost:8000/media/path/to/image.jpg"
  }
]
```

---

## 4. Student Instructions

**GET** `/api/students/instructions/?lang=ru`

**Response:**

```json
[
  {
    "id": 1,
    "pdf": "http://localhost:8000/media/path/to/file.pdf"
  }
]
```

---

## 5. Scholarship Programs

**GET** `/api/students/scholarships/?lang=ru`

**Response:**

```json
[
  {
    "id": 1,
    "name": "Scholarship Program Name",
    "description": "Program description",
    "eligibility_criteria": "Eligibility criteria text",
    "amount": "5000.00",
    "currency": "KGS",
    "application_deadline": "2026-12-31",
    "application_link": "https://example.com/apply",
    "contact_email": "scholarship@academy.kg",
    "contact_phone": "+996 123 45 67",
    "is_active": true,
    "required_documents": [
      {
        "id": 1,
        "name": "Passport",
        "description": "Valid passport copy",
        "is_required": true,
        "order": 1
      }
    ]
  }
]
```

---

## 6. Scholarship Required Documents

**GET** `/api/students/scholarships/documents/?lang=ru`

**Response:**

```json
[
  {
    "id": 1,
    "name": "Document Name",
    "description": "Document description",
    "is_required": true,
    "order": 1
  }
]
```

---

## Quick Examples

### Get all support texts in English

```
GET /api/students/support/?lang=en
```

### Get scholarship programs in Kyrgyz

```
GET /api/students/scholarships/?lang=kg
```

### Get exchange programs with default language (Russian)

```
GET /api/students/exchange/
```

---

## Notes

- All endpoints return arrays of objects
- Use `?lang=ru`, `?lang=kg`, or `?lang=en` for language selection
- Default language is Russian (`ru`)
- File URLs are absolute and ready to use
- HTML content in text fields is pre-rendered
