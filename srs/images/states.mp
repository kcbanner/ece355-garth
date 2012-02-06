filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  
  Begin.b;
  State.Armed("Armed")();
  State.Disarmed("Disarmed")();
  State.MinorAlarm("MinorAlarm")();
  State.MajorAlarm("MajorAlarm")();
  State.CriticalAlarm("CriticalAlarm")();

  topToBottom(40)(
      MinorAlarm,
      MajorAlarm,
      CriticalAlarm);
  topToBottom(40)(
      Disarmed,
      Armed);
  leftToRight(40)(
      b,
      Disarmed,
      MinorAlarm);
  
  drawObjects(
      b,
      Armed,
      Disarmed,
      MinorAlarm,
      MajorAlarm,
      CriticalAlarm);

  clink(transition)(b, Disarmed);
  clink(transition)(Armed, Disarmed);
  clink(transition)(Disarmed, Armed);
  clink(transition)(Armed, MinorAlarm);
  clink(transition)(MinorAlarm, MajorAlarm);
  clink(transition)(MajorAlarm, CriticalAlarm);
  clink(transition)(Disarmed, MinorAlarm);
  clink(transition)(MinorAlarm, Disarmed);
  clink(transition)(MajorAlarm, Disarmed);
  clink(transition)(CriticalAlarm, Disarmed);
  
endfig;

end