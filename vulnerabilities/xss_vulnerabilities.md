## XSS Vulnerabilities

### Use the bonus payload in the DOM XSS challenge
1.  Solve the Perform a DOM XSS attack challenge.
2.  Turn on your computer's speakers!
3.  Paste the payload `<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>` into the `Search...` field and hit Enter.
4.  Enjoy the excellent acoustic entertainment!

---

### Perform a DOM XSS attack
1.  Paste the attack string `<iframe src="javascript:alert('xss')">` into the `Search...` field.
2.  Hit the Enter key.
3.  An alert box with the text "xss" should appear.

---

### Perform a reflected XSS attack
1.  Log in as any user.
2.  Do some shopping and then visit the Order History.
3.  Clicking on the little "Truck" button for any of your orders will show you the delivery status of your order.
4.  Notice the `id` parameter in the URL `http://localhost:3000/#/track-result?id=fe01-f885a0915b79f2a9` with `fe01-f885a0915b79f2a9` being one of your order numbers.
5.  As the `fe01-f885a0915b79f2a9` is displayed on the screen, it might be susceptible to an XSS attack.
6.  Paste the attack string `<iframe src="javascript:alert('xss')">` into that URL so that you have `http://localhost:3000/#/track-result?id=%3Ciframe%20src%3D%22javascript:alert(%60xss%60)%22%3E`.
7.  Refresh that URL to get the XSS payload executed and the challenge marked as solved.

---

### Perform a persisted XSS attack bypassing a client-side security mechanism
1.  Submit a POST request to `http://localhost:3000/api/Users` with:
    * `{"email": "<iframe src=\"javascript:alert('xss')\">", "password": "xss"}` as body
    * `application/json` as `Content-Type` header.
2.  Log in to the application with an admin.
3.  Visit `http://localhost:3000/#/administration`.
4.  An alert box with the text "xss" should appear.

---

### Perform a persisted XSS attack without using the frontend application at all
1.  Log in to the application with any user.
2.  Copy your `Authorization` header from any HTTP request submitted via browser.
3.  Submit a POST request to `http://localhost:3000/api/Products` with:
    * `{"name": "XSS", "description": "<iframe src=\"javascript:alert('xss')\">", "price": 47.11}` as body,
    * `application/json` as `Content-Type`
    * and `Bearer ?` as `Authorization` header, replacing the `?` with the token you copied from the browser.
4.  Visit `http://localhost:3000/#/search`.
5.  An alert box with the text "xss" should appear.

---

### Bypass the Content Security Policy and perform an XSS attack on a legacy page
1.  Log in as any user.
2.  Visit our user profile page at `http://localhost:3000/profile`.
3.  Change the username into `<script>alert('xss')</script>` and click Set Username. Notice the displayed username under the profile picture now is `lert('xss')` while in the Username field it shows `lert('xss')</script>` - a clear indication that the malicious input was sanitized.
4.  Change the username into `<<a|ascript>alert('xss')</script>` and click Set Username. The naive sanitizer only removes `<a|a` effectively changing the username into `<script>alert('xss')</script>` but you'll notice that the script is still not executed.
5.  Set the Image URL to some invalid image URL, e.g. `http://definitely.not.an/image.png`. While the linking fails and your profile will show a broken image, the CSP header will now contain `http://definitely.not.an/image.png;` - the originally supplied URL.
6.  Set `https://a.png; script-src 'unsafe-inline' 'self' 'unsafe-eval' https://code.getmdl.io http://ajax.googleapis.com` as Image URL and click \_Link Image.
7.  Refresh the page to give the browser the chance to load the tampered CSP and enjoy the alert box popping up!

---

### Perform a persisted XSS attack bypassing a server-side security mechanism
1.  In the `package.json.bak` you might have noticed the pinned dependency `"sanitize-html": "1.4.2"`. Internet research will yield a reported Cross-site Scripting (XSS) vulnerability, which was fixed with version 1.4.3. The referenced GitHub issue explains the problem and gives an exploit example: `I am not harmless: <<img src="csrf-attack"/>img src="csrf-attack"/>` is sanitized to `I am not harmless: <img src="csrf-attack"/>`.
2.  Visit `http://localhost:3000/#/contact`.
3.  Enter `<<script>Foo</script>iframe src="javascript:alert('xss')">` as Comment.
4.  Choose a rating and click Submit.
5.  Visit `http://localhost:3000/#/about` for a first "xss" alert.
6.  Visit `http://localhost:3000/#/administration` for a second "xss" alert.

---

### Perform a persisted XSS attack through an HTTP header
1.  Log in as any user.
2.  Visit `http://localhost:3000/#/privacy-security/last-login-ip`.
3.  Log out and then log in again.
4.  Find the request to `https://localhost:3000/rest/saveLoginIp` in your Browser DevTools.
5.  Replay the request after adding the `True-Client-IP` header with the value `<iframe src="javascript:alert('xss')">`.
6.  Log in again and visit `http://localhost:3000/#/privacy-security/last-login-ip` to see the alert popup.

---

### Embed an XSS payload into our promo video
1.  Visit `http://localhost:3000/promotion` and view the source to see the video is at `http://localhost:3000/video` with subtitles embedded.
2.  Access the subtitle file directly at `http://localhost:3000/assets/public/videos/owasp_promo.vtt`.
3.  The goal is to overwrite this file using a Zip Slip vulnerability. The correct path on the server is `frontend/dist/frontend/assets/public/videos/owasp_promo.vtt`.
4.  Prepare a ZIP file with an `owasp_promo.vtt` inside that contains the payload `</script><script>alert('xss')</script>` and the path `../../frontend/dist/frontend/assets/public/video/owasp_promo.vtt` (on Linux).
5.  Upload the ZIP file on `http://localhost:3000/#/complain`.
6.  Visit `http://localhost:3000/promotion` again to trigger the XSS payload.

---
