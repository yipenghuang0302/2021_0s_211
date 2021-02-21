# Using the Python script to run MOSS

## Ensure the following files are in the same directory:
- run_moss.py Python script
- moss script
- basefiles directory containing all of the .c/.h base files
- submissions.zip from Canvas

## Modify CONFIG if needed
- Paths to submissions_zip, submissions_dir, basefiles can be changed if needed
- "repetitions_until_ignore" is the value of -m flag
- "message" can be changed depending on the context, but must be within double quotes
- "programs" array contains the files that students wrote their programs in, modified for every assignment

## Run the Python script
- After the script runs, MOSS will upload the basefiles and files to be compared
- It will then output the following: Query submitted.  Waiting for the server's response.
- After the processing is done on the MOSS servers, a link will be outputted where the result can be found

# How the MOSS command is structured:

Structure:
./moss -l c -c "[message]" -b [all provided .c/.h files] -m [N] -d [type of file in directory]

Example use:
./moss -l c -c "CS 211 Programming Assignment 1" -c -b balanced_provided.c -b bstReverseOrder_provided.c -m 10 -d submissions/\*/\*/\*/\*.c

* -l flag specifies the programming language (C)
* -c flag specifies a message that will be attached to the result
* -d flag specifies that the files to compare are under a directory
* -b flag specifies base files containing code to exclude from checking such as code provided by instructors (eg. balanced_provided.c, ptl_code.c, etc.)
* -m flag specifies the number of times that a piece of code can be found until it stops counting toward plagiarism

### NOTES
- 'submissions/\*/\*/\*/\*.c' specifies that the files to compare are any C files in the third level subdirectory in submissions
- In the Python script, this is optimized by including the specific file names and not just any C file so that only the files we want to test will be submitted.