filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  Class.Controller("Controller")
    ()
    ("+handleEvent(event): void");

  classStereotypes.Controller("<<interface>>");

  Class.SensorController("SensorController")
    ()
    ("+subscribeToEvent(event_type): void");

  Class.SafetyController("SafetyController")()();
  Class.SecurityController("SecurityController")()();
  Class.EnergyController("EnergyController")()();
  
  leftToRight(20)(
      SensorController,
      SafetyController,
      SecurityController,
      EnergyController);
  topToBottom(50)(Controller, SafetyController);
  
  drawObjects(
      Controller,
      SensorController,
      SafetyController,
      SecurityController,
      EnergyController);

  stepY := -20;
  stepX := 60;
  
  link(inheritance)(pathStepY(
        Controller.s,
        SensorController.n,
        stepY));
  link(inheritance)(pathStepY(
        Controller.s,
        SafetyController.n,
        stepY));
  link(inheritance)(pathStepY(
        Controller.s,
        SecurityController.n,
        stepY));
  link(inheritance)(pathStepY(
        Controller.s,
        EnergyController.n,
        stepY));
  
endfig;

end
