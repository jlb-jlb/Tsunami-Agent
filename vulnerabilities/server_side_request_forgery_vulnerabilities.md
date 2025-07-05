## Server-Side Request Forgery (SSRF)

### Request a hidden resource on server through server
1.  The vulnerable input field for this SSRF attack is the Gravatar URL on the `/profile` page.
2.  The server downloads the image from the provided URL, indicating a potential SSRF vulnerability.
3.  By decompiling or proxying the "juicy malware" (from another challenge), you can find a secret URL: `http://localhost:3000/solve/challenges/server-side?key=tRy_H4rd3r_n0thIng_iS_Imp0ssibl3`.
4.  Visiting this URL directly will not work. You must paste it into the Gravatar URL field and click "Link Gravatar" to trigger the SSRF and solve the challenge.

---
