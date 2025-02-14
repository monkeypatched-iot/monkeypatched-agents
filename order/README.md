# Order API
Order agent

# docker build 
sudo docker build -t monkeypatched/order-agent:latest . --no-cache

# docker run
sudo docker run  --network host -d -p 9003:9003 monkeypatched/order-agent:latest

# api docs
http://localhost:9003/docs



az login

sudo az acr login --name monkeypatched

# tag container
sudo docker tag  monkeypatched/order-agent:latest  monkeypatched.azurecr.io/agent/order-agent:latest 

# push contaner
sudo docker push monkeypatched.azurecr.io/agent/order-agent:latest