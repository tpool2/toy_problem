function [xint,yint] = calc_intersect(m1,b1,m2,b2)

xint = (b2-b1)/(m1-m2);
yint = m1*(b2-b1)/(m1-m2) + b1;

end

