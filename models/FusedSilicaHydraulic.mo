model FusedSilicaHydraulic
  extends BareGlassHydraulic(E=72e9,rho=2200);
  annotation(Documentation(info="High-purity fused-silica candidate; Astroquartz manufacturer modulus/density. Peak stress remains a scenario, not a dry-bundle fatigue allowable. Protective surface sizing is not excluded by absence of bulk epoxy matrix."));
end FusedSilicaHydraulic;
