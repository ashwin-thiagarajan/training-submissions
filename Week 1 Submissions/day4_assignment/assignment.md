# Day 4 Assignment: Pydantic

## Submission File

```text
day4_assignment.py
```

## Tasks

Create Pydantic models for:

- `Customer`
- `Product`
- `OrderItem`
- `Order`

## Validation Rules

- Customer email must be valid.
- Customer name must have at least 2 characters.
- Product price must be greater than 0.
- Product stock cannot be negative.
- Order item quantity must be greater than 0.
- Order status must be one of `PLACED`, `PAID`, `SHIPPED`, or `CANCELLED`.
- Order must contain at least one order item.

## Test Cases Required

Add examples for:

- One valid customer.
- One invalid customer email.
- One valid order.
- One invalid order with zero quantity.

## Evaluation

- Correct use of `BaseModel`.
- Correct field constraints.
- Correct nested model usage.
- Invalid data should fail validation.

