# Product API
Product agent

# docker build 
sudo docker build -t monkeypatched/order-agent:latest . --no-cache

# docker run
sudo docker run  --network host -d -p 9003:9003 monkeypatched/order-agent:latest

# api docs
http://localhost:9003/docs