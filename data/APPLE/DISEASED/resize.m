myFolder = 'D:\DBV\walnut1\ad';
if ~isdir(myFolder)
  errorMessage = sprintf('Error: The following folder does not exist:\n%s', myFolder);
  uiwait(warndlg(errorMessage));
  return;
end
filePattern = fullfile(myFolder, '*.jpg');
jpegFiles = dir(filePattern);
for k = 1:length(jpegFiles)
  baseFileName = jpegFiles(k).name;
  fullFileName = fullfile(myFolder, baseFileName);
  fprintf(1, 'Now reading %s\n', fullFileName);
  imageArray = imread(fullFileName);
  imshow(imageArray);  % Display image.
  drawnow; % Force display to update immediately.
  % Get initial size
  [rows, columns, numberOfColorChannels] = size(imageArray);
  % Get size reduction / magnification factor
  sizeFactor = 6000 / columns;
  % Resize
  newImage = imresize(imageArray, sizeFactor);
  % Get the new size.
  [rows, columns, numberOfColorChannels] = size(imageArray);
  % Crop if necessary
 % if rows > 4000
    % Take upper 600 lines.  You could take lower or middle 600 also.
   % newImage = imcrop(imageArray, [1,1,columns, 600]);
    newFileName = strrep(fullFileName, '.jpg', '_resized.jpg');
    imwrite(newImage, newFileName );
  %end
end
