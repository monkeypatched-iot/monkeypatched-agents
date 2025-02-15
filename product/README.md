# Product API
Product agent

# docker build 
sudo docker build -t monkeypatched/product-agent:latest . --no-cache

# docker run
sudo docker run  --network host -d -p 9002:9002 monkeypatched/product-agent:latest

# api docs
http://localhost:9002/docs

az login

sudo az acr login --name monkeypatched

# tag container
sudo docker tag  monkeypatched/product-agent:latest  monkeypatched.azurecr.io/agent/product-agent:latest 

# push contaner
sudo docker push monkeypatched.azurecr.io/agent/product-agent:latest