# Fraud-Detection-System
This repository contains a simple End-to-end ML project with the aim to build up dashboard creation, coding, and model deployment skills. (Keep in mind this is an old project now, my skillset has greatly improved since this was created.)

The app address is "https://fraudapp-production-50f6.up.railway.app/" 

The Technical Report directory contains a PDF explaining the design of the system and the decision making behind the design choices.

The scripts for the training process are found in the "Fraud System Complete" directory and numbered in the order they must be run.

NOTE: The occurance of generated fraud has been increased to 1 in 5 transactions so that the dashboard can be demonstrated in a reasonable amount of time. 
Therefore, the static metrics will not match the dynamic metrics. The true occurance of fraud is set in the "lib\app_functions\new_transaction.py" file 
by changing the line "x=randint(0,4)" to "x=randint(0,587)"

NOTE: The estimates for the metrics will most likely not match the dynamic metrics even when the fraud occurance is correctly set due to the 
error from the synthetically generated data which is not accounted for.

NOTE: prior to running the scripts, a directory named "database" must be created in the "Fraud System Complete" directory so that the SQLite database
can be created.
