import os
import tarfile
import zipfile

CONFIG = {
    "submissions_zip" : "submissions.zip",
    "submissions_dir" : "submissions",
    "basefiles_dir" : "basefiles",
    "repetitions_until_ignore" : 10,
    "message" : "\"CS 211 Programming Assignment 1\"",
    "programs" : ["balanced.c", "maximum.c", "matMul.c", "bstReverseOrder.c", "goldbach.c"]
}

def getBaseFiles():
    basefiles = []
    for filename in os.listdir(CONFIG["basefiles_dir"]):
        if filename.endswith(".c"):
            # append with -b flag to indicate a base file to Moss
            basefiles.append("".join(["-b ", os.path.join(CONFIG["basefiles_dir"], filename)]))

    return basefiles

def getStudentFiles():
    basefiles = []
    for filename in CONFIG["programs"]:
        # append with [submissions_dir]/*/*/*/filename to define folder structure
        basefiles.append(os.path.join(CONFIG["submissions_dir"],"*", "*", "*", filename))

    return basefiles

def extractZip():
    print("Extracting {}".format(CONFIG["submissions_zip"]))
    with zipfile.ZipFile(CONFIG["submissions_zip"], 'r') as zip_ref:
        zip_ref.extractall(CONFIG["submissions_dir"])

def extractFiles():
    # loop through all the tar files in the submissions folder
    for filename in os.listdir(CONFIG["submissions_dir"]):
        if filename.endswith(".tar"):
            print("Extracting", os.path.join(CONFIG["submissions_dir"], filename))

            id = filename.split('_')[1] # obtain student id from second part of tarball name

            tarball = tarfile.open(os.path.join(CONFIG["submissions_dir"], filename))
            # extract into a folder named using student ID
            tarball.extractall(os.path.join(CONFIG["submissions_dir"], id))
            tarball.close()

def runMoss():
    # execute bash command to set executable permissions for Moss
    print("Setting executable permissions")
    set_permissions = "chmod ug+x moss"
    os.system(set_permissions)

    # execute bash command to run Moss
    print("Running Moss...")
    baseFiles = " ".join(getBaseFiles())
    studentFiles = " ".join(getStudentFiles())
    moss_command = "./moss -l c -c {} {} -m {} -d {}"
    moss_command = moss_command.format(CONFIG["message"], baseFiles, CONFIG["repetitions_until_ignore"], studentFiles)
    print("Executing {}".format(moss_command))
    os.system(moss_command)

if __name__ == "__main__":
    extractZip()
    extractFiles()
    runMoss()
    print("Completed running Moss. Go to the link to view the results.")