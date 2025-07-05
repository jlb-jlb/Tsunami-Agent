## XML External Entity (XXE) Injection

### Retrieve the content of C:\Windows\system.ini or /etc/passwd from the server
1.  Solve the "Use a deprecated B2B interface that was not properly shut down" challenge.
2.  Prepare an XML file that defines and uses an external entity, for example: `<!ENTITY xxe SYSTEM "file:///etc/passwd" >`.
3.  Upload this file through the "File Complaint" dialog. The server will parse the XML, and the error message in the JavaScript console will contain the contents of the local system file.

---

### Give the server something to chew on for quite a while
1.  This is a denial-of-service attack using XXE.
2.  On Linux, prepare an XML file with an external entity that points to a resource that takes a long time to resolve, like `<!ENTITY xxe SYSTEM "file:///dev/random">`.
3.  On Windows, a "quadratic blowup" attack can be used, which involves a large entity being replicated many times.
4.  Upload this file via the "File Complaint" dialog. The request will time out after about 2 seconds, but the challenge will be solved. The classic "billion laughs" attack is defended against.

---
