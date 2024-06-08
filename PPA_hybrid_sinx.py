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
        
        binary_list.append(sign_bit + '0'+ binary_integer + binary_fractional)
    
    return binary_list    

#######################################


import math 
def PPA_hybrid_sinx(x,combined_fraction_widths):

    fraction_widths = combined_fraction_widths[:3]
    fraction_widths1 = combined_fraction_widths[3:]

    coefficient_int = [-1.38969368784555e-05,1.00180303809062,-0.0346608520878083,
                        0.138380195244790,0.992171770706222,-0.103546222855846,
                        0.274991166192216,0.963216482665988,-0.171082833823530,
                        0.407967791923376,0.914729985941142,-0.236326691900638,
                        0.535365318905679,0.846302570913861,-0.298262142616927,
                        0.655035998865252,0.757209333609685,-0.355753099203657,
                        0.764528313635175,0.646105287552906,-0.407444261026624,
                        0.860760383691764,0.510388681417401,-0.451557531933264,
                        0.939389638802240,0.344010121212614,-0.485304779411492,
                        0.992138485152333,0.125247741018008,-0.498812356378983]
    
    coefficient_int1 = [1.38997265948326e-05,0.999045605652702,
                        0.0756404684767055,0.994976082273178,
                        0.122710132067811,0.991055904557702,
                        0.138407993264794,0.987540094576632,
                        0.175582338713714,0.981293525636010,
                        0.208957888381137,0.974477718170707,
                        0.239648173936725,0.967176845344251,
                        0.268270394711140,0.960846139577210
                        ]


    sp_int = [0.00	,0.138839721679688,	0.278594970703125,	0.420242309570313,
              0.564956665039063,	0.714248657226563,	0.870330810546875	,1.03678894042969,	1.22088623046875,	1.44532775878906]
    sp_int1 =[0.00,0.0756988525390625	,0.123016357421875, 0.138839721679688	,0.176483154296875,	0.210494995117188,	0.241989135742188,	0.271591186523438]

    coefficients = decimal_to_binary_with_fraction_widths(coefficient_int, fraction_widths)
    coefficients1 = decimal_to_binary_with_fraction_widths(coefficient_int1, fraction_widths1)
    # print((coefficients[3]))
    sp_bin = decimal_to_binary_with_fraction_1(sp_int)
    sp_bin1 = decimal_to_binary_with_fraction_1(sp_int1)

    coefficient=[]
    coefficient = [[x for x in coefficients[i:i+3]] for i in range(0, len(coefficient_int), 3)]
    
    coefficient1=[]
    coefficient1 = [[y for y in coefficients1[k:k+2]] for k in range(0, len(coefficient_int1), 2)]

    sp=[]
    sp = [[x for x in sp_bin]]
    
    sp1=[]
    sp1 = [[y for y in sp_bin1]]

    for coef in coefficient:
        print(coef)
    for sp in sp:
       pass
  
    for coef1 in coefficient1:
        print(coef1)
    for sp1 in sp1:
         pass
    


   
    comparator = [0] * 10
    # sp_int=[0]*3
    for i in range(10):
        comparator[i] = 1 if x >= sp_int[i] else 0


    i = 0 if comparator[0] == 0 else \
    (1 if comparator[1] == 0 else \
    (2 if comparator[2] == 0 else \
    (3 if comparator[3] == 0 else \
    (4 if comparator[4] == 0 else \
    (5 if comparator[5] == 0 else \
    (6 if comparator[6] == 0 else \
    (7 if comparator[7] == 0 else \
    (8 if comparator[8] == 0 else \
    (9 if comparator[9] == 0 else 9)))))))))

    print(f'comparator {comparator}')
    comparator1 = [0] * 8
    # sp_int1=[0]*1
    for j in range(8):
        comparator1[j] = 1 if x >= sp_int1[j] else 0
    j = 0 if comparator1[0] == 0 else \
    (1 if comparator1[1] == 0 else \
    (2 if comparator1[2] == 0 else \
    (3 if comparator1[3] == 0 else \
    (4 if comparator1[4] == 0 else \
    (5 if comparator1[5] == 0 else \
    (6 if comparator1[6] == 0 else \
    (7 if comparator1[7] == 0 else \
    8)))))))


    print(f'i {i}')
    print(f'j {j}')
    flag = 1 if ((i<=9) and (i>=2)) else 0
    print(f'flag {flag}')
    a_bin = coefficient[i-1][2] if (flag==1) else None
    b_bin = coefficient[i-1][1] if (flag==1) else None
    c_bin = coefficient[i-1][0] if (flag==1) else None
    z_bin = sp[i-1] if (flag==1) else None
    print(f'a_bin {a_bin} b_bin {b_bin} c_bin {c_bin} z_bin  {z_bin}')
    a = (binary_with_fraction_to_decimal(a_bin,fraction_widths[2])) if (flag==1) else None
    b = (binary_with_fraction_to_decimal(b_bin,fraction_widths[1])) if (flag==1) else None
    c = (binary_with_fraction_to_decimal(c_bin, fraction_widths[0])) if (flag==1) else None
    z = (binary_with_fraction_to_decimal(z_bin,16)) if (flag==1) else None
    print(f'a {a} b {b} c {c} z {z}')
    #print(type(a))
   

    a_bin1 = coefficient1[j-1][1] if (flag==0) else None
    b_bin1 = coefficient1[j-1][0] if (flag==0) else None
    z_bin1 = sp1[j-1] if (flag==0) else None
    print(f'a_bin1 {a_bin1} b_bin1 {b_bin1} z_bin1  {z_bin1}')
    a1 = (binary_with_fraction_to_decimal(a_bin1,fraction_widths1[1])) if (flag==0) else None
    b1 = (binary_with_fraction_to_decimal(b_bin1,fraction_widths1[0])) if (flag==0) else None
    z1 = (binary_with_fraction_to_decimal(z_bin1,16)) if (flag==0) else None
    print(f'a1 {a1} b1 {b1} z1 {z1}') if (flag==0) else None

    P1_decimal = (a*(x-z)) if (flag==1) else (a1*(x-z1))
    print(f'P1_int= { P1_decimal}')
    print(type(P1_decimal))
    P1_int ="{:.20f}".format(P1_decimal)
    print(f'P1_int= { P1_int}')
  

    # Pn = int(decimal_to_binary_with_fraction(P1_int))
    # print(f'Pn= { Pn}')
    # print(type(Pn))
    P1 =decimal_to_binary_with_fraction(float(P1_int),(fraction_widths[1] if flag==1 else fraction_widths1[0]))
    print(f'P1= { P1}')
    print(type(P1))
    M1 = binary_with_fraction_to_decimal(P1,(fraction_widths[1] if flag==1 else fraction_widths1[0]))
    print(f'M1= { M1}')
    A1_int = M1+b if flag == 1 else M1+b1
    print(f'A1_int= { A1_int}')
    A1 = decimal_to_binary_with_fraction(A1_int,(fraction_widths[1] if flag==1 else fraction_widths1[0]))
    print(f'A1= { A1}')
    A11 = (decimal_to_binary_with_fraction(A1_int, 16))
    A1_int1 = binary_with_fraction_to_decimal(A1,(fraction_widths[1] if flag==1 else fraction_widths1[0]))
    print(f'A1_int1= { A1_int1}')
   # P2_mul = A1_int1*(x-z)
    P2_int =  A1_int1*(x-z) if flag == 1 else None
    print(f'P2_int= { P2_int}')
    P2 = decimal_to_binary_with_fraction(P2_int,fraction_widths[0]) if flag == 1 else None
    print(f'P2= { P2}')
    M2 = binary_with_fraction_to_decimal(P2,fraction_widths[0]) if flag == 1 else None
    print(f'M2= { M2}')
    A2_int = M2+c if flag == 1 else None
    print(f'A2_int= { A2_int}')
    A2 = (decimal_to_binary_with_fraction(float(A2_int),16)) if flag == 1 else None
    print(f'A2= { A2}')
    A_final = A2.zfill(20) if flag == 1 else None
    A1_final = A11.zfill(20)
    y = A2 if flag ==1 else A1
    decimal = binary_with_fraction_to_decimal(y,16)
    return decimal 

#############################

x=0.0
#fraction_widths = [16,16,16,16,16]
#ans = PPA_hybrid_sinx(x,fraction_widths)
result = (math.sin(x))
print(f'{x}\t{result}\tresult')
#print(f'{result}     result')
#print (f'{x}\t{ans}\tans')
    
