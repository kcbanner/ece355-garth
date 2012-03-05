filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  Component.SensorController("SensorController")();
  Component.SystemController("SystemController")();
  Component.AlarmController("AlarmController")();
  Component.Outputs("Outputs")();
  Component.Sensors("Sensors")();
  Component.SensorOS("Sensor OS")();
  Component.EventHandling("Event Handling")();
  Component.CommProtocol("Communications Protocol")();
  Component.HardwareInterface("Hardware Interface")();
  Component.ExternalInterface("External Interface")();
  
  topToBottom(60)(
      SystemController,
      EventHandling,
      CommProtocol,
      HardwareInterface);

  topToBottom(60)(
      ExternalInterface,
      SystemController);

  topToBottom(60)(
      AlarmController,
      Outputs);
  
  topToBottom(60)(
      SensorController,
      Sensors,
      SensorOS);
  
  leftToRight(40)(
      SensorController,
      SystemController,
      AlarmController);
  
  drawObjects(
      SensorController,
      SystemController,
      AlarmController,
      Outputs,
      Sensors,
      SensorOS,
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
  
  link(requiredInterface)(SystemController.n -- .5[SystemController.n,
      ExternalInterface.s]);
  link(providedInterface)(ExternalInterface.s -- .5[ExternalInterface.s,
      SystemController.n]);  
  
endfig;

end