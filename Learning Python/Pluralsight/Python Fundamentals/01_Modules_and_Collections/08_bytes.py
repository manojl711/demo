# Converting between strings and bytes
# From str - bytes, use encode
# From bytes - str, use decode

# bytes - used for raw binary data and fixed with single byte char encodings such as ASCII
# there is also a bytes constructor which is advanced feature

d = b'some bytes'
print(d)
print(d.split())

# Python supports a wide variety of encodings
# Pangrams eg.
# The five boxing wizards jump quickly
# Pack my box with five dozen liquor jugs
# The quick brown fox jumps over the lazy dog
# Jinxed wizards pluck ivy from the big quilt
# Crazy Fredrick bought many very exquisite opal jewels
# We promptly judged antique ivory buckles for the next prize.
# A mad boxer shot a quick, gloved jab to the jaw of his dizzy opponent
# The job requires extra pluck and zeal from every young wage earner

mysentence = 'Det er så hyggelig å treffe deg'  # I am very glad to meet you
print(mysentence)

data = mysentence.encode('utf-8')  # str - bytes
print(data)

# while decoding we must apply the correct decoding
norwegian = data.decode('utf-8')  # bytes - str
print(norwegian)

# Remember: File, Network resources and HTTP responses are transmitted using byte streams
