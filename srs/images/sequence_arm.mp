filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  Actor.Resident("Resident");

  ClassName.Keypad("Keypad");
  classStereotypes.Keypad("<<boundary>>");  
  
  ClassName.Sensor("Sensor");
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

  % 1. item() adds the text
  % 2. link(associationUni) adds the line
  % 3. Space the Y coords by -30 (next will be -100, then -130, etc)
  % 4. fiddle with the text X coord
  
  item(iAssoc)("generateSensorEvent()")(obj.sw = (30, -70));
  link(associationUni)((Resident.human.midx, -70) -- (Sensor.midx, -70));
  
  clink(dashedLink)(Resident.human, A);
  clink(dashedLink)(Keypad, B);
  clink(dashedLink)(Sensor, C);
  clink(dashedLink)(SensorController, D);
  clink(dashedLink)(SystemController, E);
  clink(dashedLink)(AlarmController, F);

endfig;

end