
About:
-----------
This is a web server written in the Python programming language.  
The web server uses its own thread pool for thread organization and management.  
It also uses the socket library in its own class to manage network connections of http clients  
I am making the web server freely available for download and for further possible modifications and extensions.  


Starting webserver:
-------------------
This program requires python interpreter. Required python version >= 3.8.  
It has 4 variables in main.py file  
- server_host = "0.0.0.0"             &emsp;&emsp;&emsp;# listening ip address
- server_port = 8443                  &emsp;&emsp;&emsp;# listening port
- private_key = "./private.key"       &emsp;&emsp;&emsp;# path to private.key
- server_cert = "./server.crt"        &emsp;&emsp;&emsp;# path to tls certificate

After settings this simply run:  
python ./main.py  


Needed python modules:
----------------------
- socket
- threading
- ssl
- time
- re
- select