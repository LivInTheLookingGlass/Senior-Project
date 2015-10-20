# Senior Project

##Abstract:
A purely peer to peer distributed computing network which rewards the participants for solving proposed problems. Bounties and IP addresses are exchanged across a websocket network. If the bounty is above a client’s threshold, they will request a java-based test from this IP address. Because a system does not want to reward for faulty results, a test app is sent to the client. If the result is returned correctly, the bountied problem will then be sent.

##Introduction
With the rise of distributed computing projects, from Folding at Home, SETI, etc., there is a distinct lack of standardisation in their distribution methods. Because of this, anyone who wants to tap into this incredible trove of information must design their own platform and market this to the world. Because of this, it’s not surprising that it’s been relatively slow to diversify.

Another problem is that clients have no incentive to run these programs, save for charitable inclinations. Until recently, it would have been next to impossible to provide an incentive. However, with the onset of cryptocurrencies, there is now an easy solution. If people are provided a bounty for problems, they can gain a passive income for their idle resources. This becomes their incentive.

##Bounties
A bounty is a request that fits a standard format. There are three required data fields, and an array to store extra information.

The first field stores the quantity of the bounty in satoshis (the base unit of Bitcoin). The second stores the IP address of the server. The third stores the Bitcoin address of the server. These three pieces of information can be used to filter out invalid requests.

For instance, if a bounty is 100,000,000 satoshis (1 BTC), but their address only contains 10,000, you can safely say that the request is invalid, as they do not have the funds to pay you. Likewise if you cannot connect to their IP address.
The data array can contain various flags. For instance, if the program is designed to run on multiple threads, it could contain the ideal core count. Or if the server is run by a well known entity, it could contain something like “SETI thanks you”.

![](http://i.imgur.com/pNUXvZs.png)

Each node decides to propagate a bounty to the network by using the following workflow:

![](http://i.imgur.com/7ceMiiv.png)

##Security
Because a client is allowing other people to run unknown code on their computer, there needs to be a way to keep things secure. This is possible by the use of a sandbox, making Java an ideal language for tests. While this is less efficient than other languages, it builds a security solution into the network and client itself.

##Tests
Tests are a vital part of the network. Like there are ways for clients to exclude invalid requests, there must also be a way for servers to exclude inappropriate clients. They can do this with small bits of test code. The client will then send them the result of this code, and if it is correct, will receive the real problem.

This opens an avenue of attack for the network, however, so there must be constraints on these tests. These will be defined at a later time.

##Queries
After all of this, the query is finally sent to the client. Simultaneously, a payment channel is opened. This channel will be updated once per minute as long as there is an active connection between the server and client, and will grow at a linear rate until a result is achieved, but will never reach the full bounty until a result is submitted. This is to protect from fraud on both the server and user end. The server is protected in that the client has an incentive to stay online, and the user is protected in that the connection will expire if a predetermined time goes by without a result.

Upon closing the connection, the reward is distributed between the two parties in the way agreed upon in the last transaction broadcast. If a result is given, the full bounty will be delivered. The transactions are always broadcast with a lock-time of 24 hours.

![](http://i.imgur.com/ohQYnrD.png)

##Servers
The server side of this has two additional components: a propagator and a parser. The propagator handles requests from various clients. It is comprised of a wallet, a socket, and (at least) two files. The wallet is used to pay clients, and essentially signs transactions all day. It largely runs in a separate thread. The socket decides which file to send to clients, and then sends them. When the socket receives a file, it passes it on to the parser.

The parser has two purposes: analyze test results, and move problem results to the proper area. Because of this, test results take the priority. This piece must be custom written by the server maintainers, because it needs to verify that the test was completed correctly. Because each test is tailored to the problem at hand, there is no general purpose solution for it. When it is not doing this, the parser writes solution files to a specified folder, where it can be analyzed without slowing down server functions.
