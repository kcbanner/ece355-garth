filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  Class.Controller("Controller")
    ()
    ("-pollSensor(sensorId: int)",
      "+handleEvent(event: Event): void",
      "+subscribeToEvent(eventType: EventType): void");

  classStereotypes.Controller("<<interface>>");

  Class.SensorController("SensorController")
    ()
    ("-handleSensorInput(event: SensorEvent)",
      "-pollSensor(sensorId: int)");

  Class.SystemController("SystemController")
    ()
    ("-logEventToServer(event: Event)",
      "-handleNFCInput(event: NFCEvent)",
      "-handleKeypadInput(event: KeypadEvent)");
  
  Class.AlarmController("AlarmController")
    ()
    ("-handleCriticalAlarm(event: AlarmEvent)",
      "-handleMajorAlarm(event: AlarmEvent)",
      "-handleMinor(event: AlarmEvent)");
  
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
    ("+CriticalAlarm",
      "+MajorAlarm",
      "+MinorAlarm")
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
    ("+inputDeviceId: int")
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
      FloodSensorEvent);
  
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

beginfig(3);
  Class.Sensor("Sensor")
    ("-sensorId: int")
    ("+getSensorId(): int",
      "+generateSensorEvent(): SensorEvent");

  classStereotypes.Sensor("<<interface>>");

  Class.DoorSensor("DoorSensor")
    ("-doorId: int")
    ("+getDoorId(): int");

  Class.WindowSensor("WindowSensor")
    ("-windowId: int")
    ("+getWindowId(): int");

  Class.FloodSensor("FloodSensor")
    ("-lastWaterHeight: int",)
    ("+getWaterHeight(): int");
  
  Class.TempSensor("TempSensor")
    ("-lastTemperature: int",)
    ("+getTemperature(): int");

  Class.MotionSensor("MotionSensor")
    ("-motionThreshold: int")
    ("+setMotionThreshold(threshold: int): void");

  leftToRight.top(20)(
      DoorSensor,
      WindowSensor,
      FloodSensor,
      TempSensor,
      MotionSensor);
  topToBottom(50)(
      Sensor,
      FloodSensor);
  
  drawObjects(
      Sensor,
      DoorSensor,
      WindowSensor,
      FloodSensor,
      TempSensor,
      MotionSensor);
  
  stepY := -20;
  stepX := 60;

  link(inheritance)(pathStepY(
        Sensor.s,
        DoorSensor.n,
        stepY));
  link(inheritance)(pathStepY(
        Sensor.s,
        WindowSensor.n,
        stepY));
  link(inheritance)(pathStepY(
        Sensor.s,
        FloodSensor.n,
        stepY));
  link(inheritance)(pathStepY(
        Sensor.s,
        TempSensor.n,
        stepY));
  link(inheritance)(pathStepY(
        Sensor.s,
        MotionSensor.n,
        stepY));

  
endfig;

beginfig(4);
  Class.InputDevice("InputDevice")
    ("-deviceId: int")
    ();

  classStereotypes.Sensor("<<interface>>");

  Class.KeypadInputDevice("KeypadInputDevice")
    ()
    ("-generateKeypadEvent(): KeypadEvent");

  Class.NFCReaderInputDevice("NFCReaderInputDevice")
    ()
    ("-generateNFCEvent(): NFCEvent");

  leftToRight.top(20)(
      KeypadInputDevice,
      NFCReaderInputDevice);
  topToBottom(50)(
      InputDevice,
      KeypadInputDevice);
  
  drawObjects(
      InputDevice,
      KeypadInputDevice,
      NFCReaderInputDevice);
  
  stepY := -20;
  stepX := 60;
  
  link(inheritance)(pathStepY(
        InputDevice.s,
        KeypadInputDevice.n,
        stepY));
  link(inheritance)(pathStepY(
        InputDevice.s,
        NFCReaderInputDevice.n,
        stepY));
  
endfig;

beginfig(5);
  Class.AlarmDevice("AlarmDevice")
    ("-deviceId: int")
    ();

  classStereotypes.AlarmDevice("<<interface>>");

  Class.SirenAlarm("SirenAlarm")
    ("-activated:boolean")
    ("setActivated(activated: boolean): void");

  Class.SpeechAlarm("SpeechAlarm")
    ("-message:String", "-repeat:boolean")
    ("+playMessage(message: String, repeat: boolean): void",
      "+stopPlaying(): void");

  Class.SMSAlarm("SMSAlarm")
    ()
    ("+sendMessage(phoneNumber: String, message: String): void");

  Class.ExternalAlarm("ExternalAlarm")
    ()
    ("+externalAlarm(externalURL: String, alarmEvent: AlarmEvent): void");
  
  leftToRight.top(20)(
      SirenAlarm,
      SpeechAlarm);
  leftToRight.top(20)(
      SMSAlarm,
      ExternalAlarm);
  topToBottom(50)(
      AlarmDevice,
      SpeechAlarm,
      ExternalAlarm);

  drawObjects(
      AlarmDevice,
      SirenAlarm,
      SpeechAlarm,
      SMSAlarm,
      ExternalAlarm);
  
  stepY := -20;
  stepX := 60;
  
  link(inheritance)(pathStepY(
        AlarmDevice.s,
        SirenAlarm.n,
        stepY));
  link(inheritance)(pathStepY(
        AlarmDevice.s,
        SpeechAlarm.n,
        stepY));
  link(inheritance)(pathStepY(
        AlarmDevice.s,
        SMSAlarm.n - (50, 0),
        stepY));
  link(inheritance)(pathStepY(
        AlarmDevice.s,
        ExternalAlarm.n + (140, 0),
        stepY));
  
endfig;
  
end
