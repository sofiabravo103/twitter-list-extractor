# twitter-extractor 

An extraction tool for building machine learning training based on users from lists in Twitter.

## Set up ##

#### Install python 2.7 ####
* Ubuntu/Debian:
```sudo apt-get install python2.7```
* Fedora:
```sudo yum install python2.7```
* Arch:
```sudo pacman -S python2```

#### Install pip through package manager ####
* Ubuntu/Debian:
```sudo apt-get install python-pip```
* Fedora:
```sudo yum install python-pip```
* Arch:
```sudo pacman -S python2-pip```

#### Python dependencies ####
* twitter
```pip install tweepy```

## Specifications file ##

To get the extractor running you only need to fill the spec_information.py file (and locate it in the repo's root folder). First you will need to create a twitter app [here](https://apps.twitter.com/), 
and then go to **Keys and Access Tokens** to get your consumer key and access token, you will need this information
to access twitter.

~~~~~
spec_consumer_key = '...'
spec_consumer_secret = '...'
spec_access_token = '...'
spec_access_token_secret = '...'
~~~~~

In the examples folder you will find an example of how the configuration file must look.
The information required to download users from ach list is specified in the dictionary spec_list.
~~~~~
spec_lists = {
  'id' :                              
      {'screen_name' : '...',        
      'list_name' : '...',                                             
      'target_size' :  100},

  'other' :
	... 
}

## Usage ##

