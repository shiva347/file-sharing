
## Project Setup 
Clone the repository
```
git clone https://github.com/shiva347/file-sharing.git
```

Create and activate a virtual environment
```
python -m venv myenv
```
For Windows 
```
myenv\Scripts\activate
```
For Linux or Mac
```
source myenv/bin/activate
```
Navigate backend project directory
```
cd filesharing
```
Install the required packages
```
pip install -r requirements.txt
```

```
python manage.py makemigrations
```

```
python manage.py migrate
```
Create Superuser(Ops User) - in our case this is a Ops User
```
python manage.py createsuperuser
```
Run Server
```
python mange.py runserver
```
