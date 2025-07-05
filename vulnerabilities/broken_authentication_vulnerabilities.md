## Broken Authentication

### Log in with the administrator's user account
1.  Log in with Email `' or 1=1--` and any Password, which will authenticate the first entry in the Users table (the administrator).
2.  Or log in with Email `admin@juice-sh.op'--` and any Password if you know the administrator's email address.
3.  Or log in with Email `admin@juice-sh.op` and Password `admin123` if you have retrieved the password hash and cracked it.

---

### Log in with MC SafeSearch's original user credentials
1.  Googling "MC SafeSearch" will lead you to the music video "Protect Ya' Passwordz".
2.  Watch the video to learn that MC used his dog's name "Mr. Noodles" as a password but changed "some vowels into zeroes".
3.  Log in with Email `mc.safesearch@juice-sh.op` and Password `Mr. N00dles`.

---

### Log in with the administrator's user credentials without previously changing them or applying SQL Injection
1.  Visit `http://localhost:3000/#/login`.
2.  Log in with Email `admin@juice-sh.op` and Password `admin123`.

---

### Determine the answer to John's security question
1.  Find the photo posted by `j0hNny` on the photo wall and check its metadata to get the coordinates where it was taken.
2.  Search for these coordinates on Google to find out the location is Daniel Boone National Forest.
3.  Go to the "Forgot your password?" page, enter `john@juice-sh.op` as the email, and `Daniel Boone National Forest` as the answer to the security question.

---

### Determine the answer to Emma's security question
1.  Find the photo posted by `E=ma²` on the photo wall.
2.  Zoom in on the image to see a logo of a company named `ITsec`.
3.  Go to the "Forgot your password?" page, enter `emma@juice-sh.op` as the email, and `ITsec` as the answer to the security question.

---

### Log in with Chris' erased user account
1.  Log in with Email `chris.pike@juice-sh.op'--` and any Password if you know Chris's email address.
2.  Or log in with Email as `' or deletedAt IS NOT NULL--` and any Password, as Chris is likely the only or first deleted user.

---

### Log in with Amy's original user credentials
1.  Researching "93.83 billion trillion trillion centuries" or "One Important Final Note" will lead you to information about Password Padding.
2.  Amy used a similar padding trick with her husband's name, Kif, written as `K1f`, with the same padding length as the example: `K1f.....................`.
3.  Log in with Email `amy@juice-sh.op` and this password.

---

### Log in with Bender's user account
1.  Log in with Email `bender@juice-sh.op'--` and any Password if you know Bender's email address.
2.  Alternatively, solve "Change Bender's password into slurmCl4ssic without using SQL Injection or Forgot Password" first and then log in with the new password.

---

### Log in with Jim's user account
1.  Log in with Email `jim@juice-sh.op'--` and any Password if you know Jim's email address.
2.  Or log in with Email `jim@juice-sh.op` and Password `ncc-1701` if you have cracked his password hash.

---

### Reset the password of Bjoern's OWASP account via the Forgot Password mechanism
1.  Visit the "Forgot Password" page and enter `bjoern@owasp.org` to see the security question is "Name of your favorite pet?".
2.  Find Bjoern's Twitter profile to discover his cat's name is "Zaya".
3.  Use "Zaya" as the answer to reset the password.

---

### Reset Jim's password via the Forgot Password mechanism
1.  Visit the "Forgot Password" page and enter `jim@juice-sh.op` to see his security question is "Your eldest siblings middle name?".
2.  Clues in the application reveal Jim's identity is James T. Kirk.
3.  Wikipedia will tell you his brother is George Samuel Kirk. Use "Samuel" as the answer to reset the password.

---

### Log in with Bjoern's Gmail account
1.  Inspect the `main.js` file to find that for OAuth logins, the password is the user's reversed email address, Base64-encoded.
2.  Base64-encode the reversed email of `bjoern.kimminich@googlemail.com` to get the password `bW9jLmxpYW1nQGhjaW5pbW1pay5ucmVvamI=`.
3.  Log in with these credentials.

---

### Reset Bender's password via the Forgot Password mechanism
1.  Researching "Bender" from Futurama reveals his first job was at a factory for "Stop'n'Drop" suicide booths.
2.  Use "Stop'n'Drop" as the answer to his security question to reset the password.

---

### Reset Uvogin's password via the Forgot Password mechanism
1.  Using a tool like Sherlock on variations of "uvogin" (like "uv0gin") leads to a Twitter account.
2.  Using the Wayback Machine on this Twitter profile reveals a deleted tweet mentioning "Silence of the Lambs," which is the answer to his security question.

---

### Reset Morty's password via the Forgot Password mechanism
1.  Researching "Morty" leads to Morty Smith from Rick and Morty, whose dog was named Snuffles/Snowball.
2.  A rate-limited brute-force attack is needed. Write a script that tries mutations of "snuffles" and "snowball," bypassing the rate limit by changing the `X-Forwarded-For` header in each request.
3.  The correct answer is `5N0wb41L`.

---

### Forge an essentially unsigned JWT token
1.  Log in as any user to get a valid JWT.
2.  Decode the JWT. In the payload, change the `email` to `jwtn3d@juice-sh.op`.
3.  In the header, change the `alg` (algorithm) from `HS256` to `none`.
4.  Re-encode the header and payload and join them with a dot, adding another dot at the end (`base64url(header).base64url(payload).`).
5.  Use this new JWT in the `Authorization` header or as a cookie to impersonate the user.

---

### Log in with the support team's original user credentials
1.  Find the support team's KeePass database at `http://localhost:3000/ftp/incident-support.kdbx`.
2.  Inspecting `main.js` reveals a log message in Romanian and a regex for the corporate password policy for privileged accounts.
3.  Use a brute-force script that follows this password policy to crack the KeePass file password, which is `Support2022!`.
4.  Inside the KeePass file, find the password for the `support@juice-sh.op` user account: `J6aVjTgOpRs@?5l!Zkq2AYnCE@RF$P`.
5.  Log in with these credentials.

---

### Solve the 2FA challenge for user "wurstbrot"
1.  Using SQL Injection on the product search, find the `totpsecret` column in the `Users` table.
2.  Retrieve the `totpsecret` for `wurstbrot@juice-sh.op`: `IFTXE3SPOEYVURT2MRYGI52TKJ4HC3KH`.
3.  Add this key to a 2FA application (like Google Authenticator).
4.  Log in as `wurstbrot@juice-sh.op` using SQL Injection, then enter the 6-digit code from your 2FA app to solve the challenge.

---

### Forge an almost properly RSA-signed JWT token
1.  Download the public JWT key from `http://localhost:3000/encryptionkeys/jwt.pub`.
2.  Using a tool like Burp Suite with the "JSON Web Token Attacker" extension, modify the email in a captured JWT payload to `rsa_lord@juice-sh.op`.
3.  In the attacker tab, use the "Key Confusion" attack, loading the public key. This tricks the server into using the public key to verify a token signed with the same public key (as if it were a symmetric key).
4.  Send the modified request to solve the challenge.

---
