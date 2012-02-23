filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  ClassName.EventHandling("Event Handling");
  ClassName.CommProtocol("Communications Protocol");
  ClassName.HardwareInterface("Hardware Interface");

  topToBottom(40)(
      EventHandling,
      CommProtocol,
      HardwareInterface);
  
  drawObjects(
      EventHandling,
      CommProtocol,
      HardwareInterface);

  link(associationUni)(EventHandling.s -- CommProtocol.n);
  link(associationUni)(CommProtocol.s -- HardwareInterface.n);
  
endfig;

end
