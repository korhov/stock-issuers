# stock-issuers
Биржевые эмитенты (Service of exchange issuers)

docker build -t stock-issuers .
docker build -f parser.Dockerfile -t stock-issuers-parser .
docker build -f api.Dockerfile -t stock-issuers-api .

docker run --rm -v $(pwd):/home/stock-issuers -p 8000:80 -it stock-issuers

docker run --rm -v $(pwd):/home/stock-issuers -p 8000:80 -it stock-issuers-api
docker run --rm -v $(pwd):/home/stock-issuers -it stock-issuers-parser