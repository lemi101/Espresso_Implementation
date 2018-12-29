class espresso:
    def __init__(self, key, iv):
        # Init Variables
        self.key = key
        self.iv = iv
        self.counter = 0
        self.ls = []

        # Init Register 
        for _ in range(2000): self.ls.append(None)

        # Insert Key to Register
        for i in range(len(self.key)):
            k = list(format(key[i], '08b'))
            k.reverse()

            for j in range(len(k)): 
                self.ls[(8 * i) + j] = int(k[j])

        # Insert IV to Register
        for i in range(len(self.iv)):
            v = list(format(iv[i], '08b'))
            v.reverse()

            for j in range(len(v)): 
                self.ls[128 + (8 * i) + j] = int(v[j])
        
        # Insert "1"'s to Register 
        for i in range(31):
            self.ls[128 + 96 + i] = 1
        
        # End 256 bit Init Register with "0"
        self.ls[255] = 0

        # Init Register Run (x 256)
        for _ in range(256):
            self.update(1) 
        
        
    def update(self, init):
        # Run Register
        out  = self.ls[80 + self.counter] ^ self.ls[99 + self.counter] ^ self.ls[137 + self.counter] ^ self.ls[227 + self.counter] ^ self.ls[222 + self.counter] ^ self.ls[187 + self.counter] ^ self.ls[243 + self.counter] & self.ls[217 + self.counter] ^ self.ls[247 + self.counter] & self.ls[231 + self.counter] ^ self.ls[213 + self.counter] & self.ls[235 + self.counter] ^ self.ls[255 + self.counter] & self.ls[251 + self.counter] ^ self.ls[181 + self.counter] & self.ls[239 + self.counter] ^ self.ls[174 + self.counter] & self.ls[44 + self.counter]  ^  self.ls[164 + self.counter] & self.ls[29 + self.counter]  ^ self.ls[255 + self.counter] & self.ls[247 + self.counter] & self.ls[243 + self.counter] & self.ls[213 + self.counter] & self.ls[181 + self.counter] & self.ls[174 + self.counter]
        n255 = self.ls[0 + self.counter] ^ self.ls[41 + self.counter] & self.ls[70 + self.counter]
        n251 = self.ls[42 + self.counter] & self.ls[83 + self.counter]  ^ self.ls[8 + self.counter]
        n247 = self.ls[44 + self.counter] & self.ls[102 + self.counter] ^ self.ls[40 + self.counter]
        n243 = self.ls[43 + self.counter] & self.ls[118 + self.counter] ^ self.ls[103 + self.counter]
        n239 = self.ls[46 + self.counter] & self.ls[141 + self.counter] ^ self.ls[117 + self.counter]
        n235 = self.ls[67 + self.counter] & self.ls[90 + self.counter] & self.ls[110 + self.counter] & self.ls[137 + self.counter]
        n231 = self.ls[50 + self.counter] & self.ls[159 + self.counter] ^ self.ls[189 + self.counter]
        n217 = self.ls[3 + self.counter] & self.ls[32 + self.counter]
        n213 = self.ls[4 + self.counter] & self.ls[45 + self.counter]
        n209 = self.ls[6 + self.counter] & self.ls[64 + self.counter]
        n205 = self.ls[5 + self.counter] & self.ls[80 + self.counter]
        n201 = self.ls[8 + self.counter] & self.ls[103 + self.counter]
        n197 = self.ls[29 + self.counter] & self.ls[52 + self.counter] & self.ls[72 + self.counter] & self.ls[99 + self.counter]
        n193 = self.ls[12 + self.counter] & self.ls[121 + self.counter]

        if(init):
            n255 ^= out
            n217 ^= out
        
        # Update State
        self.counter += 1

        self.ls[255 + self.counter] = n255
        self.ls[251 + self.counter] ^= n251
        self.ls[247 + self.counter] ^= n247
        self.ls[243 + self.counter] ^= n243
        self.ls[239 + self.counter] ^= n239
        self.ls[235 + self.counter] ^= n235
        self.ls[231 + self.counter] ^= n231
        self.ls[217 + self.counter] ^= n217
        self.ls[213 + self.counter] ^= n213
        self.ls[209 + self.counter] ^= n209
        self.ls[205 + self.counter] ^= n205
        self.ls[201 + self.counter] ^= n201
        self.ls[197 + self.counter] ^= n197
        self.ls[193 + self.counter] ^= n193

        # ??? (Copied from Original Test Vector, Maybe for Dynamic Array?)
        if(self.counter == 1700):
            # Some memcpy (memcpy(ls, ls+1700, 256);)
            self.counter = 0

        return out


if __name__ == "__main__":
    # Key 128 bits / 16 Bytes
    key = [] 
    for x in range(16): key.append(int(x))

    # IV 96 bits / 12 Bytes
    iv = [] 
    for y in range(12): iv.append(int(y))

    # Keystream size (20 Bytes)
    ks = []
    for _ in range(20 * 8): ks.append(0)

    esp = espresso(key, iv)

    ky = []
    for _ in range(20 * 8): ky.append(esp.update(0))
    
    keystream = ""
    kp = ""

    # Print Keystream
    for z in range(len(ks)):
        p = ks[z] ^ ky[z]
        kp += str(p)

        if(len(kp) == 8):
            kp = ''.join(reversed(kp))
            keystream += hex(int(kp, 2))[2:]
            kp = ""
    
    print(keystream)
