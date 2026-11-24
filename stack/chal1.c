#include <stdio.h>
#include <unistd.h>

// rop gadgets
__attribute__((naked, used)) void sub_406767(void) {
  __asm__("pop %rdi\n"
          "ret\n");
}
__attribute__((naked, used)) void sub_404242(void) { __asm__("ret\n"); }

static void setup(void) {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}

__attribute__((noinline)) void win(void) {
  puts("gg frickin ez");
  execve("/bin/sh", NULL, NULL);
}

__attribute__((noinline)) void vuln(void) {
  char buf[64];

  printf("let me tell you something: %p\n", puts);

  puts("now tell me something:");
  fgets(buf, 999, stdin);

  puts("don't say that!");
}

int main(void) {
  setup();
  vuln();
  return 0;
}
