model CarbonTorsionPlant
  parameter Integer n=20 "Sequential cartridges per lane";
  parameter Integer lanes=10;
  parameter Real P=10000 "W electrical output per lane";
  parameter Real duration=180 "s each cartridge supplies nominal output";
  parameter Real eLab=2.1e6 "J/kg laboratory loading-energy reference, not a plant rating";
  parameter Real scale=0.5 "retained specific energy after scale-up";
  parameter Real twistFraction=0.7 "fraction of laboratory twist; quadratic surrogate";
  parameter Real etaRope=0.9;
  parameter Real etaCollection=0.9 "captures coupled axial/torsional work and transmission";
  parameter Real etaGenerator=0.95;
  parameter Real etaConverter=0.98;
  parameter Real retention=0.95 "assumed remaining energy after 1 h idle";
  parameter Real reserve=0.10 "minimum fraction of no-load remaining energy after final discharge";
  parameter Real eta=etaRope*etaCollection*etaGenerator*etaConverter;
  parameter Real lambda=-log(retention)/3600;
  parameter Real E0=P/eta/lambda*(exp(lambda*duration)-1)*exp(lambda*(n-1)*duration)/(1-reserve);
  parameter Real cartridgeMass=E0/(eLab*scale*twistFraction^2);
  parameter Real activeMass=lanes*n*cartridgeMass;
  Real E[n](each start=E0,each fixed=true);
  Real electricalPower, stored, availableRatio;
  Real delivered(start=0,fixed=true);
  Real conversionLoss(start=0,fixed=true);
  Real relaxationLoss(start=0,fixed=true);
  Real residual;
equation
  for j in 1:n loop
    der(E[j])=-lambda*E[j]-(if time>=(j-1)*duration and time<j*duration then P/eta else 0);
  end for;
  electricalPower=if time<n*duration then lanes*P else 0;
  stored=lanes*sum(E);
  availableRatio=min(E)/E0;
  der(delivered)=electricalPower;
  der(conversionLoss)=electricalPower*(1/eta-1);
  der(relaxationLoss)=lambda*stored;
  residual=stored+delivered+conversionLoss+relaxationLoss-lanes*n*E0;
end CarbonTorsionPlant;
