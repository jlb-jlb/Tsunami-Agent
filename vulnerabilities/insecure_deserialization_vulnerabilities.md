## Insecure Deserialization

### Perform a Remote Code Execution that would keep a less hardened application busy forever
1.  Discover the B2B API documentation at `http://localhost:3000/api-docs`.
2.  This API allows submitting orders with `orderLinesData` as a string, which can contain arbitrary JSON.
3.  A payload for a denial-of-service attack via insecure JSON deserialization would be an endless loop: `{"orderLinesData": "(function dos() { while(true); })()"}`.
4.  Submit this payload to the `/orders` endpoint. The server will time out after about 2 seconds, but the challenge is marked as solved.

---

### Perform a Remote Code Execution that occupies the server for a while without using infinite loops
1.  Follow the steps for the "Perform a Remote Code Execution that would keep a less hardened application busy forever" challenge.
2.  Use the request body `{"orderLinesData": "/((a+)+)b/.test('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa')"}` to trigger a costly regular expression test.
3.  Submit the request. The server will time out after about 2 seconds with a 503 error, and the challenge will be solved.

---
