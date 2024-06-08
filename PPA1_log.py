def binary_with_fraction_to_decimal_list(binary_list):
    decimals = []

    for binary in binary_list:
        # Extract sign bit
        sign_bit = (binary >> (len(bin(binary)) - 1)) & 1

        # Extract integer part from binary (3 bits)
        integer_part = (binary >> 16) & 0b111

        # Extract fractional part from binary (16 bits)
        fractional_part = 0
        for i in range(1, 17):
            fractional_part += ((binary >> (16 - i)) & 1) * (2 ** (-i))

        # Combine integer and fractional parts and apply sign
        decimal = (-1) ** sign_bit * (integer_part + fractional_part)
        decimals.append(decimal)

    return decimals

#####################################

def binary_with_fraction_to_decimal(binary,width):
    sign_bit = int(binary[0])
    integer_bits = int(binary[1:4], 2)
    fractional_bits = int(binary[4:width+4], 2)
    
    # Calculate the decimal value of the fractional part
    fractional_decimal = 0
    for i in range(1, width+1):
        if (fractional_bits >> (width - i)) & 1:
            fractional_decimal += 2**(-i)

    # Combine the integer and fractional parts
    decimal_value = (-1)**sign_bit * (integer_bits + fractional_decimal)
    return decimal_value


#########################################

def decimal_to_binary_with_fraction(decimal,width):
    # Convert decimal to binary
    sign_bit = '0' if decimal >= 0 else '1'
    integer_part, fractional_part = str(decimal).split('.')
    integer_part = int(integer_part)
    fractional_part = float('.' + fractional_part)
    
    # Convert integer part to binary (3 bits)
    binary_integer = bin(abs(integer_part))[2:].zfill(3)
    
    # Convert fractional part to binary (16 bits)
    binary_fractional = ''
    for _ in range(width):
        fractional_part *= 2
        bit = '1' if fractional_part >= 1 else '0'
        binary_fractional += bit
        fractional_part -= int(bit)
    
    return sign_bit + binary_integer + binary_fractional

 ################################################


def decimal_to_binary_with_fraction_1(decimals):
    binary_list = []
    
    for decimal in decimals:
        # Convert decimal to binary
        sign_bit = '0' if decimal >= 0 else '1'
        integer_part, fractional_part = str(decimal).split('.')
        integer_part = int(integer_part)
        fractional_part = float('.' + fractional_part)
        
        # Convert integer part to binary (3 bits)
        binary_integer = bin(abs(integer_part))[2:].zfill(3)
        
        # Convert fractional part to binary (16 bits)
        binary_fractional = ''
        for _ in range(16):
            fractional_part *= 2
            bit = '1' if fractional_part >= 1 else '0'
            binary_fractional += bit
            fractional_part -= int(bit)
        
        binary_list.append(sign_bit + binary_integer + binary_fractional)
    
    return binary_list

##################################

