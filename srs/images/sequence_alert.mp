filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  Actor.NonResident("NonResident");
  
  ClassName.Sensor("WindowSensor");
  classStereotypes.Sensor("<<boundary>>");
  
  ClassName.SMSAlert("SMSAlert");
  classStereotypes.SMSAlert("<<boundary>>");
 
  ClassName.ExternalAlert("ExternalAlert");
  classStereotypes.ExternalAlert("<<boundary>>");

  ClassName.SensorController("SensorController");
  classStereotypes.SensorController("<<control>>");

  ClassName.SystemController("SystemController");
  classStereotypes.SystemController("<<control>>");
  
  ClassName.AlarmController("AlarmController");
  classStereotypes.AlarmController("<<control>>");

  % Placeholder
  ClassName.A("");
  ClassName.B("");
  ClassName.C("");
  ClassName.D("");
  ClassName.E("");
  ClassName.F("");
  ClassName.G("");
  
  leftToRight(20)(
      NonResident,
      Sensor,
      SMSAlert,
      ExternalAlert,
      SensorController,
      SystemController,
      AlarmController);

  placeholderY := -400;
  
  A.midx = NonResident.midx;
  A.midy = placeholderY;
  B.midx = Sensor.midx;
  B.midy = placeholderY;
  C.midx = SMSAlert.midx;
  C.midy = placeholderY;
  D.midx = ExternalAlert.midx;
  D.midy = placeholderY;
  E.midx = SensorController.midx;
  E.midy = placeholderY;
  F.midx = SystemController.midx;
  F.midy = placeholderY;
  G.midx = AlarmController.midx;
  G.midy = placeholderY;
  
  drawObjects(
      NonResident,
      Sensor,     
      SMSAlert,
      ExternalAlert,
      SensorController,
      SystemController,
      AlarmController,
      A,
      B,
      C,
      D,
      E,
      F,
      G);

  % Resident opens door
  item(iAssoc)("generateSensorEvent()")(obj.sw = (40, -70));
  link(associationUni)((NonResident.human.midx, -70) -- (Sensor.midx, -70));
  
  % generateSensorEvent()
  item(iAssoc)("handleEvent(SensorEvent)")(obj.sw = (170, -100));
  link(associationUni)((Sensor.midx, -100) -- (SensorController.midx, -100));

  % handleEvent()
  item(iAssoc)("handleEvent(SensorEvent)")(obj.sw = (380, -130));
  link(associationUni)((SensorController.midx, -130) -- (SystemController.midx, -130));

  % handleEvent()
  item(iAssoc)("handleEvent(Major AlarmEvent)")(obj.sw = (480, -150));
  link(associationUni)((SystemController.midx, -160) -- (AlarmController.midx, -160));
  % 190
  
  % sendSMSMessage()
  item(iAssoc)("sendMessage(Phone #, 'Window Alert Msg')")(obj.sw = (220, -210));
  link(associationUni)((AlarmController.midx, -210) -- (SMSAlert.midx, -210));

  item(iAssoc)("externalAlarm(URL, Major AlarmEvent)")(obj.sw = (300, -240));
  link(associationUni)((AlarmController.midx, -240) -- (ExternalAlert.midx, -240));
  % 210
  % 240
  %
  clink(dashedLink)(NonResident.human, A);
  clink(dashedLink)(Sensor, B);
  clink(dashedLink)(SMSAlert, C);
  clink(dashedLink)(ExternalAlert,D);
  clink(dashedLink)(SensorController, E);
  clink(dashedLink)(SystemController, F);
  clink(dashedLink)(AlarmController, G);
  
endfig;

end
