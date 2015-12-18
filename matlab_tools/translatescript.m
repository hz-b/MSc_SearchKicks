
d = dir('_data');
for k = 1:numel(d)
    f = d(k).name;
    
    if length(f) >= 4 && strcmp(f(1:4), 'Fast')
        fi = ['_data/' f];
        translateAndreasFile(fi)
    end
end