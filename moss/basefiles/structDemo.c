#include <stdio.h>
#include <stdlib.h>

typedef struct Name {
    char* first_name;
    char* last_name;
} Name;

typedef struct Student {
    struct Name name;
    int age;
    char* major;
} Student;

int main(int argc, char const *argv[])
{
    // initialize with values
    Name name1 = {"Michael", "Jordan"};
    printf("name1: %s %s\n", name1.first_name, name1.last_name);
    
    // set values after initialization
    Name name2;
    name2.first_name = "Kobe";
    name2.last_name = "Bryant";
    printf("name2: %s %s\n\n", name2.first_name, name2.last_name);

    // create student1 using name1
    Student student1 = {name1, 23, "Computer Science"};

    printf("student1:\nname: %s %s, age: %d, major: %s\n\n", 
            student1.name.first_name, student1.name.last_name, student1.age, student1.major);

    // create student2 using name2
    Student student2;
    // student2.name = name2;
    student2.name.first_name = "John";
    student2.name.last_name = "Doe";
    student2.age = 24;
    student2.major = "Math";

    printf("student2:\nname: %s %s, age: %d, major: %s\n", 
            student2.name.first_name, student2.name.last_name, student2.age, student2.major);

    return 0;
}
