# bot-builder
Bot builder is a Python Django server which handles user response cycle
=======
Handling multiple facebook chat-apps with a single server
===
It is fairly easy to start with facebook chatbots, the complexity rises as progress is made towards getting the apps reviewed. This is also a point of concern when it comes to choosing a default platform, while facebook chatbots solve the problem of discovery along with the assurance that a general user would probably have facebook installed, very little can be said about the scalability. How quickly can we launch 10 apps? How about 100? with simplified chat-flow and logic we can deploy such apps using scripts by the minute, the limitations being:

1. The review process, which is a painstaking 7-day long process.  
2. The generation of page-access-tokens and other such assets of private nature

Very little can be done about the review process. Going forward with handling the private assets, it is imperative that there is a need to integrate some form of source to contain business-specific data. 

#### Mapping assets to data tables
1. An Authorization table to contain `page_access_token`, `api_key`, etc along an id which is referenced by the table containing menu items.
2. Using the `request.META` we can access the headers sent over by facebook when sending messages to the chat-app-server(botbuilder).
3. A middleware in place can verify if the `page_access_token` is present in the request also if it is registered for use. During this process we can retrieve the relevant table which contains the menu data and pop it in the session for later use.
4. Putting a cache in place to store these can speed-up the query times for auth and retrieval of data table id.
=======
