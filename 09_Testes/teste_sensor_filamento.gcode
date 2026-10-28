; Teste de sensor de movimento de filamento
; Extrusa 50 mm no ar, longe da mesa (Z=50), sem deixar residuo na chapa
; Duracao ~30 s a F100

G28
G90
M83
G1 Z50 F600
G1 X130 Y80 F3000
M118 TESTE FILAMENTO - inicio
G1 E50 F100
G1 E-2 F600
M118 TESTE FILAMENTO - fim
