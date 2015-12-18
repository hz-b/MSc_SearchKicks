function outputFile = translateAndreasFile(file)
%
% Olivier CHURLAUD <olivier.churlaud@helmholtz-berlin.de>
% 2015/12/18
%

assert(exist(file, 'file') > 0, 'Input file doesn''t exist.');

load(file)

assert(exist('valuesX', 'var') > 0, 'valuesX doesn''t exist in file.');
assert(exist('valuesY', 'var') > 0, 'valuesY doesn''t exist in file.');
assert(exist('id', 'var') > 0, 'id doesn''t exist in file.');
assert(exist('Freq', 'var') > 0, 'Freq doesn''t exist in file.');
assert(exist('Samples', 'var') > 0, 'Samples doesn''t exist in file.');
assert(exist('bpms', 'var') > 0, 'bpms doesn''t exist in file.');

sample_nb = size(valuesX, 2);
difforbitX = cell(1, sample_nb);
difforbitY = cell(1, sample_nb);
CMx = cell(1, sample_nb);
CMy = cell(1, sample_nb);

CM_nb = 48;

for k = 1:sample_nb
    difforbitX{1,k} = valuesX(:, k);
    difforbitY{1,k} = valuesY(:, k);
    CMx{1,k} = zeros(CM_nb, 1);
    CMy{1,k} = zeros(CM_nb, 1);
end

size(difforbitX)
size(difforbitY)

splitedFilename = strsplit(file, '/');
if numel(splitedFilename) > 2
    folder = strjoin(splitedFilename{1:end-1}, '/');
else
    folder = splitedFilename{1};
end
filename = splitedFilename{end};
outputFile = [folder '/translated_' filename];
save(outputFile, 'difforbitX' ...
               , 'difforbitY' ...
               , 'CMx' ...
               , 'CMy' ...
               , 'id' ...
               , 'Freq' ...
               , 'Samples' ...
               , 'bpms' ...
               );
end