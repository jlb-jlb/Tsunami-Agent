## Vulnerable Components

### Inform the shop about an algorithm or library it should definitely not use the way it does
1.  Juice Shop uses inappropriate crypto algorithms and libraries, which can be discovered by working on other challenges and having the `package.json.bak` file. Examples include `z85`, `hashid`, unsalted `MD5`, and `Base64`.
2.  Visit `http://localhost:3000/#/contact`.
3.  Submit your feedback with one of the following words in the comment: `z85`, `base85`, `base64`, `md5` or `hashid`.

---

### Inform the shop about a vulnerable library it is using
1.  Solve "Access a developer's forgotten backup file" to get `package.json.bak`.
2.  Check the dependencies in `package.json.bak` for known vulnerabilities online. You will find matches for `sanitize-html` and `express-jwt`.
3.  Visit `http://localhost:3000/#/contact`.
4.  Submit your feedback with the string pair `sanitize-html` and `1.4.2` or `express-jwt` and `0.1.3` in the comment.

---

### Inform the shop about a typosquatting trick it has been a victim of
1.  Solve the "Access a developer's forgotten backup file" challenge and open the `package.json.bak` file.
2.  Scrutinize the dependencies list and you will find `epilogue-js`, which is a typosquatted version of `epilogue`.
3.  Visit `http://localhost:3000/#/contact`.
4.  Submit your feedback with `epilogue-js` in the comment to solve this challenge.

---

### Inform the development team about a danger to some of their credentials
1.  Solve "Access a developer's forgotten backup file".
2.  The `package.json.bak` file contains development dependencies under the `devDependencies` section.
3.  Research vulnerabilities in these dependencies. For the `eslint-scope` module in version `3.7.2`, you will learn about a software supply chain attack.
4.  Visit `http://localhost:3000/#/contact`.
5.  Submit your feedback with the link to the vulnerability report (e.g., `https://github.com/eslint/eslint-scope/issues/39`) in the comment to solve this challenge.

---

### Inform the shop about a typosquatting imposter that dug itself deep into the frontend
1.  Request `http://localhost:3000/3rdpartylicenses.txt` to retrieve the 3rd party license list.
2.  Combing through the list of modules you will come across `anuglar2-qrcode`, which is a typosquatted package.
3.  Visit `http://localhost:3000/#/contact`.
4.  Submit your feedback with `anuglar2-qrcode` in the comment to solve this challenge.

---
