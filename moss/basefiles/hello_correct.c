#include<stdio.h>
#include<stdlib.h>

typedef struct node{
	int num;
	struct node * next;
}node;

int pop (node ** head){
	node * temp = NULL;

	if(*head==NULL){
		return -1;
	}

	else{
		temp = *head;
		*head = (**head).next; //(*head)->next;
		int res = temp->num;
		free(temp);
		return res;
	}
}

void push (node ** head, int val){

	node * temp = malloc(1*sizeof(node));
	temp->num = val;
	temp->next = *head;
	*head = temp;
	return;
}

void freestack(node ** first_node){
	node * ptr = *first_node;
	while(ptr!=NULL){
		freestack(&ptr->next);
		free(ptr);
	}
}

int main(int argc, int* argv[]){

	node * head = NULL;
	int val = 3;
	push(&head, val);
	push(&head, 3);
	int popped_thingy = pop(&head);
	freestack(&head);
	return 0;

}

