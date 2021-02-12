import os
import tarfile
import subprocess
import shutil

# dictionary to hold student grades
# key: student id, value: grade
grades = {}

pa = "pa1" # the current programming assignment
submissions = "{}/submissions".format(pa) # directory that holds the student submissions
toGrade = "{}/current/{}".format(submissions, pa) # path to current student submission
programs = ["balanced", "bstReverseOrder", "goldbach", "matMul", "maximum"] # programs to grade

# loop through all the tar files in the submissions folder
for filename in os.listdir(submissions):
    if filename.endswith(".tar"):
        print("\nReading", os.path.join(submissions, filename))

        id = filename.split('_')[1] # obtain student id from second part of tarball name

        tarball = tarfile.open(os.path.join(submissions, filename))
        tarball.extractall(os.path.join(submissions, "current")) # extract into a folder called "current"
        tarball.close()

        # execute bash command to check for changes in assignment_autograder.py
        bash_command = "git diff {}/assignment_autograder.py {}/submissions/current/pa1/assignment_autograder.py".format(pa, pa)
        bash_output = subprocess.check_output(bash_command.split())
        if (bash_output != ""):
            # overwrite assignment_autograder.py with original
            shutil.copyfile("{}/assignment_autograder.py".format(pa), "{}/assignment_autograder.py".format(toGrade)) #copy src to dst

        # check for changes to test and answer files
        for program in programs:
            print("\nChecking {}\n".format(program))

            tests = '/'.join([pa, program, "tests"])
            answers = '/'.join([pa, program, "answers"])

            original_autograder = '/'.join([pa, program, "autograder.py"])
            student_autograder = '/'.join([toGrade, program, "autograder.py"])
            bash_command = "git diff {} {}".format(original_autograder, student_autograder)
            if (bash_output != ""):
                # overwrite with original
                shutil.copyfile(original_autograder, student_autograder) #copy src to dst

            if os.path.isdir(tests):
                for root, subdirectories, files in os.walk(tests):
                    for file in files:
                        print(file)
                        original_file = os.path.join(root, file)
                        student_file = '/'.join([toGrade, program, "tests", file])
                        bash_command = "git diff {} {}".format(original_file, student_file)
                        bash_output = subprocess.check_output(bash_command.split())
                        if (bash_output != ""):
                            # overwrite with original
                            shutil.copyfile(original_file, student_file) #copy src to dst

            if os.path.isdir(answers):
                for root, subdirectories, files in os.walk(answers):
                    for file in files:
                        print(file)
                        original_file = os.path.join(root, file)
                        student_file = '/'.join([toGrade, program, "answers", file])
                        bash_command = "git diff {} {}".format(original_file, student_file)
                        bash_output = subprocess.check_output(bash_command.split())
                        if (bash_output != ""):
                            # overwrite with original
                            shutil.copyfile(original_file, student_file) #copy src to dst

        # remove the "current" directory for the next iteration
        bash_command = "rm -r {}/submissions/current".format(pa)
        subprocess.check_output(bash_command.split())

        # REMAINING WORK:
        # run assignment_autograder.py in the 'toGrade' path
        # set a time limit on the autograder running time
        # store results in grades dictionary
        # output grades to csv file
