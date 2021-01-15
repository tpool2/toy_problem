% plot_waves.m
% x points to the right
% y points to the top
% angles are measured from the positive x-axis, CCW positive

clear all;

% satellites bearing and range
psi1 = -80*pi/180;
psi2 = -80*pi/180;
psi3 = -40*pi/180;
R = 20000000;   % orbit radius is 20,000 km

% satellite locations
sx1 = R*cos(psi1);
sy1 = R*sin(psi1);

sx2 = R*cos(psi2);
sy2 = R*sin(psi2);

sx3 = R*cos(psi3);
sy3 = R*sin(psi3);

% initial robot location
rx0 = 0; 
ry0 = 0;

% change in pseudorange
del_p1 = 10;
del_p2 = 25;
del_p3 = 26;

% defining some variables for convenience 
dx1 = rx0-sx1;
dy1 = ry0-sy1;

dx2 = rx0-sx2;
dy2 = ry0-sy2;

dx3 = rx0-sx3;
dy3 = ry0-sy3;

%%% plot the scenario %%%

% unit vectors describing direction of from satellites to robot location
% j1_i is the unit vector direction from satellite 1 to the robot expressed
% in inertial coordinates. i1_i normal to j1_i and aligned with the wave
% front. Inertial coordinates are i_i is east, j_i is north. Angles are
% positive CCW from i_i.
i1_i = [dy1/R; -dx1/R];
j1_i = [dx1/R; dy1/R];

i2_i = [dy2/R; -dx2/R];
j2_i = [dx2/R; dy2/R];

i3_i = [dy3/R; -dx3/R];
j3_i = [dx3/R; dy3/R];

% calculated another way
th1 = atan2(-dx1,dy1);
th2 = atan2(-dx2,dy2);
th3 = atan2(-dx3,dy3);

i1_ia = [cos(th1); sin(th1)];
j1_ia = [-sin(th1); cos(th1)];

i2_ia = [cos(th2); sin(th2)];
j2_ia = [-sin(th2); cos(th2)];

i3_ia = [cos(th3); sin(th3)];
j3_ia = [-sin(th3); cos(th3)];

% calculate slope and intercept
m1 = -dx1/dy1;
m1a = i1_ia(2)/i1_ia(1);
m2 = -dx2/dy2;
m2a = i2_ia(2)/i2_ia(1);
m3 = -dx3/dy3;
m3a = i3_ia(2)/i3_ia(1);

c1 = del_p1/R * (dy1 + dx1^2/dy1);
c2 = del_p2/R * (dy2 + dx2^2/dy2);
c3 = del_p3/R * (dy3 + dx3^2/dy3);

% field boundaries
xmax = 20;
xmin = -20;
ymax = 20;
ymin = -20;

% x values for plotting lines
xpts1 = 2*[2*xmax; 2*xmin];
xpts2 = 2*[2*xmax; 2*xmin];
xpts3 = 2*[2*xmax; 2*xmin];

% calculate y values based on equation for line
ypts1_0 = m1*xpts1;
ypts1_1 = m1*xpts1 + c1;

ypts2_0 = m2*xpts2;
ypts2_1 = m2*xpts2 + c2;

ypts3_0 = m3*xpts3;
ypts3_1 = m3*xpts3 + c3;

figure(1); clf;
plot(xpts1,ypts1_0,'LineWidth',2,'Color',[0 0.45 0.74]); hold on;
plot(xpts1,ypts1_1,'LineWidth',2,'Color',[0 0.45 0.74]); 
axis(3*[xmin xmax ymin ymax]);
axis('square'); grid;
plot(xpts2,ypts2_0,'LineWidth',2,'Color',[0.87 0.49 0]);
plot(xpts2,ypts2_1,'LineWidth',2,'Color',[0.87 0.49 0]);
plot(xpts3,ypts3_0,'LineWidth',2,'Color',[0.75 0.75 0]);
plot(xpts3,ypts3_1,'LineWidth',2,'Color',[0.75 0.75 0]);

%%% predict the robot's new location %%%

% calculate angle between wave fronts (alpha)
alpha = acos(i1_i'*i2_i);

% calculate change in robot position based on changes is pseudoranges
del_pos = del_p2/(sin(alpha))*i1_i - del_p1/(sin(alpha))*i2_i;

% % calculating del_rx and del_rx
% del_rx = del_pos(1);
% del_ry = del_pos(2);
% 
% % plotting new robot position
% plot(rx0,ry0,'ko',rx0+del_rx,ry0+del_ry,'mo');
% hold off;

% instead of using geometry to find robot position, try minimizing an error
% function

B = 2*(m1-m2)*(c1-c2) + 2*(m1-m3)*(c1-c3) + 2*(m2-m3)*(c2-c3);
A = (m1-m2)^2 + (m1-m3)^2 + (m2-m3)^2;

rx_min = -B/(2*A);
ry_min = mean([m1*rx_min + c1; m2*rx_min + c2; m3*rx_min + c3]);

[xint12,yint12] = calc_intersect(m1,c1,m2,c2);
[xint13,yint13] = calc_intersect(m1,c1,m3,c3);
[xint23,yint23] = calc_intersect(m2,c2,m3,c3);

xmn = mean([xint12,xint13,xint23]);
ymn = mean([yint12,yint13,yint23]);

% plotting new robot position
plot(rx0,ry0,'ko',rx_min,ry_min,'mo',xmn,ymn,'r*');
hold off;



