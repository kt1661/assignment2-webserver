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
    #print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
      #print(f"Connected IP: {addr}")
      message = connectionSocket.recv(1024)
      filename = message.split()[1]
      #print(filename)
      
      #opens the client requested file, reads and closes
      with open(filename[1:], "rb") as f:
        responsebody = f.read()
      
      headers = ("HTTP/1.1 200 OK\r\n" 
                  "Server: kt1661-localhost\r\n" 
                  "Connection: keep-alive\r\n"
                  "Content-Type: text/html; charset=UTF-8\r\n"
                  "Content-Length: {}\r\n\r\n".format(len(responsebody)))
      
      #Note that a complete header must end with a blank line, creating the four-byte sequence "\r\n\r\n" Refer to https://w3.cs.jmu.edu/kirkpams/OpenCSF/Books/csf/html/TCPSockets.html
    
      response = headers.encode() + responsebody
        
      #print(outputdata)
      #Send the content of the requested file to the client with headers
      f.close()

      connectionSocket.sendall(response)
        
      connectionSocket.close() #closing the connection socket
      
    except Exception as e:
      with open("notfound.html", "rb") as f:
        responsebody = f.read()
      
      headers = ("HTTP/1.1 400 Not Found OK\r\n" 
                  "Server: kt1661-localhost\r\n" 
                  "Connection: keep-alive\r\n"
                  "Content-Type: text/html; charset=UTF-8\r\n"
                  "Content-Length: {}\r\n\r\n".format(len(responsebody)))
      
      response = headers.encode() + responsebody
      connectionSocket.send(response)
      connectionSocket.close() #closing the connection socket


  # Commenting out the below (some use it for local testing). It is not required for Gradescope, and some students have moved it erroneously in the While loop. 
  # DO NOT PLACE ANYWHERE ELSE AND DO NOT UNCOMMENT WHEN SUBMITTING, YOU ARE GONNA HAVE A BAD TIME
  #serverSocket.close()
  #sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
  webServer(13331)