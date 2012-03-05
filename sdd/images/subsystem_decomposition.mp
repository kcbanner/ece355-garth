filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  Component.SensorController("SensorController")();
  Component.SystemController("SystemController")();
  Component.AlarmController("AlarmController")();
  Component.Inputs("Inputs")();
  Component.Outputs("Outputs")();
  Component.Sensors("Sensors")();
  
  Component.CommunicationsStack("Communications Stack")(
      EventProtocol,
      CommProtocol,
      HardwareInterface);
  
  Component.EventProtocol("Event Protocol")();
  Component.CommProtocol("Communications Protocol")();
  Component.HardwareInterface("Hardware Interface")();
  Component.ExternalInterface("External Interface")();
  
  topToBottom(60)(
      EventProtocol,
      CommProtocol,
      HardwareInterface);

  topToBottom(60)(
      ExternalInterface,
      SystemController,
      CommunicationsStack);
  
  leftToRight(60)(
      Sensors,
      CommunicationsStack,
      Outputs);

  Inputs.s = Outputs.n + (0, 30);
  
  leftToRight(40)(
      SensorController,
      SystemController,
      AlarmController);
  
  drawObjects(
      SensorController,
      SystemController,
      AlarmController,
      Inputs,
      Outputs,
      Sensors,
      CommunicationsStack,
      ExternalInterface);
  
  link(association)(pathManhattanY(SensorController.s, .75[CommunicationsStack.n,
        SystemController.s]));
  link(association)(pathManhattanY(AlarmController.s, .75[CommunicationsStack.n,
        SystemController.s]));
  
  link(requiredInterface)(Inputs.w -- .5[Inputs.w, CommunicationsStack.e + (0, 61)]);
  link(providedInterface)(CommunicationsStack.e + (0, 61) -- .5[Inputs.w, CommunicationsStack.e + (0, 61)]);

  link(requiredInterface)(Outputs.w -- .5[Outputs.w, CommunicationsStack.e]);
  link(providedInterface)(CommunicationsStack.e -- .5[Outputs.w, CommunicationsStack.e]);

  link(requiredInterface)(Sensors.e -- .5[Sensors.e, CommunicationsStack.w]);
  link(providedInterface)(CommunicationsStack.w -- .5[Sensors.e, CommunicationsStack.w]);  

  link(providedInterface)(CommunicationsStack.n -- .5[CommunicationsStack.n,
      SystemController.s]);
  link(requiredInterface)(SystemController.s -- .5[SystemController.s,
      CommunicationsStack.n]);
  
  link(providedInterface)(HardwareInterface.n -- .5[HardwareInterface.n,
      CommProtocol.s]);
  link(requiredInterface)(CommProtocol.s -- .5[CommProtocol.s,
      HardwareInterface.n]);

  link(providedInterface)(CommProtocol.n -- .5[CommProtocol.n,
      EventProtocol.s]);
  link(requiredInterface)(EventProtocol.s -- .5[EventProtocol.s,
      CommProtocol.n]);  
  
  link(requiredInterface)(SystemController.n -- .5[SystemController.n,
      ExternalInterface.s]);
  link(providedInterface)(ExternalInterface.s -- .5[ExternalInterface.s,
      SystemController.n]);
  
endfig;

end