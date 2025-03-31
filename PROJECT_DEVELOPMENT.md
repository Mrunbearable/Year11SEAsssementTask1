## Functional requirements
- - - 
### Data Retrival
    -The GUI/Program must be able to retrieve and transit Data to and from the computer and user
    -The GUI/Program must store the user info/data in a safe space where only the user and access and close
    -The GuI/Program must ensure that consent is allowed before used online for sponsering/marketing
### User Interface
    - The User Interface must be accessible to users only with permission. 
    - The User inferace must work and provide user with support when requested.
    -The GUI goal is to inform and provide the user with data whenever needed.
### Data Display
    - The Display must be readble and easy to understand. 
    - User should be allowed to choose options and provide feedback.
    - For disable people. accessibilty options may be change to support the user.
    -The Data must not be corrupted or tainted with a virus

## Non-Function Requirements
- - -
### Peformance
    - The system must be able to run smoothly
    - If there are issues in the User Interface, it must be fixed immedialty
    - The security of the User Interface must be Perfect, as if not secured could lead to potential breach and viruses
    - The User Interface must improve from user feedback to provide for users needs
    - The system must provide a variety of options to provide the needs of the user
### Reliabilty
    - The Data Provided on the User Interface must be  reliable and dated. This means the data is sourced with citations
    -The User Interface must always be avaible to user and should never be taken down unless malware takes over. If malware takes over, it should inform the user that there is an issue and should resume soon
### Usability and Accesibility
    -The layout of the User Interface must be easy for the user to navigate and understand
    -The User should be able to download the Data without consent
    -If the user needs support, The program should always provide help which the user can understand unless unavailiable
    -The User Interface should always state the rules before it can be used, this ensure the chance of being sued
    -The User Interface should be able to help disable people

## Functional Specifications
- - - 
### User Requirements
The user should easily be able to navigate the program. This statements only applies if the user is allowed access. The user should be allowed to manage and change the themes of GUI according to her prefrences. The user should also be allowed to choose

### Inputs and Outputs
The user be be able to input what data/information they are trying to find. In respone the GUI should output the info back.

### Core Features
The main purpose of this GUI is to proivde users with finding info easily. Buttons and commands must be easy to navigate and should not redirect to a different route. It is critical that this GUI meets user request otherwise the GUI is faulty and should not continue

### User Interaction
The Data is be viewed on a GUI. They can either press buttons or search from the bar

### Error Handling
The GUI should not crash and hand common errors gracefully. If there is an error it will restart the program and notify the devloper

## Gantt Chart
- - -
![Alt text](Screenshot%202025-03-10%20102117.png)

## Structure Chart
- - -
![Alt text](Structure%20Chart.png)

## Algorithms
- - -
![Alt text](Blank%20diagram%20(1).png)

## PseudoCode
```
BEGIN main()
    INPUT parameter
    choice=0
        WHILE choice is not 7 THEN
            INPUT choice
            IF choice is 1 THEN
                JobsByLocation
            ELSEIF choice is 2 THEN
                JobsBySector
            ELSEIF choice is 3 THEN
                PartTimeJobs
            ELSEIF choice is 4 THEN
                EntryLevelJobs
            ELSEIF choice is 5 THEN
                HybridJobs
            ELIF choice is 6 THEN
                RemoteJobs
            ELSE
                DISPLAY 'An error has occurred, restarting program'
            ENDIF
        ENDWHILE
END main()    
``` 
## Data Dictionary

Variable|Data Type|Format for Display|Size in Bytes|Size for Display|Description|Example|Validation|
|---|---|---|---|---|---|---|---
|Name|string|xxx|50|50|The name of the job/title|Doctor|must be a valid string|
|Location|string|xx_xx|20|100|The location of the job/title|Perth_WA|must be a valid string|
|Date|interger|N/NN/NNNNN|4|2|The Date of the upload|19/20/2021|must be a valid date and correct format|

