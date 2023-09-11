# Letter Generator

# About

Life is too short for cover letters and we generally use templates for that :). However even replacing values are a headache and I wanted to make that easier. I named this little project as Letter Generator because I want to extend with additional capabilities. So, don't hesitate to request it from me :)

# How does it work?

You can simply write a template article or letter and state the places you want to be replaced with squared brackets such as [Company Name]. Don't forget to add these to the args node with their corresponding value.

```
$ uvicorn main:app --host 0.0.0.0 --port 5000
$ cd lettergenerator
$ python3 manage.py runserver
```

# What's next?

- I'll make ui more prettier than this :) 
- Security stuff