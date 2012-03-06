filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
  Class.ExternalServer("ExternalServer")
    ()
    ("+logEvent(event: Event): void",
      "+initiateBackup(): void",
      "+initiateRemoteAdministration(): void",
      "+handleExternalAlarmEvent(event: AlarmEvent)");

  drawObjects(
      ExternalServer
      );
  
endfig;

end
