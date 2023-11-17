# codecrafters-http-server-python
Build your own HTTP server


### [Stage 1]

To try this locally on macOS,

you could run ```./your_server.sh``` in one terminal session, 
and ```nc -vz 127.0.0.1 4221``` in another. 
- ```-v``` gives more verbose output
- ```-z``` just scan for listening daemons, without sending any data to them.


### [Stage 4]

To test locally using cURL: 

```curl --verbose 127.0.0.1:4221/echo/abc```

### [Stage 5]

An easy way to test this locally would be to use nc to create a connection to your server and then use curl to hit it with a request. 
i.e. ```nc localhost 4221``` in one window followed by ```curl localhost:4221``` is a separate terminal window.



### [Stage 8] 
To test locally using cURL:

```curl -vvv -d "good job! =D" localhost:4221/files/readme.txt```
