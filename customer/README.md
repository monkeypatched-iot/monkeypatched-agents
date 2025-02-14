# Customer API
Customer agent

# docker build 
sudo docker build -t monkeypatched/customer-agent:latest . --no-cache

# docker run
sudo docker run  --network host -d -p 9001:9001 monkeypatched/customer-agent:latest

# api docs
http://localhost:9001/docs


az login

sudo az acr login --name monkeypatched


# tag container
sudo docker tag  monkeypatched/customer-agent:latest  monkeypatched.azurecr.io/agent/customer-agent:latest 

# push contaner
sudo docker push monkeypatched.azurecr.io/agent/customer-agent:latest

