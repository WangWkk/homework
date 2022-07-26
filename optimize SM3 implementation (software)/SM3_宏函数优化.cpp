#include <iostream>
#include <stdint.h>
#include <stdlib.h>
#include <cstring>
#include <stdio.h>
#include <ctime>
#define sm3_digest_BYTES 32
#define sm3_block_BYTES 64

#define rol(value,nBit)	(((value&0xffffffff)<<nBit)&0xffffffff|((value&0xffffffff)>>(32-nBit)))
#define P0(x)	(x ^ (rol(x, 9)) ^ (rol(x, 17)))
#define P1(x)	(x ^ (rol(x, 15)) ^ (rol(x, 23)))
#define FF0(X,Y,Z)	(X ^ Y ^ Z)
#define FF1(X,Y,Z)	((X & Y) | (X & Z) | (Y & Z))
#define GG0(X,Y,Z)	(X ^ Y ^ Z)
#define GG1(X,Y,Z)	((X & Y) | ((~X) & Z))

#define byte_swap16(x)	((x & (uint16_t)0x00ffU) << 8) | ((x & (uint16_t)0xff00U) >> 8)
#define byte_swap32(x)	((x & (uint32_t)0x000000ffUL) << 24) | ((x & (uint32_t)0x0000ff00UL) << 8) |\
	((x& (uint32_t)0x00ff0000UL) >> 8) | ((x & (uint32_t)0xff000000UL) >> 24)
#define byte_swap64(x)	((x & (uint64_t)0x00000000000000ffULL) << 56) |\
	((x& (uint64_t)0x000000000000ff00ULL) << 40) |\
	((x & (uint64_t)0x0000000000ff0000ULL) << 24) |\
	((x & (uint64_t)0x00000000ff000000ULL) << 8) |\
	((x & (uint64_t)0x000000ff00000000ULL) >> 8) |\
	((x & (uint64_t)0x0000ff0000000000ULL) >> 24) |\
	((x & (uint64_t)0x00ff000000000000ULL) >> 40) |\
	((x & (uint64_t)0xff00000000000000ULL) >> 56)

using namespace std;
typedef struct sm3_ctx_t {
	uint32_t digest[sm3_digest_BYTES / sizeof(uint32_t)];
	int nblocks;	//当前block的数量
	uint8_t block[sm3_block_BYTES * 4];
	int num;
}sm3_ctx;

void sm3_init(sm3_ctx* ctx);
void sm3_update(sm3_ctx* ctx, const uint8_t* data, size_t data_len);
void sm3_final(sm3_ctx* ctx, uint8_t* digest);

void sm3_hash(uint8_t* digest, const uint8_t* data, size_t dlen);
int sm3_hash_verify(const uint8_t* data, size_t dlen, const uint8_t* digest);
static void sm3_compress(uint32_t digest[sm3_digest_BYTES / sizeof(uint32_t)],
	const uint8_t block[sm3_block_BYTES]);

void sm3_hash(uint8_t* digest, const uint8_t* data, size_t dlen)
{
	int res = 0;
	sm3_ctx* md_ctx = new sm3_ctx;
	sm3_init(md_ctx);
	sm3_update(md_ctx, data, dlen);
	sm3_final(md_ctx, digest);
	/*for (int i = 0;i < sizeof(md_ctx->digest) / sizeof(md_ctx->digest[0]);i++)
	{
		cout << hex << (md_ctx->digest[i]);
	}*/
}
int sm3_hash_verify(const uint8_t* data, size_t dlen, const uint8_t* digest)
{
	return 0;
}

void sm3_init(sm3_ctx* ctx)
{
	ctx->digest[0] = 0x7380166F;
	ctx->digest[1] = 0x4914B2B9;
	ctx->digest[2] = 0x172442D7;
	ctx->digest[3] = 0xDA8A0600;
	ctx->digest[4] = 0xA96F30BC;
	ctx->digest[5] = 0x163138AA;
	ctx->digest[6] = 0xE38DEE4D;
	ctx->digest[7] = 0xB0FB0E4E;
	ctx->nblocks = 0;
	ctx->num = 0;
}

void sm3_update(sm3_ctx* ctx, const uint8_t* data, size_t dlen)
{
	if (ctx->num) {
		unsigned int left = sm3_block_BYTES - ctx->num;
		if (dlen < left) {
			memcpy(ctx->block + ctx->num, data, left);
			ctx->num += dlen;
			return;
		}
		else {
			memcpy(ctx->block + ctx->num, data, left);
			sm3_compress(ctx->digest, ctx->block);
			ctx->nblocks++;
			data += left;
			dlen -= left;
		}
	}
	while (dlen >= sm3_block_BYTES) {
		sm3_compress(ctx->digest, data);
		ctx->nblocks++;
		data += sm3_block_BYTES;
		dlen -= sm3_block_BYTES;
	}
	ctx->num = dlen;
	if (dlen) {
		memcpy(ctx->block, data, dlen);
	}
}

