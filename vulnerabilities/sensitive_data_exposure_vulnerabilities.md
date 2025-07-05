## Sensitive Data Exposure

### Access a confidential document
1.  Follow the link to titled `Check out our boring terms of use if you are interested in such lame stuff` (`http://localhost:3000/ftp/legal.md`) on the About Us page.
2.  Successfully attempt to browse the directory by changing the URL into `http://localhost:3000/ftp`.
3.  Open `http://localhost:3000/ftp/acquisitions.md` to solve the challenge.

---

### Find the endpoint that serves usage data to be scraped by a popular monitoring system
1.  Scroll through `https://prometheus.io/docs/introduction/first_steps`.
2.  You should notice several mentions of `/metrics` as the default path scraped by Prometheus.
3.  Visit `http://localhost:3000/metrics` to view the actual Prometheus metrics of the Juice Shop and solve this challenge.

---

### Retrieve the photo of Bjoern's cat in "melee combat-mode"
1.  Visit `http://localhost:3000/#/photo-wall`.
2.  Right-click Inspect the broken image in the entry labeled "😼 #zatschi #whoneedsfourlegs".
3.  You should find an image tag with a `src` attribute like `assets/public/images/uploads/😼-#zatschi-#whoneedsfourlegs-1572600969477.jpg`.
4.  The `#` characters in the URL are interpreted by the browser as HTML anchors and not transmitted to the server. They must be URL-encoded into `%23`.
5.  Open `http://localhost:3000/assets/public/images/uploads/😼-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg` to view the photo and solve the challenge.

---

### Exfiltrate the entire DB schema definition via SQL Injection
1.  From any errors seen during previous SQL Injection attempts you should know that SQLite is the relational database in use. The schema is stored in `sqlite_master`.
2.  The `/rest/products/search` endpoint is susceptible to SQL Injection into the `q` parameter.
3.  The attack payload you need to craft is a `UNION SELECT` merging the data from the `sqlite_master` table.
4.  After finding the correct number of columns (9), the final payload is `qwert')) UNION SELECT sql, '2', '3', '4', '5', '6', '7', '8', '9' FROM sqlite_master--`.

---

### Retrieve a list of all user credentials via SQL Injection
1.  The `/rest/products/search` endpoint is susceptible to SQL Injection into the `q` parameter.
2.  Craft a `UNION SELECT` payload to merge data from the `Users` table.
3.  After finding the right number of columns (9), use the payload `qwert')) UNION SELECT id, email, password, '4', '5', '6', '7', '8', '9' FROM Users--` to retrieve the list of all user data.

---

### Learn about the Token Sale before its official announcement
1.  Open the `main.js` in your browser's developer tools and search for keywords like "ico", "token", "bitcoin" or "altcoin".
2.  You will find obfuscated JavaScript functions related to a token sale.
3.  By analyzing the route mappings, you'll find that the path is dynamically generated.
4.  You need to execute a piece of the obfuscated code in your browser's console to reveal the path, which is `/tokensale-ico-ea`.
5.  Navigate to `http://localhost:3000/#/tokensale-ico-ea` to solve this challenge.

---

### Gain access to any access log file of the server
1.  By exploring the `/ftp` folder, you might find clues about a support team.
2.  A brute force attack or lucky guess might lead you to the `/support/logs` directory.
3.  Inside `http://localhost:3000/support/logs`, you will find at least one `access.log` of the current day. Open or download it to solve this challenge.

---

### Access a developer's forgotten backup file
1.  Browse to `http://localhost:3000/ftp`.
2.  Opening `http://localhost:3000/ftp/package.json.bak` directly will fail.
3.  Use a Poison Null Byte (`%00`) to trick the filter. The `%` character needs to be URL-encoded as well (`%25`).
4.  Accessing `http://localhost:3000/ftp/package.json.bak%2500.md` will solve the challenge.

---

### Access a salesman's forgotten backup file
1.  Use the Poison Null Byte attack as described in "Access a developer's forgotten backup file".
2.  Download `http://localhost:3000/ftp/coupons_2013.md.bak%2500.md`.

---

### Access a misplaced SIEM signature file
1.  Use the Poison Null Byte attack as described in "Access a developer's forgotten backup file".
2.  Download `http://localhost:3000/ftp/suspicious_errors.yml%2500.md`.

---

### Dumpster dive the Internet for a leaked password and log in to the original user account it belongs to
1.  Visit `https://stackoverflow.com/questions/tagged/access-log` and look for questions related to Juice Shop's URL paths.
2.  You will find a link to a PasteBin (`https://pastebin.com/4U1V1UjU`) with leaked log files.
3.  Search for "password" in the paste to find a GET request with a password in the URL.
4.  The logged password is URL-encoded. Decode `0Y8rMnww$*9VFYE%C2%A759-!Fg1L6t&6lB` to `0Y8rMnww$*9VFYE§59-!Fg1L6t&6lB`.
5.  By performing a password spraying attack or comparing hashes, you'll find the password belongs to `J12934@juice-sh.op`. Log in with these credentials to solve the challenge.

---

### Retrieve the language file that never made it into production
1.  Monitoring network calls when switching languages reveals that translation files are loaded from `/i18n/` with the locale as the filename (e.g., `en.json`).
2.  The hidden language is Klingon, represented by the code `tlh_AA`.
3.  Request `http://localhost:3000/i18n/tlh_AA.json` to solve the challenge.

---
