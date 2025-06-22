# About
Backend of our [project](https://github.com/FairCoalitionCasesDistributionProject), made using [Django Rest Framework](https://www.django-rest-framework.org). Used to evaluate a fair division using [Fairpy](https://github.com/erelsgl/fairpy) implementations as well as to save/restore user sessions using [Firebase](https://firebase.google.com/) database.<br />
Deployed with [Render](https://render.com/). <br />


## Running and Installing Guide
* Clone Repository <br /> 
``` git clone https://github.com/FairCoalitionCasesDistributionProject/Backend.git```


* Virtual Environment Setup<br />
It is strongly recommended to use python virtual environment. [For more information.](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
  * Installation <br />
``` pip install --user virtualenv```

  * Creation <br />
``` python -m venv env ```

  * Activation <br />
``` .\env\Scripts\activate ```

* For Linux <br />
  * Install the virtual environment <br />
  ``` pip install virtualenv ```

  * Creation <br />
  ``` virtualenv env ```

  * Activation <br />
  ``` source env/bin/activate ```

* Dependencies installation
``` pip install -r requirements.txt```

### Environment Variables Setup
This project uses environment variables for all sensitive configuration. **You must create a `.env` file in the project root before running the server.**

You can copy the template:
```sh
cp env.example .env
```
Then fill in all required values (see below).

#### Required Environment Variables
- `DJANGO_SECRET_KEY` - Django secret key (generate with `python generate_secret_key.py`)
- `DEBUG` - Set to `False` for production
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `CORS_ALLOWED_ORIGINS` - Comma-separated list of allowed CORS origins
- `DATABASE_URL` - (Optional) Production database URL
- **Firebase Configuration:**
  - `FIREBASE_API_KEY`
  - `FIREBASE_AUTH_DOMAIN`
  - `FIREBASE_PROJECT_ID`
  - `FIREBASE_STORAGE_BUCKET`
  - `FIREBASE_MESSAGING_SENDER_ID`
  - `FIREBASE_APP_ID`
  - `FIREBASE_DATABASE_URL`

**Never commit your `.env` file or secrets to version control!**

### Generating a Secure Secret Key
Run the following script to generate a secure Django secret key:
```sh
python generate_secret_key.py
```
Copy the output and paste it into your `.env` file as `DJANGO_SECRET_KEY`.

### Running Local Server
Run at the main directory:<br />
``` python manage.py runserver ```<br />

Can be viewed at the url:<br /> 
http://127.0.0.1:8000/api/ <br />
<br />
At the form send a json using the format: <br />
``` {"key": "1.1", "items": 3, "mandates": [1, 1], "preferences": [[1, 1, 1], [1, 1, 1]]} ```

### Running Unit Tests at /api/tests.py
At the main directory run:<br />
``` python manage.py test ```


## Security
- All secrets and sensitive configuration are managed via environment variables.
- CORS and allowed hosts are restricted for security.
- Security headers and rate limiting are enforced.
- Input validation and sanitization are implemented.
- See [SECURITY.md](./SECURITY.md) for full details and deployment checklist.

## Deployment Checklist
- Set all environment variables in your production environment.
- Set `DEBUG=False` and restrict `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`.
- Use HTTPS in production.
- Review [SECURITY.md](./SECURITY.md) for more best practices.

---

**For any security issues, see SECURITY.md or contact the development team immediately.**

















