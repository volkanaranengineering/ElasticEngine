model BareGlassHydraulic
  parameter Real peakStress=1e9 "Pa scenario input, NOT a qualified working allowable";
  extends TensionHydraulic(
    E=86.9e9, rho=2460, L=100, area=0.005,
    strain0=peakStress/E, mode=1);
  annotation(Documentation(info="Aligned bare S-2 glass fibres, no epoxy matrix. Area is solid glass only. Assumes perfect load sharing and lossless elastic recovery. Terminations and long-duration bundle strength are unqualified."));
end BareGlassHydraulic;
