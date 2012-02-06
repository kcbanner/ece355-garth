filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
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
  
  leftToRight(100)(
      Sensor,
      SensorController,
      SystemController,
      AlarmController);

  A.midx = Sensor.midx;
  A.midy = -400;
  B.midx = SensorController.midx;
  B.midy = -400;
  C.midx = SystemController.midx;
  C.midy = -400;
  D.midx = AlarmController.midx;
  D.midy = -400;
  
  drawObjects(
      Sensor,
      SensorController,
      SystemController,
      AlarmController,
      A,
      B,
      C,
      D);

  % generateSensorEvent()
  item(iAssoc)("generateSensorEvent()")(obj.sw = (80, -70));
  link(associationUni)((Sensor.midx, -70) -- (SensorController.midx, -70));
  
  clink(dashedLink)(Sensor, A);
  clink(dashedLink)(SensorController, B);
  clink(dashedLink)(SystemController, C);
  clink(dashedLink)(AlarmController, D);
  
endfig;

end