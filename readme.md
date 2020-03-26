# Notes

## Gunicorn
### Procfile explained
`web: gunicorn --chdir Core application:app`
Word | Explanation
-----|-------------
web  | Name of the instance gunicorn should start
gunicorn | The command gunicorn runs. Could also be python application.py
--chdir Core | Changing working directory before starting process
application | The name of the process you want to start. 
:app | This is tricky. This is the name of instance inside your function, so application in this example, that you want to do something with. In this case it is refering to app = Flask(__name__)




