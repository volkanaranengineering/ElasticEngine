model SpringDischarge
  parameter Real J = 1 "kg.m2";
  parameter Real k = 10 "N.m/rad";
  parameter Real b = 1 "N.m.s/rad; dissipative test load";
  Real theta(start=1, fixed=true);
  Real omega(start=0, fixed=true);
  Real delivered(start=0, fixed=true);
  Real stored;
  Real kinetic;
  Real residual;
equation
  der(theta) = omega;
  J*der(omega) = -k*theta-b*omega;
  der(delivered) = b*omega^2;
  stored = 0.5*k*theta^2;
  kinetic = 0.5*J*omega^2;
  residual = stored+kinetic+delivered-0.5*k;
end SpringDischarge;