def decimal_to_binary_with_fraction_widths(decimals, fraction_widths):
    binary_list = []
    num_decimals = len(decimals)
    num_widths = len(fraction_widths)
    
    # Repeat widths list if it's shorter than the number of decimals
    repeated_widths = fraction_widths * (num_decimals // num_widths) + fraction_widths[:num_decimals % num_widths]
    
    for decimal, width in zip(decimals, repeated_widths):
        # Convert decimal to binary
        sign_bit = '0' if decimal >= 0 else '1'
        integer_part, fractional_part = str(decimal).split('.')
        integer_part = int(integer_part)
        fractional_part = float('.' + fractional_part)
        
        # Convert integer part to binary
        binary_integer = bin(abs(integer_part))[2:].zfill(4 // 2)
        
        # Convert fractional part to binary with width specified for each row
        binary_fractional = ''
        for _ in range(width):
            fractional_part *= 2
            bit = '1' if fractional_part >= 1 else '0'
            binary_fractional += bit
            fractional_part -= int(bit)
        
        binary_list.append(sign_bit + '0'+binary_integer + binary_fractional)
    
    return binary_list    

#######################################

import math 

def PPA1_log(x,fraction_widths):
    coefficient_int = [0.000214924853328684,
1.40776335535059,
0.0706723763432590,
1.34066473832866,
0.141126673693050,
1.27676030195531,
0.211593009445442,
1.21589730900399,
0.282058384406928,
1.15793681336772,
0.352521808172931,
1.10274386048771,
0.422975233194979,
1.05018272642888,
0.493435720726808,
1.00012483603920,
0.563895049920418,
0.952453792617057,
0.634353124241739,
0.907058133252488,
0.704802590815256,
0.863827623769104,
0.775255640367575,
0.822654717320116,
0.845714810250803,
0.783442393092801,
0.916176043809805,
0.746098576304478,
0.986427800552374,
0.724750659757040]
    
    sp_int =[0.0,
0.0500495918211643,
0.102601663233387,
0.157793545433738,
0.215747310597391,
0.276600289921416,
0.340489814602884,
0.407583733882658,
0.478034637979706,
0.552010376134890,
0.629678797589075,
0.711238269626917,
0.796887159533074,
0.886823834592203,
0.981261921110857]

    coefficients = decimal_to_binary_with_fraction_widths(coefficient_int, fraction_widths)
    # print((coefficients[3]))
    sp_bin = decimal_to_binary_with_fraction_1(sp_int)

    coefficient=[]
    coefficient = [[x for x in coefficients[i:i+2]] for i in range(0, len(coefficient_int), 2)]
    
    sp=[]
    sp = [[x for x in sp_bin]]
    
    for coef in coefficient:
        print(coef)
    for sp in sp:
        print(sp)
    # coefficient = [
    #     [0b00010000000010101010, 0b00001110111111101101, 0b00001011100001000111],
    #     [0b00100000011111010000, 0b00011111001101000000, 0b00010101101101110010],
    #     [0b00111001011011110101, 0b00110111111001010110, 0b00100100101000100100],
    #     [0b01011100110011011011, 0b01011100001110110000, 0b00110100011100110110]
    # ]
    # sp = [
    #     0b00000000000000000000,
    #     0b00001011010100000000,
    #     0b00010100011100000000,
    #     0b00011100001000000000
    # ]
    
    
    # comparator = [0] * 4
    # for i in range(4):
    #     comparator[i] = 1 if x >= sp[i] else 0

    comparator = [0] * 15
    # sp_int=[0]*4
    for i in range(15):
        #sp_int[i] = binary_with_fraction_to_decimal(sp[i])  # Convert each element of sp from binary string to integer
        comparator[i] = 1 if x >= sp_int[i] else 0

    i = 0 if (comparator[0] == 0) else (1 if (comparator[1] == 0) else (2 if (comparator[2] == 0) else (3 if (comparator[3] == 0) else (4 if (comparator[4] == 0) else (5 if (comparator[5] == 0) else (6 if (comparator[6] == 0) else (7 if (comparator[7] == 0) else (8 if (comparator[8] == 0) else (9 if (comparator[9] == 0) else (10 if (comparator[10] == 0) else (11 if (comparator[11] == 0) else (12 if (comparator[12] == 0) else (13 if (comparator[13] == 0) else (14 if (comparator[14] == 0) else 15))))))))))))))

    # comparator = [0] * 4
    # sp_int=[0]*4
    # for i in range(4):
    #     #sp_int[i] = binary_with_fraction_to_decimal(sp[i])  # Convert each element of sp from binary string to integer
    #     comparator[i] = 1 if x >= sp_int[i] else 0
       
    # i = 0 if (comparator[0]  == 0) else (1 if (comparator[1]  == 0) else (1 if (comparator[2]  == 0) else (3 if (comparator[3]  == 0) else 3)))
    print(f'{comparator}')
    #i = next((index for index, val in enumerate(comparator, start=1) if val == 0), 0)

    print(f'i {i}')
    a_bin = coefficient[i-1][1]
    b_bin = coefficient[i-1][0]
    z_bin = sp[i-1]
    print(f'a_bin {a_bin} b_bin {b_bin} z_bin  {z_bin}')
    a = (binary_with_fraction_to_decimal(a_bin,fraction_widths[1]))
    b = (binary_with_fraction_to_decimal(b_bin,fraction_widths[0]))
    z = (binary_with_fraction_to_decimal(z_bin,16))
    print(f'a {a} b {b} z {z}')
    #print(type(a))
# P1 = (a >> (width - 1)) << (2 * (width - 1))
# M1 = (P1 >> (2 * (width - 1))) << (width - 1)
 
   # P1_mul = a[0] * (x[0] - z[0])
    P1_int = a*(x-z)
    print(f'P1_int= { P1_int}')
    print(type(P1_int))
    # Pn = int(decimal_to_binary_with_fraction(P1_int))
    # print(f'Pn= { Pn}')
    # print(type(Pn))
    P1 =(decimal_to_binary_with_fraction(P1_int,fraction_widths[0]))
    print(f'P1= { P1}')
    print(type(P1))
   
    M1 = binary_with_fraction_to_decimal(P1,fraction_widths[0])
    print(f'M1= { M1}')
    A1_int = M1+b
    print(f'A1_int= { A1_int}')
    A1 = (decimal_to_binary_with_fraction(A1_int,16))
    print(f'A1= { A1}')
    # A_final = A1.zfill(20)
    y = A1_int

    return y 

x=0.9
fraction_widths = [16, 16]
ans = PPA1_log(x,fraction_widths)
result = math.log(1+x,2)
print(f'result {result}')
print (ans)
##################################



    

