# Customer API
Customer agent

# docker build 
sudo docker build -t monkeypatched/customer-agent:latest . --no-cache

# docker run
sudo docker run  --network host -d -p 9001:9001 monkeypatched/customer-agent:latest

# api docs
http://localhost:9001/docs


