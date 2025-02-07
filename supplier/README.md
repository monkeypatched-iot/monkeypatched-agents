# Product API
Product agent

# docker build 
sudo docker build -t monkeypatched/supplier-agent:latest . --no-cache

# docker run
sudo docker run  --network host -d -p 9005:9005 monkeypatched/supplier-agent:latest

# api docs
http://localhost:9002/docs