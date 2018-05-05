%{
Quick script to generate permutations of a column vector that contains repeated measurements
per subject. Each shuffled vector randomly assigns the data from one subject to another.
Saves a matrix where each column is a different permuted order. At this point, it's easy to
loop through the columns and re-run your analysis on each permuted version of the variable.
}%

%CHANGE THESE%
%%%%%%%%%%%%%%
numperms = 1000 %number of permutations
numsubs = 91 %number of subjects
data = concept2 %column vector with all your data
numvals = 15 %number of data points per subject
%%%%%%%%%%%%%%

perms = zeros(length(data),numperms) %preallocate
for ss = 1:numperms
    
    newOrder = randperm(numsubs);
    newArray = zeros(length(concept2),1);
    
    for ii = 1:length(newOrder)
        for jj = (numvals-1):-1:0
            newArray(numvals*ii-jj) = concept2(numvals*newOrder(ii)-jj);
        end
    end
    
    newArray
    perms(:,ss) = newArray;
    
    clear newOrder; clear newArray;
end
