filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  Component.EventHandling("Event Handling")();
  Component.CommProtocol("Communications Protocol")();
  Component.HardwareInterface("Hardware Interface")();
  Component.ExternalInterface("External Interface")();
  
  topToBottom(40)(
      ExternalInterface,
      EventHandling,
      CommProtocol,
      HardwareInterface);

  drawObjects(
      EventHandling,
      CommProtocol,
      HardwareInterface,
      ExternalInterface);

  link(providedInterface)(HardwareInterface.n -- .5[HardwareInterface.n,
      CommProtocol.s]);
  link(requiredInterface)(CommProtocol.s -- .5[CommProtocol.s,
      HardwareInterface.n]);

  link(providedInterface)(CommProtocol.n -- .5[CommProtocol.n,
      EventHandling.s]);
  link(requiredInterface)(EventHandling.s -- .5[EventHandling.s,
      CommProtocol.n]);  

  link(providedInterface)(EventHandling.n -- .5[EventHandling.n,
      ExternalInterface.s]);
  link(requiredInterface)(ExternalInterface.s -- .5[ExternalInterface.s,
      EventHandling.n]);  
  
endfig;

end