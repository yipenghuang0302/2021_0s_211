long plus(long x, long y) {
  return x+y;
}

void sumstore(long x, long y, long* dest) {
  long t = plus (x, y);
  *dest = t;
}

int main() {
  long x=0, y=0, dest;
  sumstore (x, y, &dest);
  return 0;
}
