# Creating a  Web Application for Extracting Text from Image.

In this Project we aim to develop a web application that receives user data (image for now) and outputs the text embodied in it. We use `flask` as the web application framework. Also, `Microsoft Azure Optical Character Recognition (OCR)` is the model/API that we employ for the text extraction.


If you are running this app on a remote server but wish to test it on your local system/browser, you need SSH tunneling. The general structure is as follows

 ```
ssh -L [local_port]:[remote_host]:[remote_port] [user]@[remote_host]
 ```

`-L` specifies local port forwarding. `local_port` is the port on your machine that you want to bind to. `remote_host` is the remote server that you want to connect to and run the API. `remote_port` is the port on the remote machine that you want to forward the connection to. For instance, you could do

```
ssh -L 8080:localhost:3000 user@remote.server.com
```
On your local machine you can use the following URL to access the APP: `http://localhost:8080/`

To connect to the Azure API, make sure `AZURE_ENDPOINT` and `AZURE_API_KEY` are either defined in an environment file or set as environment variables. The first approach is what we followed in the code, whereas for the second choice you need to do the following
```
in bash:
export AZURE_ENDPOINT="your_endpoint"
export AZURE_API_KEY="your_api_key"

in analyze.py:
endpoint=os.getenv("AZURE_ENDPOINT")
key=os.getenv("AZURE_API_KEY")
```
When calling app.run, ensure that the specified port matches the remote_port defined in the SSH forwarding configuration. Setting `debug=True` enables automatic code reloading when changes are made to the source code, which facilitates interactive testing and streamlines the development process.


