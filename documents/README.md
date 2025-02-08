# Customer API
Customer agent

# docker build 
sudo docker build -t monkeypatched/document-indexer:latest . --no-cache

# docker run
sudo docker run  --network host -d -p 9013:9013 monkeypatched/document-indexer:latest

# api docs
http://localhost:9013/docs


