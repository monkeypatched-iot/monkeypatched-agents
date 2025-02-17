# Customer API
Builder agent

# docker build 
sudo docker build -t monkeypatched/builder-agent:latest . --no-cache

# docker run
sudo docker run  --network host -d -p 9006:9006 monkeypatched/builder-agent:latest

# api docs
http://localhost:9006/docs


az login

sudo az acr login --name monkeypatched

# tag container
sudo docker tag  monkeypatched/builder-agent:latest  monkeypatched.azurecr.io/agent/builder-agent:latest 

# push contaner
sudo docker push monkeypatched.azurecr.io/agent/builder-agent:latest