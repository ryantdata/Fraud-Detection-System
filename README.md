Hello!

# Fraud-Detection-System
This repository contains a simple End-to-end ML project with the aim to build up dashboard creation, coding, and model deployment skills.

The app address is "fraud-system.herokuapp.com"

The Technical Report directory contains a PDF explaining the design of the system and the thought process behind the design choices.

The scripts for the training process are found in the "Fraud System Complete" directory and numbered in the order they must be run.

NOTE: prior to running the scripts, a directory named "database" must be created in the "Fraud System Complete" directory so that the SQLite database
can be created.

NOTE: The occurance of generated fraud has been increased to 1 in 5 transactions so that the dashboard can be demonstrated in a reasonable amount of time. 
Therefore, the static metrics will not match the dynamic metrics. The true occurance of fraud is set in the "lib\app_functions\new_transaction.py" file 
by changing the line "x=randint(0,4)" to "x=randint(0,587)"

