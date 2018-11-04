#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/* hex2dec */
int hex2dec(char c)
{
    int val;

    if ((c >= '0') && (c <= '9')) {
        val = c - '0';
    } else if ((c >= 'A') && (c <= 'F')) {
        val = c - 'A' + 10;
    } else if ((c >= 'a') && (c <= 'f')) {
        val = c - 'a' + 10;
    } else {
        return -1;
    }

    return val;
}


/* hex2dec2 - 2char version of hex2dec */
int hex2dec2(char *ptr)
{
    int val, val2;

    val = hex2dec(ptr[0]);
    if ((val < 0)  || (val > 0xf)) {
        return -1;
    }

    val2 = hex2dec(ptr[1]);
    if ((val2 < 0)  || (val2 > 0xf)) {
        return -1;
    }

    return (val * 0x10) + val2;
}



/* decode hex and return length */
int decode_hex(char *arg, unsigned char **decoded)
{
    int i;
    int len = strlen(arg);
    int val;

    if ((len < 1) || ((len % 2) != 0)) {
        return 0;
    }

    *decoded = (char *)malloc(len / 2);

    if (*decoded) {

        for (i=0; i<(len / 2); i++) {
            val = hex2dec2(arg + (i*2));
            if ((val < 0) || (val > 255)) {
                printf("error in hexstring\n");
                free(*decoded);
                *decoded = NULL;
                return 0;
            }
            (*decoded)[i] = (char) val;
        }

    } else {
        printf("decode_hex malloc error\n");
        return 0;
    }

    return (len / 2);
}



int main(int argc, char *argv[])
{
    unsigned char *key = NULL;
    int keylen = 0;
    unsigned char *buffer = NULL;
    int n_read = 0;
    int i;
    unsigned char c;


    if (argc != 2) {
        printf("modvigenere key (hexstring)\n");
        exit(1);
    }

    keylen = decode_hex(argv[1], &key);

    buffer = (char *)malloc(keylen);

    while ((n_read = read(0, buffer, keylen)) > 0) {
        for (i=0; i<n_read; i++) {
            switch (i % 8) {
                case 0:
                    c = buffer[i] ^ key[i];
                    break;
                case 1:
                    c = (buffer[i] + key[i]) % 256;
                    break;
                case 2:
                    c = buffer[i] ^ key[i];
                    break;
                case 3:
                    c = (buffer[i] - key[i]) % 256;
                    break;
                case 4:
                    c = buffer[i] ^ key[i];
                    break;
                case 5:
                    c = buffer[i] ^ key[i];
                    break;
                case 6:
                    c = (buffer[i] + key[i]) % 256;
                    break;
                case 7:
                    c = (buffer[i] - key[i]) % 256;
                    break;
            }
            printf("%02x", c);

        }
        if (n_read < keylen) {
            exit(0);
        }
    }
}

