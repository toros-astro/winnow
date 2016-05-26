# TOROS Winnower web page

This django web app is designed to "winnow the wheat from the chaff" in the Image Difference analysis of astronomical images. 

Image Differencing will leave behind many fake objects due to bad subtraction that will be classified as bogus by a Machine Learning algorithm. This ML algorithm has to be 'trained' with labeled data and this website provides a web interface to generate this training set via human input classification.

---

# Download, Install and Setup
Follow the following steps to download, install, and run this Django project.

### Clone the repository
```
git clone git@github.com:toros-astro/winnower.git
```

### Navigate to the main directory. Then type:
```
python manager.py migrate
```
in order to set up the sqlite database.

#### Start the Django server
```
python manager.py runserver
```

### Use your webbrowser to visit
```
http://127.0.0.1:8000/
```

---

# LIVE Site
A live version of this site can be accessed by visiting: http://toros-dev.no-ip.org


---

The site will look similar to the following screenshot:
![LIVE site screenshot](http://i.imgur.com/sVWE8eD.png)

---

Copyright Martin Beroiz, 2015

email: <martinberoiz@gmail.com>
