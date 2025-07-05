## Weak Passwords

### Log in with the administrator's user credentials without previously changing them or applying SQL Injection
1.  Visit `http://localhost:3000/#/login`.
2.  Log in with Email `admin@juice-sh.op` and Password `admin123`, which is a weak, default password.

---

### Log in with MC SafeSearch's original user credentials
1.  Research "MC SafeSearch" to find the music video "Protect Ya' Passwordz".
2.  The video reveals that his password is his dog's name, "Mr. Noodles," with some vowels changed to zeroes.
3.  Log in with Email `mc.safesearch@juice-sh.op` and Password `Mr. N00dles`.

---

### Log in with Amy's original user credentials
1.  Research "One Important Final Note" to learn about password padding.
2.  Amy used her husband's name, "Kif," as `K1f`, followed by 21 dots for padding: `K1f.....................`.
3.  Log in with Email `amy@juice-sh.op` and this password.

---

### Log in with Jim's user account
1.  You can either use SQL Injection (`jim@juice-sh.op'--`) or crack his password hash.
2.  The password is `ncc-1701`, a reference to the USS Enterprise from Star Trek, which is hinted at in his product reviews and recycling request.

---
