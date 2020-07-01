**Credits to Adam Geitgey for the facial recognition library at https://github.com/ageitgey/face_recognition.**
## Basic

This is website is an attendance system which utilizes facial recognition to detect students in a class and mark attendance.
The website has been made using Flask framework , HTML + Bootstrap for front end and MYSQL for the backend along with the facial
recognition API.If your system has an NVIDIA GPU with CUDA support, you may install CUDA for better performance.By default, the website
DOES NOT use CUDA.

**NOTE : As of now the system has been developed for linux systems. Therefore certain steps for installation may not
work. Will update for other OS as well.**

## **Installation**
  ### **Requirements**

        Ubuntu >= 16.04
        python3 (atleast 3.4)
        CUDA >= 7.5.0
        CuDNNN >= 5.0.0
        mysql >=5.7.0 (both client and server)
        mysqldb >=5.7.0
        opencv-python
        flask
        flask-sqlalchemy
        flask-migrate
        flask-mail
        flask-uploads
        flask-mysql
        flask-mysqldb
        click
        face_recognition
        numpy
        Pillow
        scipy
        dlib
        cmake
        npm (Node package manager)
        vuejs 3.0
        axios
        vuex
        vue-cli
        cmake
        CUDA Capable Nvidia GPU (Optional)

  ### **Steps** 
      1.) If you don't have an NVIDIA GPU or have one but it does not support CUDA , skip this step.(To check CUDA support visit
          https://developer.nvidia.com/cuda-gpus). Else install NVIDIA CUDA (https://developer.nvidia.com/cuda-downloads) and NVIDIA 
          CuDNNN (https://developer.nvidia.com/cudnn) using their official documentation. CuDNNN requires you to register an NVIDIA
          Developers Account(Free) before you can download the library.
          
      2.) Install face recognition library and dlib as given here : https://github.com/ageitgey/face_recognition#installation
      
      3.) Install mysql (either using official docs https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/ or some other source
          you find convenient multiple guides are available) and setup privilges accordingly.
      
      4.) Use pip3 install -r requirements.txt to install remaining requirements.
      
      5.) Clone this repo to your system.
      
      6.) After cloning make following changes:
          6a.) In config.py Set ADMINS = list of email addresses of admins
          6b.) Update env.sh to suit your environment settings as follows : 
                  DATABASE_URL user --> your username 
                              pwd  --> your mysql password
                              db   --> the database name where data will be stored
                  FLASK_APP  microblog.py --> whatever new name you choose for your app.
                  MAIL_USERNAME  emailid --> the admin's email id
                  MAIL_PASSWORD  pwd --> admin's email password
                  VUE_FRONT_URL --> url of the frontend(vuejs) route + /resetpwd/ (crucial needed for email sending)
                  FLASK_HOST --> ip address of server where flask will run (e.g 192.168.42.56). default value is localhost
                  FLASK_PORT --> port number at which flask will run (e.g 2000). default value is 5000
            
                  VUE_HOST --> ip address of server where vuejs will run (e.g 192.168.42.56) default value is localhost
                  VUE_PORT --> port number at which vuejs will run  (e.g. 7000) default value is 8080
                   
                  VUE_FRONT_URL and FLASK_URL must NOT be the same. At least differ the ports.

                  ADMINS --> the admins email id
                The remaining environment variables are to be set up according to your email server
                
          6c.) In routes.py update **known_dir** in **detect_faces_in_image** function to the directory 
               where images of known persons are kept.   
      7.) Create a table department in your database as per the fields given in models.py
      8.) In the cloned directory run
                     . env.sh
                     flask db init
                     flask db migrate
                     flask db upgrade
      9.) In the same directory run:
                    flask shell
                    from app.models import *
                    Role.insert_roles()
          and then exit
      10.) Insert database records (for first time setup) using mysql or flask shell 
          (refer https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database or mysql docs for relevant commands)
      11.) Make sure npm is installed on your system
      12.) navigate to app/frontend/ (in terminal session) in the directory and run 
                    npm install
          to install requisite vue packages
 
 # **Usage**
      1.) Open a terminal session in the cloned repo directory.
      2.) Ensure MySQL is running and requisite credentials have been added in env.sh
      2.) Run the following ([] means optional):
                  . env.sh
                  flask run [--with-threads] --host=$FLASK_HOST --port=$FLASK_PORT
          By default the server runs on localhost:5000/
      3.) In another terminal session (opened at app/frontend/) run
                  npm run serve (for development)
      4.) If you wish to use CUDA for better performance, then set the value of model argument in attd_sys/routes.py as "cnn" everywhere. if not set it "hog"
      
