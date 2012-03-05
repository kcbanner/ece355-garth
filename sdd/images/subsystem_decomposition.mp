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
  
  link(association)(pathManhattanY(SensorController.s, .75[EventHandling.n,
        SystemController.s]));
  link(association)(pathManhattanY(AlarmController.s, .75[EventHandling.n,
        SystemController.s]));

  link(providedInterface)(AlarmController.w + (0, 10) -- .5[AlarmController.w + (0, 10), SystemController.e + (0, 10)]);
  link(requiredInterface)(SystemController.e + (0, 10) -- .5[SystemController.e + (0, 10), AlarmController.w + (0, 10)]);

  link(requiredInterface)(AlarmController.w - (0, 10) -- .5[AlarmController.w - (0, 10), SystemController.e - (0, 10)]);
  link(providedInterface)(SystemController.e - (0, 10) -- .5[SystemController.e - (0, 10), AlarmController.w - (0, 10)]);
  
  link(providedInterface)(SensorController.e + (0, 10) -- .5[SensorController.e + (0, 10), SystemController.w + (0, 10)]);
  link(requiredInterface)(SystemController.w + (0, 10) -- .5[SystemController.w + (0, 10), SensorController.e + (0, 10)]);

  link(requiredInterface)(SensorController.e - (0, 10) -- .5[SensorController.e - (0, 10), SystemController.w - (0, 10)]);
  link(providedInterface)(SystemController.w - (0, 10) -- .5[SystemController.w - (0, 10), SensorController.e - (0, 10)]);
  
  link(providedInterface)(Outputs.n + (20, 0) -- .5[Outputs.n + (20, 0),
      AlarmController.s + (20, 0)]);
  link(requiredInterface)(AlarmController.s + (20, 0) -- .5[AlarmController.s + (20, 0) , Outputs.n + (20, 0) ]);
  
  link(providedInterface)(Sensors.n - (20, 0) -- .5[Sensors.n - (20, 0),
      SensorController.s - (20, 0)]);
  link(requiredInterface)(SensorController.s - (20, 0) -- .5[SensorController.s - (20, 0), Sensors.n - (20, 0)]);
  
  link(providedInterface)(SensorOS.n -- .5[SensorOS.n,
      Sensors.s]);
  link(requiredInterface)(Sensors.s -- .5[Sensors.s,
      SensorOS.n]);

  link(providedInterface)(EventHandling.n -- .5[EventHandling.n,
      SystemController.s]);
  link(requiredInterface)(SystemController.s -- .5[SystemController.s,
      EventHandling.n]);
  
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