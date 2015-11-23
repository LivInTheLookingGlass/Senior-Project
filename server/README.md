#Server

This is a server library. It has files that pertain solely to server operation. These files are designed to be generic, but it is completely possible that they will need to be changed on a use-by-use basis. This is especially true on the parser file.

###Bounty

This contains overrides for `Bounty` utilities.

###Parser

This file deals with receiving `Bounty` tests and results. For results it moves it outside of this program's jurisdiction, for processing in a problem-specific program. For tests, it verifies internally.

###Peers

This file contains overrides for peer management methods. These are mostly for methods of the style `handle*()`.

###Naming standard

These are tentative and subject to change

* Temporary variables: keep to one word (ie, manager, string, etc)
* Constant variables:  `all_lowercase_with_underscores`
* All others:          `camelCase`
