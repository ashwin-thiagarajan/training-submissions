# Day 1 Assignment: Django ORM Order API

## Submission Folder

```text
day1_django_orm_order_api/
```

Use this reference template for Django project conventions:

```text
week2_training/standard_templates/django_qtx_reference/
```

Do not copy it blindly. Adapt the structure to the order API and apply the Week 2 quality checklist.

## Objective

Build an order-management API using Django REST Framework and Django ORM.

## Required Models

Create:

- `Customer`
- `Product`
- `Order`
- `OrderItem`

## Required Endpoints

| Method | Path | Behavior |
| --- | --- | --- |
| `POST` | `/api/v1/customers/` | Create customer |
| `POST` | `/api/v1/products/` | Create product |
| `POST` | `/api/v1/orders/` | Create order with items |
| `GET` | `/api/v1/orders/{id}/` | Return order with customer and item details |
| `GET` | `/api/v1/customers/{id}/orders/` | Return all orders for a customer |

## Validation Rules

- Customer email must be valid and unique.
- Product price must be greater than 0.
- Product stock cannot be negative.
- Order must contain at least one item.
- Order item quantity must be greater than 0.
- Order creation must fail with `409 Conflict` when requested quantity is greater than available stock.

## Technical Requirements

- Use `ModelSerializer`.
- Use Pydantic schemas for order-creation service input.
- Use `transaction.atomic()` for order creation.
- Use `select_related()` and `prefetch_related()` for order detail APIs.
- Keep stock update logic in `services.py`.
- Use logging for create-order success and failure paths.
- Write tests for successful order creation, invalid payload, insufficient stock, and missing order ID.

## Evaluation

| Area | Weight |
| --- | ---: |
| ORM model design and migrations | 20% |
| Serializer validation | 20% |
| Transaction-safe service logic | 20% |
| Status codes and error response shape | 15% |
| Tests | 20% |
| Logging and structure | 5% |