void sm3_final(sm3_ctx* ctx, uint8_t* digest) {
	size_t i;
	uint32_t* pdigest = (uint32_t*)(digest);
	uint64_t* count = (uint64_t*)(ctx->block + sm3_block_BYTES - 8);

	ctx->block[ctx->num] = 0x80;

	if (ctx->num + 9 <= sm3_block_BYTES) {
		memset(ctx->block + ctx->num + 1, 0, sm3_block_BYTES - ctx->num - 9);
	}
	else {
		memset(ctx->block + ctx->num + 1, 0, sm3_block_BYTES - ctx->num - 1);
		sm3_compress(ctx->digest, ctx->block);
		memset(ctx->block, 0, sm3_block_BYTES - 8);
	}

	count[0] = (uint64_t)(ctx->nblocks) * 512 + (ctx->num << 3);
	count[0] = byte_swap64(count[0]);

	sm3_compress(ctx->digest, ctx->block);
	//cout << hex << ctx->digest << endl;
	//for (i = 0;i < sizeof(ctx->digest) / sizeof(ctx->digest[0]);i++)
	//{
	//	pdigest[i] = byte_swap32(ctx->digest[i]);
	//	//cout <<hex<< pdigest[i];
	//}
}

static void sm3_compress(uint32_t digest[sm3_digest_BYTES / sizeof(uint32_t)],
	const uint8_t block[sm3_block_BYTES])
{
	int j;
	uint32_t W[68], W1[64];
	const uint32_t* pblock = (const uint32_t*)(block);
	uint32_t A = digest[0], B = digest[1], C = digest[2], D = digest[3];
	uint32_t E = digest[4], F = digest[5], G = digest[6], H = digest[7];

	uint32_t SS1, SS2, TT1, TT2, T[64];

	for (j = 0;j < 16;j++)
		W[j] = byte_swap32(pblock[j]);

	for (j = 16;j < 68;j++)
		W[j] = P1(W[j - 16] ^ W[j - 9] ^ rol(W[j - 3], 15)) ^ rol(W[j - 13], 7) ^ W[j - 6];

	for (j = 0;j < 64;j++)
		W1[j] = W[j] ^ W[j + 4];
	for (j = 0;j < 16;j++)
	{
		T[j] = 0x79CC4519;
		SS1 = rol((rol(A, 12) + E + rol(T[j], j)), 7);
		SS2 = SS1 ^ rol(A, 12);
		TT1 = FF0(A, B, C) + D + SS2 + W1[j];
		TT2 = GG0(E, F, G) + H + SS1 + W[j];
		D = C, C = rol(B, 9), B = A, A = TT1;
		H = G, G = rol(F, 19), F = E, E = P0(TT2);
	}
	for (j = 16;j < 64;j++)
	{
		T[j] = 0x7A879D8A;
		SS1 = rol((rol(A, 12) + E + rol(T[j], j)), 7);
		SS2 = SS1 ^ rol(A, 12);
		TT1 = FF1(A, B, C) + D + SS2 + W1[j];
		TT2 = GG1(E, F, G) + H + SS1 + W[j];
		D = C, C = rol(B, 9), B = A, A = TT1;
		H = G, G = rol(F, 19), F = E, E = P0(TT2);
	}
	digest[0] ^= A, digest[1] ^= B, digest[2] ^= C, digest[3] ^= D;
	digest[4] ^= E, digest[5] ^= F, digest[6] ^= G, digest[7] ^= H;
}

int main() {
	const char* plaintext = "abc";
	uint8_t* plaintext1 = (uint8_t*)(plaintext);
	uint8_t* digest = (uint8_t*)malloc(32 * 8);
	clock_t start, end;
	start = clock();
	for (int i = 0; i < 5;i++) {
		for (int j = 0; j <= 1000000;j++) {
			sm3_hash(digest, plaintext1, 3);
		}
	}
	//sm3_hash(digest, plaintext1, 3);
	end = clock();
	//cout << endl;
	double dur_time = double(end - start) / CLOCKS_PER_SEC / 5;
	int num_per_sec = int(1000000 / dur_time);
	cout << "每执行100万次耗时 " << dur_time << " s" << endl;
	cout << "每秒大约可以执行 " << num_per_sec << " 次" << endl;
}
