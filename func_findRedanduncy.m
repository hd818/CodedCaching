% see how many redanduncies if using I/Q
% plan 1: directly get file A
% plan 2: get file A by using B+C+D....
function R_redundant = func_findRedanduncy(N,K,r)
% N = 3; K = 10; r = 1;
%% 2.  Demand types
partition = intpartgen(K-N, N); % consider all files requested
partition = cell2mat(partition(end));
if size(partition, 2) < N;
    partition = [partition, zeros(size(partition,1), N-size(partition,2))];
end
partition = partition + 1; 

d_num = size(partition, 1); % Number of demand types

%% 4. For each demand.
R_redundant = 1e12; % set it to really large initial value
for id = 1 : d_num
    R_redundant_d = 0;
    for f = 1:N
        demand = partition(id, :); % renew demand
        R_redundant_d_f = 0;
        demand(f) = demand(f) -1; % discard the current file
        if demand(f) == 0; % no current file, only plan 2 works
            demand_new(f) = 0;
            R_redundant_d_f = func_mynchoosek(sum(max(demand-2,0)), r+1);
        else demand(f) >= 1;
             even_pos = find(mod(demand, 2) == 0);
             odd_pos = find(mod(demand, 2) == 1);
             if isempty(find(demand == 1)); % if all files requested by multiple users
                % see which plan works better
                % plan 1
                demand_new = demand;
                demand_new(even_pos) = demand_new(even_pos) - 1; % minus 1
                demand_new(odd_pos) = demand_new(odd_pos) - 3; % minus 3
                if mod(demand(f),2) == 1;
                    demand_new(f) = demand(f) - 2; % update the current file, if odd, -3
                else
                    demand_new(f) = demand(f) - 2; % update the current file, if even, -1
                end
                R_redundant_d_f_1 = func_mynchoosek(sum(max(demand_new,0)), r+1);
                % plan 2
                demand_new = demand;
                demand_new(even_pos) = demand_new(even_pos) - 2;
                demand_new(odd_pos) = demand_new(odd_pos) - 2;
                if mod(demand(f),2) == 1;
                    demand_new(f) = demand(f) - 1; % update the current file, if odd, -3
                else
                    demand_new(f) = demand(f) - 1; % update the current file, if even, -1
                end
                R_redundant_d_f_2 = func_mynchoosek(sum(max(demand_new,0)), r+1);

                R_redundant_d_f = max(R_redundant_d_f_1, R_redundant_d_f_2);
            else  % if there is file requested by one user, only plan 2 works
                demand_new = demand;
                demand_new(even_pos) = demand_new(even_pos) - 2;
                demand_new(odd_pos) = demand_new(odd_pos) - 2;
                if mod(demand(f),2) == 1;
                    demand_new(f) = demand(f) - 1; % update the current file, if odd, -1
                else
                    demand_new(f) = demand(f) - 1; % update the current file, if even, -1
                end
                R_redundant_d_f = func_mynchoosek(sum(max(demand_new,0)), r+1);
            end
        end
        R_redundant_d_f = R_redundant_d_f * (demand(f) + 1);
        
        %% ============== If for in some demand, some file do not need I/Q/Bar, don't use it
        test1 = zeros(1,N); test1(f) = 1;
        test2 = ones(1,N); test2(f) = 0;
        if isequal(mod(demand, 2), test1) || isequal(mod(demand, 2), test2) 
            R_redundant_d_f = func_mynchoosek(sum(demand-1), r+1);
            R_redundant_d_f = R_redundant_d_f * (demand(f) + 1);
        end
        % ===============================================================
%         R_redundant_d_f = R_redundant_d_f * 2; % since there are two copies, even for those don't user I/Q/Bar, we multiple with 2
        R_redundant_d = R_redundant_d + R_redundant_d_f;
    end
    R_redundant = min(R_redundant, R_redundant_d);
    R_redundant_d;
end
R_redundant;

