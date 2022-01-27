import os

def getPythonLayers():
    cmd = 'docker run -v "$PWD":/var/task "lambci/lambda:build-python3.8" /bin/sh -c "pip3 install -r ./requirements/requirements.txt -t pythonLayers/general/python; exit";'
    os.system(cmd)
    cmd = 'docker run -v "$PWD":/var/task "lambci/lambda:build-python3.8" /bin/sh -c "pip3 install -r ./requirements/pandas_requirements.txt -t pythonLayers/pandas/python; exit";'
    os.system(cmd)

def buildPythonImages():
    cmd = f"aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin {os.environ['AWS_ACCOUNT_ID']}.dkr.ecr.us-east-1.amazonaws.com"
    os.system(cmd)
    cmd = 'cd fargate/ && docker-compose pull && docker-compose build && docker-compose push'
    os.system(cmd)

getPythonLayers = {
                 'fn' : getPythonLayers,
                 'help' : 'This will get all python layers so you can deploy this stack from your local machine!'
                }

buildPythonImages = {
                 'fn' : buildPythonImages,
                 'help' : 'This will get all python images so you can deploy this stack from your local machine!'
                }