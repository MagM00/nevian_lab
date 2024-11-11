function videos_concatenation_optimized(input_dir, output_file, remove_raw)
    FFmpeg_exe = 'M:\Software\FFmpeg\bin\ffmpeg.exe'; % Ensure this path is correct

    % Correctly build the path for Windows environments, if necessary
    % input_dir = fullfile(input_dir);

    % List all files in the directory
    files = dir(input_dir);
    
    % Filter .mp4 videos, ignoring case
    videos = files(arrayfun(@(x) endsWith(lower(x.name), '.mp4'), files));
    n_videos = numel(videos);

    if n_videos == 0
        fprintf('No videos were found.\n');
    elseif n_videos == 1
        singleVideoPath = fullfile(input_dir, videos(1).name);
        fprintf('Only one video found. Copying "%s" to "%s".\n', singleVideoPath, output_file);
        copyfile(singleVideoPath, output_file);
    else
        videos_list_filename = fullfile(tempdir, 'videos_list.txt');
        fileID = fopen(videos_list_filename, 'w');
        for i_video = 1:n_videos
            videoPath = fullfile(input_dir, videos(i_video).name);
            fprintf(fileID, 'file ''%s''\n', videoPath);
        end
        fclose(fileID);

        % Run FFmpeg to concatenate videos
        cmd = sprintf('"%s" -safe 0 -f concat -i "%s" -c copy "%s"', FFmpeg_exe, videos_list_filename, output_file);
        system(cmd);
        delete(videos_list_filename);
    end

    if remove_raw
        for i_video = 1:n_videos
            delete(fullfile(input_dir, videos(i_video).name));
        end
    end
end

% example usage:
% videos_concatenation_optimized('H:\Jun\sensory_stim\grabda\video\1489_ctrl', 'H:\Jun\sensory_stim\grabda\video\1489_ctrl.mp4', 1)