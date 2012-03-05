filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  ClassName.EventProtocol("Event Protocol");
  ClassName.CommProtocol("Communications Protocol");
  ClassName.HardwareInterface("Hardware Interface");

  topToBottom(40)(
      EventProtocol,
      CommProtocol,
      HardwareInterface);
  
  drawObjects(
      EventProtocol,
      CommProtocol,
      HardwareInterface);

  link(associationUni)(EventProtocol.s -- CommProtocol.n);
  link(associationUni)(CommProtocol.s -- HardwareInterface.n);
  
endfig;

end