## Improper Input Validation

### Provoke an error that is neither very gracefully nor consistently handled
1.  Visit `http://localhost:3000/rest/qwertz`.
2.  Alternatively, log in to the application with `'` (single-quote) as Email and anything as Password.

---

### Follow the DRY principle while registering a user
1.  Go to `http://localhost:3000/#/register`.
2.  Fill out all required information except the Password and Repeat Password fields.
3.  Type a password into the Password field.
4.  Type the same password into the Repeat Password field.
5.  Go back to the Password field and change it. The Repeat Password field does not show the expected error.
6.  Submit the form to solve the challenge.

---

### Give a devastating zero-star feedback to the store
1.  Visit the Contact Us form and put in a Comment text and solve the CAPTCHA. The Submit button is still disabled because you did not select a Rating.
2.  Inspect the Submit button with your DevTools and remove the `disabled` attribute from the `<button>` HTML tag.
3.  Click the now-enabled Submit button to solve the challenge.

---

### Use a deprecated B2B interface that was not properly shut down
1.  Go to the File Complaint form.
2.  Open the `main.js` in your DevTools and find the file upload declaration. You will notice "application/xml" and "text/xml" in the `allowedMimeType` array.
3.  Click on the "Choose File" button. In the File Name field enter `*.xml` and select any arbitrary XML file.
4.  Enter some Message text and press Submit to solve the challenge. You will see a 410 (Gone) HTTP Error, indicating the interface is deprecated.

---

### Let the server sleep for some time
1.  You can interact with the backend API for product reviews via `/rest/products/{id}/reviews`.
2.  Inject a `sleep(integer ms)` command by changing the URL into `http://localhost:3000/rest/products/sleep(2000)/reviews` to solve the challenge. The server will wait for a maximum of 2 seconds.

---

### Update multiple product reviews at the same time
1.  Log in as any user to get your Authorization token.
2.  Submit a PATCH request to `http://localhost:3000/rest/products/reviews` with:
    * `{ "id": { "$ne": -1 }, "message": "NoSQL Injection!" }` as body
    * `application/json` as `Content-Type` header.
    * and your `Bearer` token in the `Authorization` header.

---

### Perform a Remote Code Execution that would keep a less hardened application busy forever
1.  Find the Swagger API documentation at `http://localhost:3000/api-docs` which describes the B2B API.
2.  The API allows POSTing orders where `orderLinesData` can be a string of arbitrary JSON.
3.  An insecure JSON deserialization would execute any function call defined within the JSON String. A possible payload for a DoS attack is `{"orderLinesData": "(function dos() { while(true); })()"}`.
4.  Submit this payload to the `/orders` endpoint. The server will time out after about 2 seconds, and the challenge will be solved.

---

### Give the server something to chew on for quite a while
1.  Solve the "Use a deprecated B2B interface that was not properly shut down" challenge.
2.  On Linux, prepare an XML file with an external entity that will take a long time to resolve: `<!ENTITY xxe SYSTEM "file:///dev/random">`. On Windows, a quadratic blowup attack can be used.
3.  Upload this file through the File Complaint dialog. The request will time out after about 2 seconds, but the challenge will be solved.

---
