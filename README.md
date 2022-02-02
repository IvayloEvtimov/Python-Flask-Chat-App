# Python Flask Chat App

## Course project done during Python Development Course at NBU

---

### **Overview**

Basic chat messenger app capable of sending and receiving messages in the form of text, image or video between 2 users

### **Dependencies:**

flask,werkzeug libraries for Python

---

### **File Structure**

- flaskr/
  - static/
  - templates/
    - auth/ - login and register templates
    - chat/ - main chat template
  - _init__.py
  - auth.py - logic for authenticanting and creating new users
  - chat.py - main logic
  - db.py - NOSQL database connection logic
