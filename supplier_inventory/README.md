# Customer API
Supplier Inventory agent

# docker build 
sudo docker build -t monkeypatched/supplier-agent:latest . --no-cache

# docker run
sudo docker run  --network host -d -p 9004:9004 monkeypatched/supplier-agent:latest

# api docs
http://localhost:9009/docs



az login

sudo az acr login --name monkeypatched

# tag container
sudo docker tag  monkeypatched/component-agent:latest  monkeypatched.azurecr.io/agent/component-agent:latest 

# push contaner
sudo docker push monkeypatched.azurecr.io/agent/component-agent:latest
