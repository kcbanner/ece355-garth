filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  Class.ExternalServer("ExternalServer")
    ()
    ("+logEvent(event: Event): void",
      "+handleExternalAlarmEvent(event: AlarmEvent)");

  drawObjects(
      ExternalServer
      );
  
endfig;

end
