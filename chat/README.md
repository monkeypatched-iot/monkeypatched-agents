# Order API
Query  agent

# docker build 
sudo docker build -t monkeypatched/chat-agent:latest . --no-cache

# docker run
sudo docker run  --network host -d -p 9017:9017 monkeypatched/chat-agent:latest

# api docs
http://localhost:9003/docs

az login

sudo az acr login --name monkeypatched

# tag container
sudo docker tag  monkeypatched/chat-agent:latest  monkeypatched.azurecr.io/agent/chat-agent:latest 

# push contaner
sudo docker push monkeypatched.azurecr.io/agent/chat-agent:latest