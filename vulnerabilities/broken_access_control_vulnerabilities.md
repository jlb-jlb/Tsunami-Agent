## Broken Access Control

### Access the administration section of the store
1.  Open the `main.js` in your browser's developer tools and search for "admin".
2.  One of the matches will be a route mapping to `path: "administration"`.
3.  Navigating to `http://localhost:3000/#/administration` will give a 403 Forbidden error.
4.  Log in with an administrator's account to access the page and solve the challenge.

---

### View another user's shopping basket
1.  Log in as any user.
2.  Put some products into your shopping basket.
3.  Inspect the Session Storage in your browser's developer tools to find a numeric `bid` value.
4.  Change the `bid`, for example, by adding or subtracting 1 from its value.
5.  Visit `http://localhost:3000/#/basket` to solve the challenge. You might need to reload the page.

---

### Register as a user with administrator privileges
1.  Submit a POST request to `http://localhost:3000/api/Users` with:
    * `{"email":"admin","password":"admin","role":"admin"}` as body
    * and `application/json` as `Content-Type`.

---

### Put an additional product into another user's shopping basket
1.  Log in as any user and find your own `BasketId`.
2.  Submit a POST request to `http://localhost:3000/api/BasketItems` with a payload that includes both your `BasketId` and the target's `BasketId` using HTTP Parameter Pollution: `{"ProductId": 14,"BasketId": "1","quantity": 1,"BasketId": "2"}`.
3.  This request will satisfy the validation based on your own `BasketId` but put the product into the other basket.

---

### Post some feedback in another user's name
1.  Go to the Contact Us form on `http://localhost:3000/#/contact`.
2.  Inspect the DOM to find a hidden input field: `<input _ngcontent-c23 hidden id="userId" ...>`.
3.  Remove the `hidden` attribute from the `<input>` tag in your browser's developer tools.
4.  The field should now be visible. Type any other user's database identifier in there and submit the feedback.

---

### Post a product review as another user or edit any user's existing review
1.  Select any product and write a review for it.
2.  Submit the review while observing the Networks tab of your browser.
3.  Analyze the `PUT` request. Change the `author` name in the Request Body to another user's email (e.g., `admin@juice-sh.op`) and re-send the request.

---

### Obtain a Deluxe Membership without paying for it
1.  Go to `http://localhost:3000/#/payment/deluxe`.
2.  Inspect the pay button next to the "pay using wallet" option and remove the `disabled="true"` attribute.
3.  Click the button and observe the `POST` request. It contains a `paymentMode` parameter set to "wallet".
4.  Right-click on the request and select "edit and resend". Change the `paymentMode` parameter to an empty string and send the request.

---

### Steal someone else's personal data without using Injection
1.  Create an order and notice your email is partially obfuscated in the order tracking response (e.g., `*dm*n@j**c*-sh.*p` for `admin@juice-sh.op`).
2.  Register a new user with an email address that would result in the exact same obfuscated email address (e.g., `edmin@juice-sh.op`).
3.  Log in with your new user and export your data via `http://localhost:3000/#/privacy-security/data-export`.
4.  The data export for your new user will include the orders of the original user due to the email obfuscation clash.

---

### Log in with the (non-existing) accountant without ever registering that user
1.  Solve "Exfiltrate the entire DB schema definition via SQL Injection" to learn the `Users` table column names.
2.  Prepare a `UNION SELECT` payload that creates a user on-the-fly with the role of "accounting".
3.  Log in with the crafted SQL Injection payload in the email field. For example: `' UNION SELECT * FROM (SELECT 15 as 'id', '' as 'username', 'acc0unt4nt@juice-sh.op' as 'email', '12345' as 'password', 'accounting' as 'role', ...)`.

---
