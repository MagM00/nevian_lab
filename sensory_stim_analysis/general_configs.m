function config = general_configs()

    % Get user's home directory
    user_home = char(java.lang.System.getProperty('user.home'));
    
    % Determine the operating system
    if ispc
        os_type = 'Windows';
        
        % Define the root path for the repository (where the general_config file is)
        repo_path = fileparts(mfilename('fullpath'));
        
        % Extract the name of the repository from the repo path
        [~, repo_name] = fileparts(repo_path);
        
        % Define the root path for temporal data storage in OneDrive on Windows
        temp_data_path = fullfile('D:/', ['_temp_', repo_name]);
        
    elseif ismac
        os_type = 'Mac';
        
        % Define the root path for the repository (where the general_config file is)
        repo_path = fileparts(mfilename('fullpath'));
        
        % Extract the name of the repository from the repo path
        [~, repo_name] = fileparts(repo_path);
        
        % Define the root path for temporal data storage in OneDrive on Mac
        temp_data_path = fullfile(user_home, 'OneDrive - Universitaet Bern', 'Temp_data', repo_name);
        
    elseif isunix
        os_type = 'Unix/Linux';
        
        % Define the root path for the repository (where the general_config file is)
        repo_path = fileparts(mfilename('fullpath'));
        
        % Extract the name of the repository from the repo path
        [~, repo_name] = fileparts(repo_path);
        
        % Define the root path for temporal data storage on Unix/Linux
        % For now, I'm using the OneDrive folder in the user's home directory. Adjust as needed.
        temp_data_path = fullfile(user_home, 'OneDrive', 'Temp_data', repo_name);
        
    else
        error('OS not supported');
    end
    
    if ~exist(temp_data_path, 'dir')
        mkdir(temp_data_path);
    end

    % Store configuration settings in a structure
    config.os_type = os_type;
    config.repo_path = repo_path;
    config.temp_data_path = temp_data_path;

    % Add other configuration settings as needed

end
