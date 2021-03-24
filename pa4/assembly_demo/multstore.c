long mult2 (
  long a,
  long b
) {
  long s = a * b;
  return s;
}

void multstore(
  long x,
  long y,
  long *dest
) {
  long t = mult2(x,y);
  *dest = t;
}

int main () {
  return 0;
}
