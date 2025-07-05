## Unvalidated Redirects

### Let us redirect you to one of our crypto currency addresses
1.  Log in to the application with any user.
2.  Visit the Your Basket page and perceive that all donation links are passed through the `to` parameter of the `/redirect` route.
3.  Open `main.js` in your browser's DevTools and search for `/redirect?to=` to find hidden functions that are called from the Your Basket page.
4.  Open one of the three URLs, e.g., `http://localhost:3000/redirect?to=https://blockchain.info/address/1AbKfgvw9psQ41NbLi8kufDQTezwG8DRZm` to solve the challenge.

---

### Enforce a redirect to a page you are not supposed to redirect to
1.  Pick one of the redirect links in the application, e.g., `http://localhost:3000/redirect?to=https://github.com/juice-shop/juice-shop`.
2.  Trying to redirect to an unrecognized URL fails due to an allowlist validation.
3.  Craft a redirect URL so that the target URL in the `to` parameter comes with its own parameter containing a URL from the allowlist, e.g., `http://localhost:3000/redirect?to=http://kimminich.de?pwned=https://github.com/juice-shop/juice-shop`.

---
