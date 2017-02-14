a = csvread('Winter_EV_Profiles.csv')


a = a*ones(100,1)

a = [a(49:end);a(1:48)]

plot(a)