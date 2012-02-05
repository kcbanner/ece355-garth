filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  Class.A("A")
    ("attr1: int", "attr2: int")
    ("method1(): void", "method2(): int");

  A.nw = (0, 0);
  drawObjects(A);

endfig;
end