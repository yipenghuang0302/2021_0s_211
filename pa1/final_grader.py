import os
import tarfile
import subprocess
import shutil

submissions_location = "/ilab/users/nrm98/TA211/submissions"
submission_list = os.listdir(submissions_location)
for person in submission_list:

    #Untar + Extract Files
    my_tar = tarfile.open(f"{submissions_location}/{person}")
    my_tar.extractall(submissions_location)

    #Run the grading command to get output
    result = subprocess.check_output("python3 assignment_autograder.py", shell=True, cwd=f"{submissions_location}/pa1").decode('ascii')

    #Parse data to get Score+ID of person
    result = result.split("\n")[-3].split(" ")[3]
    ID = person.split("_")[2]
    print(f"ID: {ID}")
    print(f"Score: {result}")
    print("***********************")
    shutil.rmtree(f"{submissions_location}/pa1")