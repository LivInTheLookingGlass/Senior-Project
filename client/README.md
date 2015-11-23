#Common

This is a common library. It has files that are shared between both the server and client mode. There are, however, certain methods that are overridden in each case. Most of these have to do with `Bounty` and peer propogation.

###GUI

This contains methods and data exchange hooks to deal with a user GUI.

###Problem

This file contains methods to deal with problems delivered from bounties. This includes execution, permission management, etc.

###Test

This file contains methods to deal with tests delivered from bounties. This includes execution, permission management, etc.

###Naming standard

These are tentative and subject to change

* Temporary variables: keep to one word (ie, manager, string, etc)
* Constant variables:  `all_lowercase_with_underscores`
* All others:          `camelCase`
