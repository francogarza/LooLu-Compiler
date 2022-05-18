import semanticCube as sc

sc.cube('INT','FLOAT','*',1,1)
sc.cube('BOOL','FLOAT','-',1,1)
sc.cube('BOOL','INT','&&',1,1)
sc.cube('CHAR','CHAR','-',2,0)
sc.cube('CHAR','CHAR','/',0,2)
sc.cube('INT','BOOL','>',1,1)
sc.cube('INT','BOOL','<>',2,2)
sc.cube('INT','BOOLa','*',1,1)
