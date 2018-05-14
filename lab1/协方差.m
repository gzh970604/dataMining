  n=1;
for i=1:1:10
    for j=i:1:10
        A(n)=sum((magic04(:,i)-mean(magic04(:,i))).*(magic04(:,j)-mean(magic04(:,j))))/(size(magic04,1)-1);
        n=n+1; 
    end
end
A;
max(A)
min(A)