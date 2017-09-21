% 1 = 1 ms
% 1 below 50 bpm
% 1 above 100 bpm
% normal 80 bpm 80 beats in 60000

%normal section 750 two beats (80 bpm)
norm_base = ones(675,1);
norm_peak = 2.5*ones(75,1);
normY = cat(1,norm_base,norm_peak);

%slow dying section 1500 two beats (50 bpm)
brady_base = ones(1425,1);
bradyY = cat(1,brady_base,norm_peak);

%fast dying section 500 two beats (120 bpm)
tachy_base = ones(425,1);
tachyY = cat(1,tachy_base,norm_peak);

%30s living time
normal_sec = normY;
for i = 2:1:40
    normal_sec = cat(1,normal_sec,normY);
end

%15s slow and fast dying
brady_sec = bradyY;
for i = 2:1:10
    brady_sec = cat(1,brady_sec,bradyY);
end

tachy_sec = tachyY;
for i = 2:1:30
    tachy_sec = cat(1,tachy_sec,tachyY);
end

M = zeros(120000,2);
M(:,1) = linspace(0,120,120000);
M(:,2) = cat(1,normal_sec,brady_sec,normal_sec,tachy_sec,normal_sec);
figure(1); clf
plot(M(:,1),M(:,2));
M2 = zeros(240000,2);
M2(:,1) = linspace(0,240,240000);
M2(:,2) = cat(1,M(:,2),M(:,2));

cd('C:\Users\User\Documents');
fid = fopen('full_test.csv','w+');
fprintf(fid, '%s,', 'TIMES');
fprintf(fid, '%s\n', 'VOLTAGES');
fclose(fid);
dlmwrite('full_test.csv',M2,'-append');