filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  ClassName.Sensor("Sensor");
  classStereotypes.Sensor("<<boundary>>");

  ClassName.EventManager("EventManager");
  
  ClassName.CommunicationsInterface("CommunicationsInterface");

  ClassName.HardwareInterface("HardwareInterface");

  ClassName.SensorController("SensorController");
  classStereotypes.SensorController("<<control>>");
  
  % Placeholder
  ClassName.A("");
  ClassName.B("");
  ClassName.C("");
  ClassName.D("");
  ClassName.E("");
  
  leftToRight(20)(
      Sensor,
      EventManager,
      CommunicationsInterface,
      HardwareInterface,
      SensorController);

  placeholderY := -400;
  
  A.midx = Sensor.midx;
  A.midy = placeholderY;
  B.midx = EventManager.midx;
  B.midy = placeholderY;
  C.midx = CommunicationsInterface.midx;
  C.midy = placeholderY;
  D.midx = HardwareInterface.midx;
  D.midy = placeholderY;
  E.midx = SensorController.midx;
  E.midy = placeholderY;
  
  drawObjects(
      Sensor,
      EventManager,
      CommunicationsInterface,
      HardwareInterface,
      SensorController,
      A,
      B,
      C,
      D,
      E);

  item(iAssoc)("broadcastEvent()")(obj.sw = (Sensor.midx, -70));
  link(associationUni)((Sensor.midx, -70) -- (EventManager.midx, -70));
  
  item(iAssoc)("broadcastData()")(obj.sw = (EventManager.midx, -100));
  link(associationUni)((EventManager.midx, -100) -- (CommunicationsInterface.midx, -100));

  item(iAssoc)("sendBytes()")(obj.sw = (CommunicationsInterface.midx, -130));
  link(associationUni)((CommunicationsInterface.midx, -130) -- (HardwareInterface.midx, -130));

  item(iAssoc)("packetReceived()")(obj.se = (HardwareInterface.midx, -160));
  link(associationUni)((HardwareInterface.midx, -160) -- (CommunicationsInterface.midx, -160));

  item(iAssoc)("eventReceived()")(obj.se = (CommunicationsInterface.midx, -190));
  link(associationUni)((CommunicationsInterface.midx, -190) -- (EventManager.midx, -190));

  item(iAssoc)("handleSensorInput()")(obj.sw = (EventManager.midx, -220));
  link(associationUni)((EventManager.midx, -220) -- (SensorController.midx, -220));  
  
  clink(dashedLink)(Sensor, A);
  clink(dashedLink)(EventManager, B);
  clink(dashedLink)(CommunicationsInterface, C);
  clink(dashedLink)(HardwareInterface, D);
  clink(dashedLink)(SensorController, E);
  
endfig;

end
