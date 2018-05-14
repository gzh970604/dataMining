A=[];
for k=1:1:10
    for i=1:1:10
        A(k,i)=dot(magic04(:,k),magic04(:,i))
    end
end
        