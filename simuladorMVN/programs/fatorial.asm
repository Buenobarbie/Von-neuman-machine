@ /0000
JP MAIN


@ /0100
N   K =4
RES K =0
UM  K =1

MAIN LD N
    SC FATORIAL
    HM /0000

FATORIAL K /0000
    JZ NZERO
    LOOP MM RES
    LD N
    SB UM 
    JZ FIM 
    MM N
    ML RES 
    JP LOOP
    JP FIM
    NZERO LD UM 
    MM RES
FIM RS FATORIAL