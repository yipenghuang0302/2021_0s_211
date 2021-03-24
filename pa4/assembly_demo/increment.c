long incr(long *p, long val) {
  long x = *p;
  *p = x + val;
  return x;
}

long call_incr() {
  long v1 = 15213;
  long v2 = incr(&v1, 3000);
  return v1+v2;
}

int main () {
  return 0;
}
