# Quiz Application

This is an online quiz application website project, developed using Python's web framework Django.<br>
For front-end designing I have used Bootstrap4 and adminlte.

## Getting started with development

Dependencies:

- Python 3.8.x
- Django 4.1.3
- Ubuntu 20.04 or later

### 1. Clone this repository

```bash
git clone https://github.com/NikitaPatel29/quiz-application.git
cd quiz-application
```

### 2. Install [Pipenv](https://pipenv.pypa.io/en/latest/)

### 3. Create and activate the virtualenv

```bash
## run following command from current working directory
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
virtualenv myprojectenv
source myprojectenv/bin/activate
```

### 4. Install python packages

```bash
pip install -r requirements.txt
```

### 5. Setup the database

Django provides sqllite as the default database, so you don't need to make any changes. <br/><br/>
_Note : We used default database for this project if you want change the database then you can change the database configuration in setting.py file._

### 6. Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create superuser

```bash
python manage.py createsuperuser
```

### 8. Run collectstatic

```bash
python manage.py collectstatic
```

### 9. Run development server

```bash
python manage.py runserver
```

## Current Features

### Site access features:

- User must be logged in to access the Quiz.
- For signup user is required to give _username_, _first name_, _last name_, _e-mail address_ and _password_.
- For login the user will be required to enter _username_ and _password_ only.
- After registeration user receive a welcome email.
- The user can track the history of past quiz attempts.

### Features of the quiz:

- All questions are multiple choice question.
- Each question is displayed only once per user.
- Questions are displayed randomly for every user.
- If the user by-mistake presses refresh or go back to the previous page, there will be a new question for the user and the question he/she was on will be marked as attempted.
- Once a quiz attempt has been made, the user cannot attempt it again before 24 hours.

### Administrative features:

- Only admin can add questions.
- Admin can add questions category.
- Admin can add questions and modify them.
- Admin can not delete the question once added.
- Admin can see a list of questions.
- Admin can search questions by question text or choice text.

## Contributors

- [Nikita Patel](https://github.com/NikitaPatel29)