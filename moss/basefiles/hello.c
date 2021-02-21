#include<stdio.h>
#include<stdlib.h>

typedef struct node{
	int num;
	struct node * next;
}node;

int pop (node * head){
	node * temp = NULL;

	if(head==NULL){
		return -1;
	}

	else{
		temp = head;
		head = (*head).next; //head->next;
		return temp->num;
	}
}

node push (node * head, int val){

	node temp ;
	temp.num = val;
	temp.next = NULL;

	if(head == NULL){
		return temp;
	}

	else{
		temp.next = head;
		return temp;
	}


int val = 20;
int v = 10;
int * x = &v;



val = *x;
x = &val;

(*x) = val;

}

int main(int argc, int* argv[]){

	node * head = NULL;
	int val = 3;
	head = &push(head, val);

}

