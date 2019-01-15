
# coding: utf-8

# In[1]:


from os import environ
from flask import Flask

app = Flask(__name__)
app.run(environ.get('80'))

