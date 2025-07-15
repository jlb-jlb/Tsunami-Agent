## Basket Access and Manipulation

### Access another user's basket

1. Log in as any user and go to `My Basket`.
2. Inspect browser Storage > Session Storage.
3. Note the `bid` (Basket ID) and try manually changing it to another number like `1`, `2`, etc.
4. Refresh the basket view — if successful, you accessed another user's basket.

---

### Manipulate basket item quantity

1. Use browser dev tools or Postman to send:
```http
PUT /api/BasketItems/:id
Authorization: Bearer <your-token>
{
  "quantity": -100
}
2. Reload the basket and see the quantity reflect negative values.
