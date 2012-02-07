filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  Actor.Resident("Resident");

  ClassName.Keypad("Keypad");
  classStereotypes.Keypad("<<boundary>>");  
  
  ClassName.SpeechAlarm("SpeechAlarm");
  classStereotypes.SpeechAlarm("<<boundary>>");
    
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
  ClassName.G("");
  
  leftToRight(30)(
      Resident,
      Keypad,
      SpeechAlarm,
      Sensor,
      SensorController,
      SystemController,
      AlarmController);

  placeholderY := -400;
  
  A.midx = Resident.midx;
  A.midy = placeholderY;
  B.midx = Keypad.midx;
  B.midy = placeholderY;
  C.midx = SpeechAlarm.midx;
  C.midy = placeholderY;
  D.midx = Sensor.midx;
  D.midy = placeholderY;
  E.midx = SensorController.midx;
  E.midy = placeholderY;
  F.midx = SystemController.midx;
  F.midy = placeholderY;
  G.midx = AlarmController.midx;
  G.midy = placeholderY;

  
  drawObjects(
      Resident,
      Keypad,
      SpeechAlarm,
      Sensor,     
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

  % 1. item() adds the text
  % 2. link(associationUni) adds the line
  % 3. Space the Y coords by -30 (next will be -100, then -130, etc)
  % 4. fiddle with the text X coord
 
  % Resident uses keypad
  item(iAssoc)("generateKeyPadEvent()")(obj.sw = (30, -70)); 
  link(associationUni)((Resident.human.midx, -70) -- (Keypad.midx, -70));

  % handleEvent()
  item(iAssoc)("handleEvent(KeypadEvent)")(obj.sw = (210, -100));
  link(associationUni)((Keypad.midx, -100) -- (SystemController.midx, -100));

  % handleEvent()
  item(iAssoc)("handleEvent(AlarmEvent)")(obj.sw = (400, -130));
  link(associationUni)((SystemController.midx, -130) -- (AlarmController.midx, -130));

  % playMessage()
  item(iAssoc)("playMessage('System Armed', true)")(obj.sw = (330, -160));
  link(associationUni)((AlarmController.midx, -160) -- (SpeechAlarm.midx, -160));
    
  % generateSensorEvent()
  item(iAssoc)("generateSensorEvent()")(obj.sw = (60, -190));
  link(associationUni)((Resident.human.midx, -190) -- (Sensor.midx, -190));

  % handleEvent()
  item(iAssoc)("handleEvent(SensorEvent)")(obj.sw = (270, -210));
  link(associationUni)((Sensor.midx, -210) -- (SystemController.midx, -210));

  % stopAlarms()
  item(iAssoc)("stopAlarms()")(obj.sw = (400, -240));
  link(associationUni)((SystemController.midx, -240) -- (AlarmController.midx, -240));

  % stopPlaying()
  item(iAssoc)("stopPlaying()")(obj.sw = (330, -270));
  link(associationUni)((AlarmController.midx, -270) -- (SpeechAlarm.midx, -270));

  %item(iAssoc)("
  % item(iAssoc)("generateSensorEvent()")(obj.sw = (30, -70));
  % link(associationUni)((Resident.human.midx, -70) -- (Sensor.midx, -70));
  
  clink(dashedLink)(Resident.human, A);
  clink(dashedLink)(Keypad, B);
  clink(dashedLink)(SpeechAlarm, C);
  clink(dashedLink)(Sensor, D);
  clink(dashedLink)(SensorController, E);
  clink(dashedLink)(SystemController, F);
  clink(dashedLink)(AlarmController, G);

endfig;

end
