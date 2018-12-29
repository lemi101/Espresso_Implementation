class Espresso
    def initialize(key, iv)
      @key = key
      @iv = iv
      @counter = 0
      @ls = Array.new(2000)
  
  
    end
  
    def update(init)
      
    end
  
  end
  
  key = []
  
  (0..15).each do |i|
    key.push(i)
  end
  
  iv = []
  
  (0..11).each do |i|
    iv.push(i)
  end
  
  esp = Espresso.new(key, iv)
  
  ks = []
  
  (0..19).each do |i|
    ks.push(0)
  end

