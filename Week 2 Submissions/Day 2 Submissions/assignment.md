# Day 2 Assignment: Currency Conversion API Without ORM

## Submission Folder

```text
day2_django_no_orm_currency_api/
```

Use this reference template for Django project conventions:

```text
week2_training/standard_templates/django_qtx_reference/
```

Do not copy it blindly. Adapt the structure to the currency API and apply the Week 2 quality checklist.

## Objective

Build a Django REST Framework API that converts an amount between currencies without using Django ORM.

## Endpoint

| Method | Path | Behavior |
| --- | --- | --- |
| `POST` | `/api/v1/convert-currency/` | Convert amount from one currency to another |

## Request Body

```json
{
  "amount": 100,
  "from_currency": "USD",
  "to_currency": "INR"
}
```

## Response Body

```json
{
  "amount": 100,
  "from_currency": "USD",
  "to_currency": "INR",
  "converted_amount": 8350,
  "rate": 83.5
}
```

## Requirements

- Use a fixed in-memory exchange-rate dictionary in `services.py`.
- Do not use Django models.
- Validate request data using Pydantic.
- Amount must be greater than 0.
- Unsupported currency must return `400 Bad Request`.
- Same source and target currency must return `400 Bad Request`.
- Keep exchange-rate config in one place.
- Add logging for conversion attempts.

## Required Tests

- Successful conversion returns `200`.
- Negative amount returns `400`.
- Unsupported currency returns `400`.
- Same source and target currency returns `400`.
- Simulated service exception returns structured `500`.
