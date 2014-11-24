opendelays
==========

Python scripts that gather trains data


1. Presentation

Open Delays aims to disclose a specific kind of transport datas: the delays.

Today, planned timetables of future trips have become generally available in multiple formats. Delays of the last hours of the day are also accessible on the train website, so you know wether your current train is on time. But the accumulated delays data are generally not available : you don't find easily the accumulation of passed exploitation data of a given train line during the last year. We think that the users should have access to delays data, and for sure the company that operates the trains, or a government office, should not be the only ones to access this data.

Our goal with Open Delays is to gather exploitation data, and make it accessible to the users. With Open Delays, you could know for example that the train you are stepping in, had this last year 15mn delay in 30% of its trips : you can prepare for a probable delay on your trip ! Outside of the single traveller needs, such an overview on exploitation data is also a powerful way to make service quality more transparent, and identify precisely where are the structural problems. 
Until recently, companies were very reluctant to realease that data. Now, times and minds have changed, and public transport institutions find quite normal that users can access exploitation data, even if they don't publish them actively. So we are happy to propose this tool, that allows the user to get an enhanced vision on transport exploitation. 
This initiative in publishing delays data is not new, but we try to propose a new approach : we propose a tool that is reusable for any transport system, and insist on the openness of delays data. We expect that Open Delays will be re-used into other solutions and applications, and that this will contribute to improve users' quality of life.


2. Technical aspects and project aim

    Short program in python that pick-up one hour of data in Railtime.be website, and converts it into a CSV (comma-separated values) format.
    Our aim is limited to gather the data, and for the moment not to perform additional statistics or queries on it.
    Periodically, the gathered databases will be shared on our website in different ways (CSV, Excel/ODS sheet or directly viewable).
    Fields gathered: date, hour, train number, train type, departure station, departure time and arrival station, delays at arrival station.
    Download here [github] Open Delays program in python. Copyright 2014, WeMove & Samuel Jouan, GNU GPL v3.
    Download a sample of data gathered with Open Delays : ODS, CSV (lightweight for web usage)
    See the software development page on Github.

Technical infrastructure :

    VPS : offer Classic v1 on OVH http://www.ovh.com/fr/vps/vps-classic.xml :
    CPU 1 Core
    RAM 1Go
    Hard disk 10Go Raid 10
    Bandwidth 100Mbps
    MySQL server version: 5.5.40-0+wheezy1
    MySQL Protocol version: 10
    Webserver Apache/2.2.22 (Debian)
    MySQL client version: 5.5.40
    PHP extension: mysqli
    phpMyAdmin Version information: 3.4.11.1deb2+deb7u1

Resources used 20 November :

    %UC : 60% /coreV1, for 4 scripts
    %RAM : 30% /1Go
    %STORAGE: 10% /10Go

Scripts :

    OpenDelays_it : 59 octets /record; 52k records/day = 1,1 Go/year
    Opendelays_be1 : 50 octets /record; 22 k records/day = 400 Mo/year
    Opendelays_be2 : 32 octets /record; 17 k records/day = 200 Mo/year
    OpenDelays_uk : 79 octets /record; 250 k records/day = 7.2 Go/year

 
3. Milestones

1. Open Delays program written : DONE, 19 October 2014. See github for the code source.
2. Gathering delays data from 1 country : Belgium : DONE, 28 October 2014 . We are however not publishing the data now.
3. Gathering delays from 2 other European countries : United-Kingdom : DONE, 04 November 2014 ; Italy : DONE, 12 November 2014
4. Consolidating the system : RUNNING
3. Applications
Visualization of delays by Italian stations on 21 November 2014 - thanks to Patrick Hausman !
ritardo 20141123
 
