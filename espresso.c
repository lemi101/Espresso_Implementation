/*
 * Reference implementation of the Espresso stream cipher
 *
 * Author: Martin Hell, 2015.
 * This is a naive implementaion of the Espresso stream cipher. 
 * It should only be used to verify test vectors. It should not 
 * be used in benchmarking. No optimizations have been considered
 * in the implementation.
 *
*/


#include <stdio.h>
#include <memory.h>

typedef struct {
  unsigned char key[16];  //128 bit key
  unsigned char iv[12];   //96 bit IV
  unsigned char ls[2000]; //Shift register
  unsigned int ctr;
} espresso_ctx;

int update_ls(espresso_ctx *ctx, unsigned char init) {
  unsigned char n255, n251, n247, n243, n239, n235, n231, n217, n213, n209, n205, n201, n197, n193, out;
  unsigned char *ls = ctx->ls;
  unsigned int *ctr = &(ctx->ctr);

  // Save new variables and output
  out  = ls[80+*ctr] ^ ls[99+*ctr] ^ ls[137+*ctr] ^ ls[227+*ctr] ^ ls[222+*ctr] ^ ls[187+*ctr] ^ \
         ls[243+*ctr]&ls[217+*ctr] ^ ls[247+*ctr]&ls[231+*ctr] ^ ls[213+*ctr]&ls[235+*ctr] ^ \
         ls[255+*ctr]&ls[251+*ctr] ^ ls[181+*ctr]&ls[239+*ctr] ^ ls[174+*ctr]&ls[44+*ctr]  ^  \
         ls[164+*ctr]&ls[29+*ctr]  ^ ls[255+*ctr]&ls[247+*ctr]&ls[243+*ctr]&ls[213+*ctr]&ls[181+*ctr]&ls[174+*ctr];
  n255 = ls[0+*ctr] ^ ls[41+*ctr]&ls[70+*ctr];
  n251 = ls[42+*ctr]&ls[83+*ctr]  ^ ls[8+*ctr];
  n247 = ls[44+*ctr]&ls[102+*ctr] ^ ls[40+*ctr];
  n243 = ls[43+*ctr]&ls[118+*ctr] ^ ls[103+*ctr];
  n239 = ls[46+*ctr]&ls[141+*ctr] ^ ls[117+*ctr];
  n235 = ls[67+*ctr]&ls[90+*ctr]&ls[110+*ctr]&ls[137+*ctr];
  n231 = ls[50+*ctr]&ls[159+*ctr] ^ ls[189+*ctr];
  n217 = ls[3+*ctr]&ls[32+*ctr];
  n213 = ls[4+*ctr]&ls[45+*ctr];
  n209 = ls[6+*ctr]&ls[64+*ctr];
  n205 = ls[5+*ctr]&ls[80+*ctr];
  n201 = ls[8+*ctr]&ls[103+*ctr];
  n197 = ls[29+*ctr]&ls[52+*ctr]&ls[72+*ctr]&ls[99+*ctr];
  n193 = ls[12+*ctr]&ls[121+*ctr];
  if (init) {
	  n255 ^= out;
	  n217 ^= out;
  }
  
  // Update state
  (ctx->ctr)++;
  ls[255+*ctr] = n255;
  ls[251+*ctr] ^= n251;
  ls[247+*ctr] ^= n247;
  ls[243+*ctr] ^= n243;
  ls[239+*ctr] ^= n239;
  ls[235+*ctr] ^= n235;
  ls[231+*ctr] ^= n231;
  ls[217+*ctr] ^= n217;
  ls[213+*ctr] ^= n213;
  ls[209+*ctr] ^= n209;
  ls[205+*ctr] ^= n205;
  ls[201+*ctr] ^= n201;
  ls[197+*ctr] ^= n197;
  ls[193+*ctr] ^= n193;
  
  if ((ctx->ctr) == 1700) {
	memcpy(ls, ls+1700, 256);
	(ctx->ctr) = 0;
  }

  return out;
} 


int init_ls(espresso_ctx *ctx) {
  unsigned int i,j;
  unsigned char *ls = ctx->ls;

  // Load key and IV
  for (i=0;i<16;++i) for (j=0;j<8;++j) ls[8*i + j] = (((ctx->key[i])>>j)&1);
  for (i=0;i<12;++i) for (j=0;j<8;++j) ls[128 + 8*i + j] = (((ctx->iv[i])>>j)&1);
  for (i=0;i<31;++i) ls[128+96+i] = 1;
  ls[255] = 0;
  ctx->ctr=0;
  for (i=0;i<256;++i) update_ls(ctx,1);
  return 0;
}


int main() {
  int i,j;
  unsigned char keystream[20];
  espresso_ctx ctx;
  memset(keystream,0,20);
  
  // set key and IV
  for (i=0;i<16;++i) (&ctx)->key[i] = (unsigned char) i;
  for (i=0;i<12;++i) (&ctx)->iv[i] = (unsigned char) i;
  
  // Initiate cipher
  init_ls(&ctx);

  // Generate keystream bytes
  for (i=0;i<20;++i) for (j=0;j<8;++j) keystream[i] ^= (update_ls(&ctx,0)<<j);
  // Print keystream bytes
  for (i=0;i<20;++i) printf("%02X",keystream[i]);
  printf("\n");
}