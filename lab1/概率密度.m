x=magic04(:,1)
N_mean=mean(x) %��ֵ
N_var=var(x) %����  
y=gaussmf(x,[N_var N_mean]);

 
bar(x,y);
