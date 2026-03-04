<a id="readme-top"></a>
<div align="center">
  <h1 align="center">Python websocket chat app</h1>
</div>

## About The Project

<!-- ![Product Name Screen Shot][product-screenshot] -->

This is a terminal-based chat application that uses websocket for client-server communication. The server and client are separate software and can be run on any machine that has python and pip installed.

<details>
  <summary>Table of Contents</summary>
  <ul>
  <li><a href="#client-guide">client guide</a></li>
  <li><a href="#server-guide">Server guide</a></li>
  </ul>
</details>


<a id="client-guide"></a>
## Client guide
### To start using the client:

#### 1. Clone this repository

```sh
git clone https://github.com/Corvus451/python-chat-app.git
```

#### 2. Create a virtual environment in the `python-chat-app/client` directory
```
python -m venv venv
```
#### 2. Activate the virtual environment

Linux:
```sh
source venv/bin/activate
```
Windows:
```ps
venv\Scripts\Activate.ps1
```
#### 3. Run `app.py`
```
python app.py
```

#### 4. To run commands, prefix them with a forward slash `/`. 
```
/connect localhost:8765 myUsername
/disconnect
/quit
```

#### 5. Entering text without forward slash will send it as a chat message if connected to a server.

<p align="right"><a href="#readme-top">back to top</a></p>

<a id="server-guide"></a>
## Server guide

#### 1. Clone this repository

```sh
git clone https://github.com/Corvus451/python-chat-app.git
```

#### 2. Create a virtual environment in the `python-chat-app/server` directory
```
python -m venv venv
```
#### 2. Activate the virtual environment

Linux:
```sh
source venv/bin/activate
```
Windows:
```ps
venv\Scripts\Activate.ps1
```
#### 3. Run `server.py`
```
python server.py
```

#### The server will start listening on port 8765



<p align="right"><a href="#readme-top">back to top</a></p>
