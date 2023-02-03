UPDATE: I've just noticed that Heroku no longer supports free app deployment so this app is no longer accessible. The technical report is still valuable to read for insight on the modelling process and project goals. I will try to deploy it again once I have finished the other things I am currently working on.



# Fraud-Detection-System
This repository contains a simple End-to-end ML project with the aim to build up dashboard creation, coding, and model deployment skills.

The app address is "fraud-system.herokuapp.com" (Takes a little time to load)

The Technical Report directory contains a PDF explaining the design of the system and the thought process behind the design choices.

The scripts for the training process are found in the "Fraud System Complete" directory and numbered in the order they must be run.

NOTE: prior to running the scripts, a directory named "database" must be created in the "Fraud System Complete" directory so that the SQLite database
can be created.

NOTE: The occurance of generated fraud has been increased to 1 in 5 transactions so that the dashboard can be demonstrated in a reasonable amount of time. 
Therefore, the static metrics will not match the dynamic metrics. The true occurance of fraud is set in the "lib\app_functions\new_transaction.py" file 
by changing the line "x=randint(0,4)" to "x=randint(0,587)"

NOTE: The estimates for the metrics will most likely not match the dynamic metrics even when the fraud occurance is correctly set due to the 
error from the synthetically generated data which is not accounted for.
