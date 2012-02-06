filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  Class.Controller("Controller")
    ()
    ("+handleEvent(event): void",
     "+subscribeToEvent(event_type): void");

  classStereotypes.Controller("<<interface>>");

  Class.SensorController("SensorController")
    ()
    ("+registerSensor(): int");

  Class.SystemController("SystemController")
    ()
    ();
  
  Class.AlarmController("AlarmController")
    ()
    ();
  
  leftToRight.top(20)(
      SensorController,
      SystemController,
      AlarmController);
  topToBottom(50)(Controller, SystemController);
  
  drawObjects(
      Controller,
      SensorController,
      SystemController,
      AlarmController);

  stepY := -20;
  stepX := 60;
  
  link(inheritance)(pathStepY(
        Controller.s,
        SensorController.n,
        stepY));
  link(inheritance)(pathStepY(
        Controller.s,
        SystemController.n,
        stepY));
  link(inheritance)(pathStepY(
        Controller.s,
        AlarmController.n,
        stepY));
  
endfig;

beginfig(2);
  Class.EventType("EventType")
    ("+DoorSensorEvent",
      "+WindowSensorEvent",
      "+FloodSensorEvent",
      "+TempSensorEvent",
      "+AlarmEvent",
      "+KeypadEvent",
      "+NFCEvent")
    ();
  EventType.info.iMethodStack.top := 0;
  EventType.info.iMethodStack.bottom := 0;
  classStereotypes.EventType("<<enumeration>>");

  Class.AlarmSeverity("AlarmSeverity")
    ("+ExternalAlarm",
      "+InternalAlarm",
      "+Notification")
    ();
  AlarmSeverity.info.iMethodStack.top := 0;
  AlarmSeverity.info.iMethodStack.bottom := 0;
  classStereotypes.AlarmSeverity("<<enumeration>>");
  
  Class.Event("Event")
    ("+type:EventType",
      "+timestamp:int")
    ();    
  classStereotypes.Event("<<interface>>");

  Class.AlarmEvent("AlarmEvent")
    ("+severity:AlarmSeverity",
      "+description:String",
      "+speechMessage:String")
    ();
  
  Class.SensorEvent("SensorEvent")
    ("+sensorId:int")
    ();
  classStereotypes.SensorEvent("<<interface>>");

  Class.InputEvent("InputEvent")
    ()
    ();
  classStereotypes.InputEvent("<<interface>>");

  Class.KeypadEvent("KeypadEvent")
    ("+input:char")
    ();

  Class.NFCEvent("NFCEvent")
    ("+data:String")
    ();
  
  Class.DoorSensorEvent("DoorSensorEvent")
    ("+doorId:int",
      "+opened:boolean")
    ();

  Class.WindowSensorEvent("WindowSensorEvent")
    ("+windowId:int",
      "+opened:boolean")
    ();

  Class.FloodSensorEvent("FloodSensorEvent")
    ("+waterHeight:int",
      "+delta:int")
    ();

  Class.TempSensorEvent("TempSensorEvent")
    ("+temperature:int",
      "+delta:int")
    ();
  
  leftToRight.top(20)(SensorEvent, AlarmEvent, InputEvent);
  leftToRight.top(20)(
      DoorSensorEvent,
      WindowSensorEvent,
      FloodSensorEvent,
      TempSensorEvent,
      KeypadEvent,
      NFCEvent);
  leftToRight.bottom(20)(Event, EventType, AlarmSeverity);
  topToBottom(50)(
      Event,
      AlarmEvent,
      TempSensorEvent);
  
  drawObjects(
      Event,
      EventType,
      AlarmSeverity,
      SensorEvent,
      AlarmEvent,
      InputEvent,
      DoorSensorEvent,
      WindowSensorEvent,
      FloodSensorEvent,
      TempSensorEvent,
      KeypadEvent,
      NFCEvent);
  
  stepY := -20;
  stepX := 60;

  % link(association)(Event.e -- EventType.w);
  
  link(inheritance)(pathStepY(
        Event.s,
        SensorEvent.n,
        stepY));
  link(inheritance)(pathStepY(
        Event.s,
        AlarmEvent.n,
        stepY));
  link(inheritance)(pathStepY(
        Event.s,
        InputEvent.n,
        stepY));
  link(inheritance)(pathStepY(
        SensorEvent.s,
        DoorSensorEvent.n,
        stepY));
  link(inheritance)(pathStepY(
        SensorEvent.s,
        WindowSensorEvent.n,
        stepY));
  link(inheritance)(pathStepY(
        SensorEvent.s,
        FloodSensorEvent.n,
        stepY));
  link(inheritance)(pathStepY(
        SensorEvent.s,
        TempSensorEvent.n,
        stepY));
  link(inheritance)(pathStepY(
        InputEvent.s,
        KeypadEvent.n,
        stepY));
  link(inheritance)(pathStepY(
        InputEvent.s,
        NFCEvent.n,
        stepY));
  
endfig;

end
