filenametemplate "%j%c.mps";
input metauml;

beginfig(1);
    Begin.b;
    State.Armed("Armed")();
    State.Disarmed("Disarmed")();
    End.e;

    leftToRight(20)(
        b,
        Armed,
        Disarmed,
        e);

endfig;
end;
