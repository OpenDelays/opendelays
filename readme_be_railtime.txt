OpenDelays Program Version 1.1  19/10/2014
_____________________________________________________
This program gather Belgian train data into a database using
website railtime.be(real time data)
-----------------------------------------------------
      How To Use It:
- Run it with Python 2.6 and the MySQLdb module
- Set mysql database access (lines:11,12,13,14)
- Create the table and column named after the program or rename those one
  (lines: 76,77)

1. upload the python program somewhere on the server or on your device
2. set the scheduler task => every days, every hours
-----------------------------------------------------
See update at https://sourceforge.net/projects/opendelays/
Follow our aim at http://wemove.center/joomla/index.php/blog/item/104-open-delays
or http://wemove.center/joomla/index.php/blog
-----------------------------------------------------
Update:	1.1 19/10/2014
+ UTF-8 encoding issues fixed
+ database optimisation
+ 23h-00h data are now written with the good day in database
-----------------------------------------------------
Copyright 2014, WeMove & Samuel Jouan, GNU GPL v3.
