clc ; close all;clear all
N = 4; K = 5;

%% 1.  Plot Tian v.s. Yu.
Ned = min(K, N); % distinct files in demand d

% Tian-Chen
figure
t_axis = 0:K;
M_Tian = t_axis.*((N-1)*t_axis+K-N)/K/(K-1);
R_Tian =  N*(K-t_axis)/K;
plot(M_Tian, R_Tian, 'k--d', 'Linewidth', 1)
hold on

% Yu et al
t_axis = 0:K-1;
M_Yu = t_axis*N/K;
R_Yu = zeros(size(t_axis)); 
for iR = 1:length(t_axis)
    if K - Ned >= t_axis(iR)+1
        R_Yu(iR) = (nchoosek(K, t_axis(iR)+1) - nchoosek(K - Ned, t_axis(iR)+1)) / nchoosek(K,t_axis(iR));
    else
        R_Yu(iR) = nchoosek(K, t_axis(iR)+1) / nchoosek(K, t_axis(iR));
    end
end
M_Yu = [M_Yu, N];
R_Yu = [R_Yu, 0];
plot(M_Yu, R_Yu, 'r-x', 'Linewidth', 1) 
%legend('Tian','Yu')

% Chen scheme
M_Chen = 1/K;
R_Chen = N - N/K;
plot(M_Chen, R_Chen, 'ro') 

% Jesus 1st Scheme
g = 1:N;
M_Jesus_1 = N/K./g;
R_Jesus_1 = N - N/K*(N+1)./(g+1);
plot(M_Jesus_1, R_Jesus_1, 'g-x', 'Linewidth', 1) 
%legend('Gomez-Vilardebo Scheme 1')

% Jesus New Scheme
s = 1;
M_Jesus_2(1) = 0;
R_Jesus_2(1) = N;

for r = 1:K-s
    M_Jesus_2(r+1) = s/K + (N-1)*s/K*r/(K-s) + N*r/K;
    R_Jesus_2(r+1) = (K*func_mynchoosek(K-s, r+1) - func_findRedanduncy(N,K,r)) / (K*nchoosek(K-s,r));
%     R_Jesus_2(r+1) = (K*func_mynchoosek(K-s, r+1)) / (K*nchoosek(K-s,r));
end
plot(M_Jesus_2, R_Jesus_2, 'b-o', 'Linewidth', 1) 

% Jesus New Scheme does not remove any redundancy
% s = 1;
% M_Jesus_2_not_remove(1) = 0;
% R_Jesus_2_not_remove(1) = N;
% 
% for r = 1:K-s
%     M_Jesus_2_not_remove(r+1) = s/K + (N-1)*s/K*r/(K-s) + N*r/K;
%     R_Jesus_2_not_remove(r+1) = (K*func_mynchoosek(K-s, r+1)) / (K*nchoosek(K-s,r));
% end
% plot(M_Jesus_2_not_remove, R_Jesus_2_not_remove, 'b-o', 'Linewidth', 1) 

% % Jesus New Scheme with Virtual User
% s = 1;
% M_Jesus_Virtual(1) = NaN;
% R_Jesus_Virtual(1) = NaN;
% for r = 1:K+1-s
%     M_Jesus_Virtual(r+1) = s/(K+1) + (N-1)*s/(K+1)*r/((K+1)-s) + N*r/(K+1);
%     R_Jesus_Virtual(r+1) = (func_mynchoosek(K+1-s, r+1) - func_mynchoosek(K+1-s-min(K+1-s,N), r+1)) / nchoosek(K+1-s,r);
% end
% plot(M_Jesus_Virtual, R_Jesus_Virtual, 'b--*', 'Linewidth', 1) 
legend('Tian-Chen','Yu et al.', 'Chen', 'Gomez-Vilardebo Scheme 1', 'Gomez-Vilardebo Scheme 2')%, 'Gomez-Vilardebo Scheme with Virtual User')
set(gca, 'FontSize', 14)
title(['Caching system N = ', num2str(N), ', K = ', num2str(K), ', s = ', num2str(1)])
