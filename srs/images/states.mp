filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  
  State.Armed("Armed")();
  State.Disarmed("Disarmed")();
  State.MinorAlarm("MinorAlarm")();
  State.MajorAlarm("MajorAlarm")();
  State.CriticalAlarm("CriticalAlarm")();

  topToBottom(80)(
      MinorAlarm,
      MajorAlarm,
      CriticalAlarm);
  topToBottom(80)(
      Disarmed,
      Armed);
  leftToRight(200)(
      Disarmed,
      MinorAlarm);
  
  drawObjects(
      Armed,
      Disarmed,
      MinorAlarm,
      MajorAlarm,
      CriticalAlarm);

  item(iAssoc)("stopAlarms()")(obj.sw = (130, 100));
  item(iAssoc)("handleEvent(MinorAlarm)")(obj.sw = (110, 80));

  item(iAssoc)("armSystem()")(obj.sw = (-20, 30));
  item(iAssoc)("disarmSystem()")(obj.sw = (30, 30));

  item(iAssoc)("handleEvent(MajorAlarm)")(obj.sw = (300, 30));
  item(iAssoc)("handleEvent(CriticalAlarm)")(obj.sw = (300, -80));

  item(iAssoc)("stopAlarms()")(obj.sw = (190, 30));
  item(iAssoc)("stopAlarms()")(obj.sw = (190, -40));
  
  % Bi-directional transitions
  link(transition)((Armed.midx + 5, Armed.top) -- (Disarmed.midx + 5, Disarmed.bottom));
  link(transition)((Disarmed.midx - 5, Disarmed.bottom) -- (Armed.midx - 5, Armed.top));

  link(transition)((MinorAlarm.left, MinorAlarm.midy + 5) -- (Disarmed.right, Disarmed.midy + 5));
  link(transition)((Disarmed.right, Disarmed.midy - 5) -- (MinorAlarm.left, MinorAlarm.midy - 5));
  
  clink(transition)(Armed, MinorAlarm);
  clink(transition)(MinorAlarm, MajorAlarm);
  clink(transition)(MajorAlarm, CriticalAlarm);
  clink(transition)(MajorAlarm, Disarmed);
  clink(transition)(CriticalAlarm, Disarmed);
  
endfig;

end