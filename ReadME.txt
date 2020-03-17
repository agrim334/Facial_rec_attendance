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
        flask-wtf
        flask-sqlalchemy
        flask-migrate
        flask-mail
        flask-login
        flask-bootstrap
        flask-uploads
        flask-mysql
        flask-mysqldb
        click
        face_recognition
        numpy
        Pillow
        scipy
        dlib
  ### **Steps**
      1.) If you don't have an NVIDIA GPU or have one but it does not support CUDA , skip this step.(To check CUDA support visit
          https://developer.nvidia.com/cuda-gpus). Else install NVIDIA CUDA (https://developer.nvidia.com/cuda-downloads) and NVIDIA 
          CuDNNN (https://developer.nvidia.com/cudnn) using their official documentation. CuDNNN requires you to register an NVIDIA
          Developers Account(Free) before you can download the library.
          
      2.) Install face recognition library and dlib as given here : https://github.com/ageitgey/face_recognition#installation
      
      3.) Install mysql (either using official docs https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/ or some other source
          you find convenient multiple guides are available) and setup privilges accordingly.
      
      4.) Use pip3 install -r requirements.txt to install remaining requirements.
			
			5.) After installation make following changes:
					5a.)
      