filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  Actor.Resident("Resident");

  ClassName.Keypad("Keypad");
  classStereotypes.Keypad("<<boundary>>");  
  
  ClassName.Sensor("DoorSensor");
  classStereotypes.Sensor("<<boundary>>");

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
  
  leftToRight(40)(
      Resident,
      Keypad,
      Sensor,
      SensorController,
      SystemController,
      AlarmController);

  placeholderY := -400;
  
  A.midx = Resident.midx;
  A.midy = placeholderY;
  B.midx = Keypad.midx;
  B.midy = placeholderY;
  C.midx = Sensor.midx;
  C.midy = placeholderY;
  D.midx = SensorController.midx;
  D.midy = placeholderY;
  E.midx = SystemController.midx;
  E.midy = placeholderY;
  F.midx = AlarmController.midx;
  F.midy = placeholderY;
  
  drawObjects(
      Resident,
      Keypad,
      Sensor,     
      SensorController,
      SystemController,
      AlarmController,
      A,
      B,
      C,
      D,
      E,
      F);

  % Resident opens door
  item(iAssoc)("generateSensorEvent()")(obj.sw = (30, -70));
  link(associationUni)((Resident.human.midx, -70) -- (Sensor.midx, -70));
  
  % generateSensorEvent()
  item(iAssoc)("handleEvent(SensorEvent)")(obj.sw = (210, -100));
  link(associationUni)((Sensor.midx, -100) -- (SensorController.midx, -100));

  % handleEvent()
  item(iAssoc)("handleEvent(SensorEvent)")(obj.sw = (330, -130));
  link(associationUni)((SensorController.midx, -130) -- (SystemController.midx, -130));

  % handleEvent()
  item(iAssoc)("handleEvent(Minor AlarmEvent)")(obj.sw = (440, -160));
  link(associationUni)((SystemController.midx, -160) -- (AlarmController.midx, -160));

  % Resident types code using Keypad
  item(iAssoc)("generateKeypadEvent()")(obj.sw = (30, -190));
  link(associationUni)((Resident.human.midx, -190) -- (Keypad.midx, -190));

  % handleEvent()
  item(iAssoc)("handleEvent()")(obj.sw = (130, -220));
  link(associationUni)((Keypad.midx, -220) -- (SystemController.midx, -220));

  % stopAlarms()
  item(iAssoc)("stopAlarms()")(obj.sw = (470, -250));
  link(associationUni)((SystemController.midx, -250) -- (AlarmController.midx, -250));
  
  clink(dashedLink)(Resident.human, A);
  clink(dashedLink)(Keypad, B);
  clink(dashedLink)(Sensor, C);
  clink(dashedLink)(SensorController, D);
  clink(dashedLink)(SystemController, E);
  clink(dashedLink)(AlarmController, F);
  
endfig;

end
