# djangoblockchain
Current project for implementing blockchain through django


Based of my orginal blockchain project, I decided to implement it through Django/React. The frontend was based off of someone else's blockchain project. 
While my backend is based off of my original blockchain code. 

Eventually I want to implement letting the user have their own wallet and using a PostGres database for users to store their blockchain

In order to use my Django BlockChain app do the following:

1. Clone the Repository 
2. Then in the same folder as the Repo hit:
  - npm install create-react-app
  - start-react-app frontend  (may need to delete the frontend folder for this) 
  - cd frontend 
  - npm start
  - npm install axios react-bootstrap bootstrap font-awesome --save
  - add "proxy": "http://127.0.0.1:8000" in package.json (in frontend folder) under the key "name": "frontend"
  - add <link rel=”stylesheet” href=”https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity=”sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T” crossorigin=”anonymous”/>
    to index.html 
  - copy all files from blockchain_django/chain_simulator/js_contents and copy them to frontend/src/components (overwriting is ok)
  - run python manage.py runserver in one terminal and run npm start in another terminal 
  - http://localhost:3000 to view it in frontend 
  - http://127.0.0.1:8000/ to make api calls via backend 
  

