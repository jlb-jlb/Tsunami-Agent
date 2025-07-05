## File Upload Vulnerabilities

### Upload a file larger than 100 kB
1.  The client-side validation prevents uploads larger than 100 kB.
2.  Craft a POST request to `http://localhost:3000/file-upload` with a form parameter `file` that contains a PDF file larger than 100 kB but less than 200 kB.
3.  The server will accept the file, and the challenge will be solved.

---

### Upload a file that has no .pdf or .zip extension
1.  Craft a POST request to `http://localhost:3000/file-upload` with a form parameter `file` that contains a non-PDF file smaller than 200 kB.
2.  The response from the server will be a 204 with no content, but the challenge will be successfully solved.

---

### Overwrite the Legal Information file
1.  This challenge involves a "Zip Slip" vulnerability, which is a form of directory traversal using file archives.
2.  The goal is to overwrite the `legal.md` file located at `/ftp/legal.md`.
3.  Prepare a ZIP file that contains a file with a directory traversal path as its name. On Linux, this would be `zip exploit.zip ../../ftp/legal.md`.
4.  Upload this ZIP file via the "File Complaint" screen. This will overwrite the `legal.md` file on the server and solve the challenge.

---

### Deprive the shop of earnings by downloading the blueprint for one of its products
1.  The description of the "OWASP Juice Shop Logo (3D-printed)" product suggests it has a blueprint.
2.  Download the product image and view its Exif metadata. The camera model is "OpenSCAD," a program that works with `.stl` files.
3.  A lucky guess or brute-force attack is needed to find the filename. Download `http://localhost:3000/assets/public/images/products/JuiceShop.stl` to solve the challenge.

---
