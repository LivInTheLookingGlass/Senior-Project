#Common

This is a common library. It has files that are shared between both the server and client mode. There are, however, certain methods that are overridden in each case. Most of these have to do with bounty and peer propogation.

###Bounty

This contains the definition for the `Bounty` class, as well as several utility methods for dealing with them.

###Call

A library to call arbitrary python code. This is used by `Bounty` to parse system requirements. Specific module/command combination will likely be blocked for security reasons, but I have not yet seen a vulnerability worthy of this.

###Coins

This will contain all coin control methods. It will likely be a wrapper for `pywallet`.

###Peers

This file contains all peer management methods. Currently it also contains `Bounty` propogation methods, though this may be moved to the `Bounty` file in the future.

This also contains the `Listener` class, which can be used to handle peer and `Bounty` requests from abroad.

###Safeprint

A utility method for thread-safe, version-safe printing.

###Settings

A utility file to parse and store settings for later consideration.

###Naming standard

These are tentative and subject to change

* Temporary variables: keep to one word (ie, manager, string, etc)
* Constant variables:  `all_lowercase_with_underscores`
* All others:          `camelCase`
