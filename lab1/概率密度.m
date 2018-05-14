x=magic04(:,1)
N_mean=mean(x) %¾ùÖµ
N_var=var(x) %·½²î  
y=gaussmf(x,[N_var N_mean]);

 
bar(x,y);
