## Get Started

It is quick and easy to get the application up and running


  * Create a .env file in the Banbury Cloud directory. You should add the following arguments
    *  RELAY_HOST - This is the ip address for the relay server you will be using. Can be 0.0.0.0
    *  RELAY_PORT - I would use 8002
    *  MONGODB_URL - This is the url to your mongodb database. You shouldn't need this hopefully.    
  * Run the front end
    *  [Get started with the frontend]("https://github.com/Banbury-inc/Athena/tree/main/Banbury_Cloud/frontend/README.md") 
  * Run the backend
    *  Nothing to do here, API calls are coming from public url. Ill work on getting this open source 
  * Run the relay server
    *  This is as easy as simply running [relayserver.py]("https://github.com/Banbury-inc/Athena/blob/main/Banbury_Cloud/backend/relayserver.py")  
