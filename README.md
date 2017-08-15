# twito
Follow these commands to be up and running with this project

## Download the source code
```
git clone https://github.com/YJDave/twito
cd twito/twito
git clone --recursive https://github.com/ArchitaDesai/twito-template
```

## Run twito
Now you've got all the required content for twito
Go one directory back and then activate the environment
```
cd ..
source env_twito/bin/activate
```
Migrate the changes and then run the server
```
cd twito
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### For the developers
To commit changes you've made in the twito-template, go into twito-template directory and then commit and push those changes from there.
Rest of the changes to twito project can be made as usual.
