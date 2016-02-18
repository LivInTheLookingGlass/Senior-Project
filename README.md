[![](https://img.shields.io/travis/gappleto97/Senior-Project/master.svg?style=plastic&label=Linux%20Build)](https://travis-ci.org/gappleto97/Senior-Project) [![](https://img.shields.io/appveyor/ci/gappleto97/Senior-Project/master.svg?style=plastic&label=Windows%20Build)](https://ci.appveyor.com/project/gappleto97/senior-project) [![](https://img.shields.io/codecov/c/github/gappleto97/Senior-Project.svg?style=plastic&label=Coverage)](https://codecov.io/github/gappleto97/Senior-Project) [![](https://img.shields.io/codeclimate/github/gappleto97/Senior-Project.svg?style=plastic&label=Style%20Grade)](https://codeclimate.com/github/gappleto97/Senior-Project/) [![Stories in Ready](https://badge.waffle.io/gappleto97/Senior-Project.png?label=in%20progress&title=In%20Progress)](https://waffle.io/gappleto97/Senior-Project)

You'll probably find the [web format](https://gappleto97.github.io/Senior-Project) a bit nicer to read. It's also kept more up to date.

If you're looking to contribute, [go here](https://github.com/gappleto97/Senior-Project/blob/master/documentation/Contributing.md)

#Issues
If you do not have a GitHub account, please submit your issue with [this link](https://gitreports.com/issue/gappleto97/Senior-Project). Otherwise, use the [standard issue tracker](https://github.com/gappleto97/Senior-Project/issues/new). 

# Senior Project

##Abstract
A generalized, peer-to-peer platform for programs like Folding at Home, which rewards users with micropayments for solving NP-complete problems.

##Introduction
With the rise of distributed computing projects, from [Folding at Home](https://folding.stanford.edu/), [SETI](https://setiathome.ssl.berkeley.edu/), etc., there is a distinct lack of standardization in their distribution methods. Because of this, anyone who wants to tap into this trove of information must design their own platform and market this to the world. It’s not surprising that it’s been slow to diversify.

Another problem is that clients have no incentive to run these programs, save for charitable inclinations. Until recently, it would have been next to impossible to provide an incentive. However, with the onset of cryptocurrencies, there is now an easy solution. If people are provided a bounty for problems, they can gain a passive income for their idle resources. This becomes their incentive.<sup>[1](#myfootnote1)</sup>

##Design Goals
There are four attacks that I currently anticipate on this platform. Each of them must be addressed in its design, and throughout this proposal I will point out when they are.

1. Mallicious user
	* This is a Denial of Service attack on the servers. By spoofing an active user (not solving the problems it is sent), an attacker could waste the money and processing time of the server.
2. Mallicious server
	* This is a Denial of Service attack on the user and charity servers (one which does not pay). By spoofing a charity server, an attacker could send useless programs, which, for instance, add random sums forever. Such an attack would go against the wishes of the user (not contributing towards general research), and force real charity servers to provide payment which they may not be able to afford.
3. Dishonest server
	* This is a Denial of Service attack on the user and platform. By broadcasting a bounty with a substantial reward, an attacker could trick nodes into wasting their computational time. This would drive up the general price of the platform, and possibly force it to a halt.
4. Outside actors
	* It is very possible that an outside bad actor could misuse the platform. One such misuse could be hiring out a botnet.

##Bounties
A bounty is a request that fits a standard format. There are three required data fields, and an array to store extra information.

The first field stores the quantity of the bounty in satoshis (the base unit of Bitcoin). The second stores the IP address of the server. The third stores the Bitcoin address of the server. These three pieces of information can be used to filter out invalid requests.

For instance, if a bounty is 100,000,000 satoshis (1 BTC),<sup>[2](#myfootnote2)</sup> but their address only contains 10,000, you can safely say that the request is invalid, as they do not have the funds to pay you. Likewise if you cannot connect to their IP address.

The data array can contain various flags. For instance, if the program is designed to run on multiple threads, it could contain the ideal core count. Or if the server is run by a well known entity, it could contain something like “SETI thanks you”.

![](https://i.imgur.com/xCsjOto.png)

Each node decides to propagate a bounty to the network by using the following workflow:

![](https://i.imgur.com/bkmwNsB.png)

##Security
Because a client is allowing other people to run unknown code on their computer, there needs to be a way to keep things secure. This is possible by the use of a sandbox, making Java an ideal language for tests. While this is less efficient than other languages, it builds a security solution into the network and client itself.

There will also be cases where one will not want to run it in a sandbox. Support for this type of operation is critical for companies like Intel, AMD, NVidia, and Samsung, which may want to test edge cases of their products in the wild. If everything is sandboxed, there’s no way for them to easily guarantee that they are getting to the correct devices. These use cases will be investigated, as they could make up most of the demand for this network.


##Tests
Tests are a vital part of the network. Like there are ways for clients to exclude invalid requests, there must also be a way for servers to exclude inappropriate clients. They can do this with small bits of test code. The client will then send them the result of this code, and if it is correct, will receive the real problem.

This opens an avenue of attack for the network, however, so there must be constraints on these tests. These will be defined at a later time.<sup>[3](#myfootnote3)</sup>

##Queries
After all of this, the query is finally sent to the client. Simultaneously, a [payment channel](https://bitcoin.org/en/developer-guide#micropayment-channel)<sup>[4](#myfootnote4)</sup> is opened. This channel will be updated once per minute as long as there is an active connection between the server and client, and will grow at a linear rate until a result is achieved, but will never reach the full bounty until a result is submitted. This is to protect from fraud on both the server and user end. The server is protected in that the client has an incentive to stay online, and the user is protected in that the connection will expire if a predetermined time goes by without a result.

Upon closing the connection, the reward is distributed between the two parties in the way agreed upon in the last transaction broadcast. If a result is given, the full bounty will be delivered. The transactions are always broadcast with a lock-time of 24 hours.
![](https://i.imgur.com/I25QiL0.png)

##Servers
The server side of this has two additional components: a propagator and a parser. The propagator handles requests from various clients. It is comprised of a wallet,<sup>[5](#myfootnote5)</sup> a socket,<sup>[6](#myfootnote6)</sup> and (at least) two files. The wallet is used to pay clients in the manner described above. By necessity it spawns large numbers of threads—one per client connected. The socket decides which file to send to clients, and then sends them. When the socket receives a file, it passes it on to the parser.

The parser has two purposes: analyze test results, and move problem results to the proper area. Because of this, test results take the priority. This piece must be written by the server maintainers; there is no general solution for it. When it is not doing this, the parser moves solution files to a different folder, where it can be analyzed without slowing down the rest of the server.

#Progress

##So Far

* Basic networking capabilities
  * Send messages
  * Listen and respond (concurrently)
  * On a custom port, if desired
* Transparent settings storage
* UPnP forwarding (Linux, OSX)
 
##Working on it

* Dedicated server mode
* More complete settings controls
* UPnP forwarding (Windows)

##Future

* Coin control
  * Payment channel
  * Secure wallet generation
  * Secure wallet storage
* More complete bounty definition
* Network discovery
* Sandboxed Execution

----------------------------

<a name="myfootnote1">1</a>: Users will have the option of running this for free. The bounty is to encourage participation, and is not strictly necessary.

<a name="myfootnote2">2</a>: The program would store in values in satoshis to avoid floating point inaccuracies.

<a name="myfootnote3">3</a>: Fork bombing and other such annoyances are a major concern with the test network. Because of this, any solution that necessitates trust must be rejected. Code analysis for any obvious concerns will be necessary, but may not be enough.

<a name="myfootnote4">4</a>: This opens up a security risk to the user because their private key is exposed to my program. This is the single biggest reason that this must be an open source project. Encryption will be explored.

<a name="myfootnote5">5</a>: Part of the common library.

<a name="myfootnote6">6</a>: Overrides of the standard peer management system.
