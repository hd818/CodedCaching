function result = func_mynchoosek(N, K)
if N < K
    result = 0;
elseif N >= 0 && K == 0
    result = 1;
else
    result = nchoosek(N,K);
end