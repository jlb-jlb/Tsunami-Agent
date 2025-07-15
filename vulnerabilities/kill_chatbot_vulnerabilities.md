## Kill the Support Chatbot

### Disable the chatbot

1. Open the browser DevTools (Console).
2. Type and run:
```javascript
var script = document.createElement('script');
script.src = 'assets/public/images/uploads/disablebot.js';
document.body.appendChild(script);
```
