% plot_waves_inverse.m
% x points to the right
% y points to the top
% angles are measured from the positive x-axis, CCW positive
%
% specify change in robot position, calculate change in pseudorange

clear all;

% satellites bearing and range
psi1 = 40*pi/180;
psi2 = -60*pi/180;
R = 20000000;   % orbit radius is 20,000 km

% satellite locations
sx1 = R*cos(psi1);
sy1 = R*sin(psi1);

sx2 = R*cos(psi2);
sy2 = R*sin(psi2);

% initial robot location
rx0 = 0;
ry0 = 0;

% final robot location
rx1 = -10;
ry1 = 20;

% defining some variables for convenience 
dx1 = rx0-sx1;
dy1 = ry0-sy1;

dx2 = rx0-sx2;
dy2 = ry0-sy2;

drx1 = rx1-rx0;
dry1 = ry1-ry0;

% unit vectors describing direction of from satellites to robot location
% j1_i is the unit vector direction from satellite 1 to the robot expressed
% in inertial coordinates. i1_i normal to j1_i and aligned with the wave
% front. Inertial coordinates are i_i is east, j_i is north. Angles are
% positive CCW from i_i.
i1_i = [dy1/R; -dx1/R];
j1_i = [dx1/R; dy1/R];

i2_i = [dy2/R; -dx2/R];
j2_i = [dx2/R; dy2/R];

% calculate angle between wave fronts (alpha)
alpha = acos(i1_i'*i2_i);

%%% calculate change in pseudorange %%%
A = [-dy2 dy1; dx2 -dx1];
del_p_vec = R*sin(alpha)*inv(A)*[drx1; dry1];
del_p1 = del_p_vec(1);
del_p2 = del_p_vec(2);

%%% plot the scenario %%%
% calculate slope and intercept
m1 = -dx1/dy1;
m2 = -dx2/dy2;

c1 = del_p1/R * (dy1 + dx1^2/dy1);
c2 = del_p2/R * (dy2 + dx2^2/dy2);

% field boundaries
xmax = 20;
xmin = -20;
ymax = 20;
ymin = -20;

% x values for plotting lines
xpts1 = 2*[2*xmax; 2*xmin];
xpts2 = 2*[2*xmax; 2*xmin];

% calculate y values based on equation for line
ypts1_0 = m1*xpts1;
ypts1_1 = m1*xpts1 + c1;

ypts2_0 = m2*xpts2;
ypts2_1 = m2*xpts2 + c2;

figure(1); clf;
plot(xpts1,ypts1_0,'LineWidth',2,'Color',[0 0.45 0.74]); hold on;
plot(xpts1,ypts1_1,'LineWidth',2,'Color',[0 0.45 0.74]); 
axis(3*[xmin xmax ymin ymax]);
axis('square'); grid;
plot(xpts2,ypts2_0,'LineWidth',2,'Color',[0.87 0.49 0]);
plot(xpts2,ypts2_1,'LineWidth',2,'Color',[0.87 0.49 0]);

%%% predict the robot's new location %%%

% calculate change in robot position based on changes is pseudoranges
del_pos = del_p2/(sin(alpha))*i1_i - del_p1/(sin(alpha))*i2_i;

% calculating del_rx and del_rx
del_rx = del_pos(1);
del_ry = del_pos(2);

% plotting new robot position
plot(rx0,ry0,'ko',rx0+del_rx,ry0+del_ry,'mo');
hold off;
