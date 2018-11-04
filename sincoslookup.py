import math


# sin function fast lookup table (0 - 359 degrees)
sinLookupTbl = [math.sin(math.radians(x)) for x in range(360)]
# cos functions fast lookup table (0 - 359 degrees)
cosLookupTbl = [math.cos(math.radians(x)) for x in range(360)]
