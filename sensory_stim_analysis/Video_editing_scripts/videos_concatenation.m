function videos_concatenation(input_dir, output_file, remove_raw)
    %% Preamble
    % This function takes the input dir and concatenates videos inside the
    % folder and saves them in the outputdir folder.
    %       Input: 
    %           input_dir: folder where the videos are. Within each forlder there must be at least
    %               2 .mp4 videos to be concatenated, otherwise it will be copied.
    %           output_file :The file where the cameras are going to be saved. It will
    %               contain all the concatenation of the videos <
    %%
    % Get info on animal and sessions to analyze
        do_copy_files = 0;
    FFmpeg_exe = 'M:\Software\FFmpeg\bin\ffmpeg.exe';
    video_path = input_dir;
    
    % Get the videos inside this folder
    videos = dir(video_path);
    videos = {videos.name}';
    videos = videos(cellfun(@(x) endsWith(x, '.mp4'), videos));
    n_videos = length(videos);

    % run concatenation
    if n_videos == 0
        log(sprintf('\tNo videos from camera %i', i_cam))
        return
    elseif n_videos == 1
        log(sprintf('Copying ''%s''', output_file), 'contains_path',true)
        copyfile(videos{1}, output_file)

    elseif n_videos > 1
        videos_list_filename = [tempname(), '.txt'];
        % Write videos list to disk
        fileID = fopen(videos_list_filename, 'w');
        for i_video = 1:n_videos
            fprintf(fileID, 'file ''%s''\n', fullfile(video_path, videos{i_video}));
        end
        fclose(fileID);

        % Run conversion in FFmpeg
        cmd = sprintf('%s -safe 0 -f concat -i %s -c copy "%s"', FFmpeg_exe, videos_list_filename, output_file);
        system(cmd)
        delete(videos_list_filename)
    end

    % Delete folder with raw videos
    if remove_raw
        fprintf('\tRemoving raw files ...')
        rmdir(video_path, 's')
        fprintf('\t\tdone')
    end

    if do_copy_files
        sprintf('\tCopying video to ''%s''', output_file)
        copyfile(filename, output_file)
        log('\t\tdone')
    end

end