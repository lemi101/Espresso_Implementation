class Espresso
  # Accessor for Access Var
  attr_accessor :key, :iv, :counter, :ls
    def initialize(key, iv)
      # Init Variable
      @key = key
      @iv = iv
      @counter = 0
      @ls = Array.new()

      (0..1999).each do |i|
        @ls.push("x")
      end

      # Insert Key
      @key = @key.map {|x| 
      ("%08b" % x).chars
      }

      @key.each_index {|y| 
      @key[y].each {|z| 
      @ls.insert((y * 8), z.to_i)
        }
      }

      # Insert IV
      @iv = @iv.map {|x| 
      ("%08b" % x).chars
      }

      @iv.each_index {|y| 
      @iv[y].each {|z| 
      @ls.insert(128 + (y * 8), z.to_i)
        }
      }

      # Insert 1's
      (0..30).each do |i|
        @ls.insert((128 + 96 + i), 1)
      end

      # End 256 bit Init Register with 0
      @ls.insert(255, 0)

      # Run Update Init 256x
      (0..255).each do |i|
        update(true)
      end

    end

    def update(init)
      # Run Register
      out  = @ls[80 + @counter] ^ @ls[99 + @counter] ^ @ls[137 + @counter] ^ @ls[227 + @counter] ^ @ls[222 + @counter] ^ @ls[187 + @counter] ^ @ls[243 + @counter] & @ls[217 + @counter] ^ @ls[247 + @counter] & @ls[231 + @counter] ^ @ls[213 + @counter] & @ls[235 + @counter] ^ @ls[255 + @counter] & @ls[251 + @counter] ^ @ls[181 + @counter] & @ls[239 + @counter] ^ @ls[174 + @counter] & @ls[44 + @counter]  ^  @ls[164 + @counter] & @ls[29 + @counter]  ^ @ls[255 + @counter] & @ls[247 + @counter] & @ls[243 + @counter] & @ls[213 + @counter] & @ls[181 + @counter] & @ls[174 + @counter]
      n255 = @ls[0 + @counter] ^ @ls[41 + @counter] & @ls[70 + @counter]
      n251 = @ls[42 + @counter] & @ls[83 + @counter]  ^ @ls[8 + @counter]
      n247 = @ls[44 + @counter] & @ls[102 + @counter] ^ @ls[40 + @counter]
      n243 = @ls[43 + @counter] & @ls[118 + @counter] ^ @ls[103 + @counter]
      n239 = @ls[46 + @counter] & @ls[141 + @counter] ^ @ls[117 + @counter]
      n235 = @ls[67 + @counter] & @ls[90 + @counter] & @ls[110 + @counter] & @ls[137 + @counter]
      n231 = @ls[50 + @counter] & @ls[159 + @counter] ^ @ls[189 + @counter]
      n217 = @ls[3 + @counter] & @ls[32 + @counter]
      n213 = @ls[4 + @counter] & @ls[45 + @counter]
      n209 = @ls[6 + @counter] & @ls[64 + @counter]
      n205 = @ls[5 + @counter] & @ls[80 + @counter]
      n201 = @ls[8 + @counter] & @ls[103 + @counter]
      n197 = @ls[29 + @counter] & @ls[52 + @counter] & @ls[72 + @counter] & @ls[99 + @counter]
      n193 = @ls[12 + @counter] & @ls[121 + @counter]

      if(init)
          n255 ^= out
          n217 ^= out
      end

      # Update State
      @counter += 1

      @ls[255 + @counter] = n255
      @ls[251 + @counter] ^= n251
      @ls[247 + @counter] ^= n247
      @ls[243 + @counter] ^= n243
      @ls[239 + @counter] ^= n239
      @ls[235 + @counter] ^= n235
      @ls[231 + @counter] ^= n231
      @ls[217 + @counter] ^= n217
      @ls[213 + @counter] ^= n213
      @ls[209 + @counter] ^= n209
      @ls[205 + @counter] ^= n205
      @ls[201 + @counter] ^= n201
      @ls[197 + @counter] ^= n197
      @ls[193 + @counter] ^= n193

      # ??? (Copied from Original Test Vector, Maybe for Dynamic Array?)
      if(@counter == 1700)
          # Some memcpy (memcpy(ls, ls+1700, 256);)
          @counter = 0
      end

      return out
    end

end

# Set Key and IV
key = []
iv = []
  
(0..15).each do |i|
  key.push(i)
end
  
(0..11).each do |i|
  iv.push(i)
end

esp = Espresso.new(key, iv)
puts esp.ls

ky = []

(0..159).each do |i|
  ky.insert(i, esp.update(false))
end

keystream = ""
kp = ""

ky.each{
  |x| 
  kp += x.to_s

  if (kp.length == 8)
    kp = kp.reverse
    keystream += "%02x" % kp.to_i(2)
    kp = ""
  end
}

puts keystream
