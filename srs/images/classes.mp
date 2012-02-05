filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  Class.Controller("Controller")
    ()
    ("+handleEvent(event): void");

  Controller.nw = (0, 0);
  classStereotypes.Controller("<<interface>>");

  Class.SensorController("SensorController")
    ()
    ("+subscribeToEvent(event_type): void");

  SensorController.n = Controller.s - (0, 50);
  
  drawObjects(Controller);
  drawObjects(SensorController);

  link(association)(Controller.s -- SensorController.n);
  
endfig;

end
