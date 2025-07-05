## SQL Injection

### Log in with the administrator's user account
1.  Use the SQL Injection payload `' or 1=1--` as the email and any password. This will authenticate you as the first user in the database, which is the administrator.
2.  Alternatively, if you know the administrator's email, you can use `admin@juice-sh.op'--` as the email and any password.

---

### Exfiltrate the entire DB schema definition via SQL Injection
1.  The `/rest/products/search` endpoint is vulnerable to SQL Injection in the `q` parameter.
2.  Use a `UNION SELECT` statement to merge data from the `sqlite_master` table, which contains the database schema in SQLite.
3.  After determining the correct number of columns (9), the payload `qwert')) UNION SELECT sql, '2', '3', '4', '5', '6', '7', '8', '9' FROM sqlite_master--` will return the schema.

---

### Retrieve a list of all user credentials via SQL Injection
1.  Using the same vulnerable endpoint (`/rest/products/search`), craft a `UNION SELECT` payload to retrieve data from the `Users` table.
2.  The payload `qwert')) UNION SELECT id, email, password, '4', '5', '6', '7', '8', '9' FROM Users--` will return a list of all users' IDs, emails, and password hashes.

---

### Order the Christmas special offer of 2014
1.  Use blind SQL Injection on the `/rest/products/search` endpoint with the `q` parameter. The payload `'))--` will retrieve all products, including logically deleted ones.
2.  Take note of the ID of the "Christmas Super-Surprise-Box (2014 Edition)" (which should be 10).
3.  Add this product to your basket by sending a POST request to `/api/BasketItems` with `{"BasketId": "<Your Basket ID>", "ProductId": 10, "quantity": 1}`.
4.  Checkout to solve the challenge.

---

### Log in with the (non-existing) accountant without ever registering that user
1.  This is an advanced SQL Injection that creates a user "on the fly" during the login process.
2.  You need to know the exact column names of the `Users` table (from the schema exfiltration challenge).
3.  Craft a `UNION SELECT` payload for the email field that will return a user with the `accounting` role, for example: `' UNION SELECT * FROM (SELECT 15 as 'id', '' as 'username', 'acc0unt4nt@juice-sh.op' as 'email', '12345' as 'password', 'accounting' as 'role', ...)`.
4.  This tricks the backend into issuing a valid JWT for this non-existent user.

---
