% plot variation

data = csvread('purposeStartHour.csv',1,1);


titles = {'Commute','Education','Business','Shopping',...
    'Other escort + personal','Entertainment','Other'};

figure(1)
for i = 1:7
    pdf = data(i,:);
    pdf = pdf/sum(pdf);
    subplot(4,2,i)
    plot([1:24],pdf)
    title(titles(i))
end

figure(2)
purposes = [0.1523,0.0634,0.0014,0.2226,0.2583,0.2801,0.0220];
bar(purposes)
set(gca,'XTickLabel',titles)
set(gca,'XTickLabelRotation',45)

data2 = csvread('regionTypePurposeLength.csv',1,1);

x = [0:0.1:30];
figure(3)

for i = 1:7
    pdf2 = normpdf(x,data2(i,1),1);
    plot(x,pdf2)
    if i ~= 7
        hold on
    else
        legend(titles)
    end
end
xlabel('Distance /miles')
ylabel('p(length | region type)')