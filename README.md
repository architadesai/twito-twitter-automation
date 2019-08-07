# Twito (Twitter on Autopilot)

A place to automate your daily Twitter tasks such as Like, Follow & Retweet, in order to improve outreach.

## Installation Instructions

- Follow these commands to be up and running with this project

### Download the source code

```
# Clone this repo
git clone https://github.com/ArchitaDesai/twito
cd twito/twito

# Clone the template repository
git clone --recursive https://github.com/ArchitaDesai/twito-template
```

### Run twito
- Now you've got all the required content for twito.

- Go one directory back and then create & activate the environment and install all the dependencies from `requirements.txt`

```
cd ..

# Create virtual environment using Python3
virtualenv -p python3 env_twito

# Activate the virtual environment
source env_twito/bin/activate

# Install dependencies
pip install -r requirements.txt
```

##### Migrate the changes and then run the server
```
cd twito
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

##### For Celery Tasks
```
python manage.py celery worker --loglevel=info
```

### For the developers
- To commit changes you've made in the twito-template, `cd` into the `twito-template` directory and then commit and push those changes from there to the `twito-template` repository.
- Rest of the changes to twito project can be made, committed & pushed as usual.
- Note: Don't add/commit the changes made in `twito-template` directory in the `twito` repository.
