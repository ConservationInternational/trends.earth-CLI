# trends.earth CLI

This project belongs to the trends.earth Project.

This repo implements the CLI of the trends.earth Environment. It allows to create and test custom scripts locally. It also can be used to publish the scripts to the trends.earth Environment

Check out the other parts of the trends.earth project:

- The API [trends.earth API](https://github.com/Vizzuality/trends.earth-API)
- The trends.earth core platform [trends.earth Environment](https://github.com/Vizzuality/trends.earth-Environment)
- A web app to explore and manage the API entities [trends.earth UI](https://github.com/Vizzuality/trends.earth-UI)

## Getting started

### Requirements

- Python 3 [Download Python](https://www.python.org/)
- pip (pip3). You can check the version you have installed doing ```pip -V```

### Installation from pypi

```
$ pip install trends-earth-cli
```

### Usage

```
$ trends
```

### Installation from repository

Make sure you have virtualenv already installed on your machine

- virtualenv. ```$ pip install virtualenv```


- Clone the repo and go to the folder

```
$ git clone https://github.com/Vizzuality/trends.earth-CLI
$ cd trends.earth-CLI
```

- Create a virtual environment if you haven't already

```
$ virtualenv -p python3 venv
```

Note that if you are using Windows, and your default python is python 2.7, then
you will need to specify the path to Python 3 using `--python`. For example:

```
$ virtualenv --python "C:\Users\azvol\Anaconda3\python.exe" venv
```

- Activate it (you should do this step any time you want to run the project locally)

```
$ source venv/bin/activate
```

or (on a Windows box using a Docker Quickstart terminal):

```
$ source venv/Scripts/activate
```

- Install the dependencies

```
$ pip install -r requirements.txt
```

Now you can use the CLI commands

## Commands

### Create

To create a new script.
The program will ask you for a name of your script.

```
$ python tecli create
```

### Start

To run a script locally.
First, go to the folder where the script has been created and run the following:

```
$ python (relativepath) start
```

For instance:

```
$ python ../../tecli start
$ python ../tecli start
```

### Config

To configure basic params like a GEE Account.

For EE_PRIVATE_KEY param it's neccesary set the value in base64 encode. To encode use the next command:

```
$ cat privatekey.pem | base64
```

```
$ python tecli config set EE_SERVICE_ACCOUNT <value>
$ python tecli config set EE_PRIVATE_KEY <base64value>
```

It is also possible to see the current config

```
$ python tecli config show EE_SERVICE_ACCOUNT
$ python tecli config show EE_PRIVATE_KEY
```

And even unset one or both of them

```
$ python tecli config unset EE_SERVICE_ACCOUNT
$ python tecli config unset EE_PRIVATE_KEY
```

### Login

To log in the API. This step is necessary when publishing scripts

```
$ python tecli login
```

### Publish

This command allows the user to publish the script to prod. As it was said, it's required to be logged before
publish a script. Set the parameter public to True if the script is publicly visible.

```
$ python tecli publish
$ python tecli publish --public=True
```

### Logs

To see the build logs printed by the script.

```
$ python tecli logs
```

### Info

To see some basic info about the script

```
$ python tecli info
```

### Clear

Delete temporary docker images

```
$ python tecli clear
```

### Download

Download the script code

```
$ python tecli download <script_id>
```

## Examples

### Tensorflow

It defines, trains and evaluates a simple perceptron model to identify handwritten digits from the MNIST dataset.

You can test the behavior doing the following:

```
$ python ../../tecli start
```

### Numpy

This script just concatenates two numpy arrays. It also shows how to define a custom Python class.

### Google Earth Engine

It calculates the umd forest loss or gain based on a given area and a period of time.
