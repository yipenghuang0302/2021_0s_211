#include <stdlib.h>
#include <stdio.h>

unsigned char not_c ( unsigned char input ) {
  return ~input;
}
unsigned short not_s ( unsigned short input ) {
  return ~input;
}
unsigned int not_i ( unsigned int input ) {
  return ~input;
}
unsigned long not_l ( unsigned long input ) {
  return ~input;
}

unsigned char xor_c ( unsigned char in0, unsigned char in1 ) {
  return in0 ^ in1;
}
unsigned short xor_s ( unsigned short in0, unsigned short in1 ) {
  return in0 ^ in1;
}
unsigned int xor_i ( unsigned int in0, unsigned int in1 ) {
  return in0 ^ in1;
}
unsigned long xor_l ( unsigned long in0, unsigned long in1 ) {
  return in0 ^ in1;
}

char sl_c ( char in0, char in1 ) {
  return in0<<in1;
}
short sl_s ( short in0, short in1 ) {
  return in0<<in1;
}
int sl_i ( int in0, int in1 ) {
  return in0<<in1;
}
long sl_l ( long in0, long in1 ) {
  return in0<<in1;
}

unsigned char sr_uc ( unsigned char in0, unsigned char in1 ) {
  return in0>>in1;
}
unsigned short sr_us ( unsigned short in0, unsigned short in1 ) {
  return in0>>in1;
}
unsigned int sr_ui ( unsigned int in0, unsigned int in1 ) {
  return in0>>in1;
}
unsigned long sr_ul ( unsigned long in0, unsigned long in1 ) {
  return in0>>in1;
}

signed char sr_sc ( signed char in0, signed char in1 ) {
  return in0>>in1;
}
signed short sr_ss ( signed short in0, signed short in1 ) {
  return in0>>in1;
}
signed int sr_si ( signed int in0, signed int in1 ) {
  return in0>>in1;
}
signed long sr_sl ( signed long in0, signed long in1 ) {
  return in0>>in1;
}

unsigned char neg_uc ( unsigned char input ) {
  return -input;
}
unsigned short neg_us ( unsigned short input ) {
  return -input;
}
unsigned int neg_ui ( unsigned int input ) {
  return -input;
}
unsigned long neg_ul ( unsigned long input ) {
  return -input;
}

signed char neg_sc ( signed char input ) {
  return -input;
}
signed short neg_ss ( signed short input ) {
  return -input;
}
signed int neg_si ( signed int input ) {
  return -input;
}
signed long neg_sl ( signed long input ) {
  return -input;
}

int main () {
  return EXIT_SUCCESS;
}
