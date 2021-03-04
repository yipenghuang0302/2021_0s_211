#include <stdlib.h>
#include <stdio.h>

unsigned char sl_uc ( unsigned char in0, unsigned char in1 ) {
  return in0<<in1;
}
unsigned short sl_us ( unsigned short in0, unsigned short in1 ) {
  return in0<<in1;
}
unsigned int sl_ui ( unsigned int in0, unsigned int in1 ) {
  return in0<<in1;
}
unsigned long sl_ul ( unsigned long in0, unsigned long in1 ) {
  return in0<<in1;
}

signed char sl_sc ( signed char in0, signed char in1 ) {
  return in0<<in1;
}
signed short sl_ss ( signed short in0, signed short in1 ) {
  return in0<<in1;
}
signed int sl_si ( signed int in0, signed int in1 ) {
  return in0<<in1;
}
signed long sl_sl ( signed long in0, signed long in1 ) {
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

int main () {
  return EXIT_SUCCESS;
}
