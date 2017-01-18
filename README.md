# Emisjent
### Overview
This is a simple Python script, which helps arrange teacher's schedule. Originally it was used to create voice emission lessons schedule. There are some restrictions, like lesson time, maximum number of lessons per week etc.

### Schedule data representation
A schedule is just a list of student's names and some `'nobody'` entries, indicating that there will be no lesson.

It is then mapped this way:

Teacher's first available date --> The first student on schedule list<br>
Teacher's second --> The second student<br>
...<br>
Teacher's last --> N-th student<br>
No date --> (N+1)-th student<br>
No date --> (N+2)-th student<br>
etc.

### Schedule arrangement
To find the best schedule simple VNS heuristics is used, it tries to minimalize custom objective function. Solution's quality depends on number of lessons, gaps in the schedule and some hard limits. 

### Technical notes
Input file is a .csv file with availability information. The script is adapted to .csv generated from availability form created in Google Forms – here is an example form: http://bit.ly/2k3TxGN.
