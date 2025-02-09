# import socket module
from socket import *
# In order to terminate the program
import sys



def webServer(port=13331):
  serverSocket = socket(AF_INET, SOCK_STREAM)
  
  #Bind port to socket and start listening for requests
  serverSocket.bind(("", port))
  serverSocket.listen()
  

  while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    
    try:
      print(f"Connected IP: {addr}")
      message = connectionSocket.recv(1024)
      filename = message.split()[1]
      print(filename)
      
      #opens the client requested file. 
      #Plenty of guidance online on how to open and read a file in python. How should you read it though if you plan on sending it through a socket?
      f = open(filename[1:], "rb")
      

      #Store the headers you want to send for any valid or invalid request.   
     
      #Content-Type is an example on how to send a header as bytes. There are more!
      outputdata = b"HTTP/1.1 200 OK; Content-Type: text/html; charset=UTF-8\r\n\r\n"
      #Note that a complete header must end with a blank line, creating the four-byte sequence "\r\n\r\n" Refer to https://w3.cs.jmu.edu/kirkpams/OpenCSF/Books/csf/html/TCPSockets.html
    
      for i in f: 
        outputdata += i
        
      print(outputdata)
      #Send the content of the requested file to the client (don't forget the headers you created)!
      #Send everything as one send command, do not send one line/item at a time!
      f.close()

      connectionSocket.sendall(outputdata)
        
      connectionSocket.close() #closing the connection socket
      
    except Exception as e:
      outputdata = b"HTTP/1.1 404 NOT FOUND; Content-Type: text/html; charset=UTF-8\r\n\r\n"
      connectionSocket.send(outputdata)
      connectionSocket.close() #closing the connection socket


  # Commenting out the below (some use it for local testing). It is not required for Gradescope, and some students have moved it erroneously in the While loop. 
  # DO NOT PLACE ANYWHERE ELSE AND DO NOT UNCOMMENT WHEN SUBMITTING, YOU ARE GONNA HAVE A BAD TIME
  #serverSocket.close()
  #sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
  webServer(13331)