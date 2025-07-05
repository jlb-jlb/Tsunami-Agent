## Directory Traversal

### Access a confidential document
1.  On the About Us page, there is a link to the terms of use: `http://localhost:3000/ftp/legal.md`.
2.  By changing the URL to `http://localhost:3000/ftp`, you can browse the directory.
3.  From there, you can access the confidential document `acquisitions.md` at `http://localhost:3000/ftp/acquisitions.md`.

---

### Overwrite the Legal Information file
1.  This is a "Zip Slip" attack, which is a directory traversal vulnerability within a file archive.
2.  The goal is to overwrite `legal.md` in the `/ftp/` directory.
3.  Create a ZIP file with a file named using a directory traversal path, like `../../ftp/legal.md`.
4.  Upload this ZIP file through the "File Complaint" form. The file will be extracted outside of the intended directory, overwriting the `legal.md` file.