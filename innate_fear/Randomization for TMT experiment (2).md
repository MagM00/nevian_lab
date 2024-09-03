```python
import random

numbers = [0] * 15 + [1] * 15
seeds = ['UniBe{:03d}'.format(i) for i in range(1, 14)]

for seed in seeds:
    random.seed(seed)
    random.shuffle(numbers)
    print(f"Seed: {seed}, Randomized Stim: {numbers}")
```

    Seed: UniBe001, Randomized Stim: [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0]
    Seed: UniBe002, Randomized Stim: [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1]
    Seed: UniBe003, Randomized Stim: [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0]
    Seed: UniBe004, Randomized Stim: [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0]
    Seed: UniBe005, Randomized Stim: [0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1]
    Seed: UniBe006, Randomized Stim: [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1]
    Seed: UniBe007, Randomized Stim: [1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1]
    Seed: UniBe008, Randomized Stim: [1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
    Seed: UniBe009, Randomized Stim: [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0]
    Seed: UniBe010, Randomized Stim: [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1]
    Seed: UniBe011, Randomized Stim: [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1]
    Seed: UniBe012, Randomized Stim: [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1]
    Seed: UniBe013, Randomized Stim: [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
    


```python
import random

seeds = ['UniBe{:03d}'.format(i) for i in range(1, 14)]

for seed in seeds:
    random.seed(seed)
    row = [random.randint(30, 60) for _ in range(30)]
    print(f"Seed: {seed}, Randomized Intervals: {row}")
```

    Seed: UniBe001, Randomized Intervals: [37, 47, 38, 33, 46, 46, 60, 34, 57, 41, 53, 40, 54, 41, 41, 60, 44, 31, 47, 44, 47, 38, 43, 52, 45, 60, 58, 46, 35, 49]
    Seed: UniBe002, Randomized Intervals: [42, 45, 44, 46, 47, 48, 54, 43, 46, 52, 30, 52, 38, 32, 41, 46, 40, 42, 38, 49, 45, 55, 53, 33, 35, 45, 57, 45, 59, 59]
    Seed: UniBe003, Randomized Intervals: [36, 56, 33, 52, 59, 41, 32, 55, 60, 54, 32, 60, 44, 44, 59, 55, 31, 48, 37, 43, 59, 43, 37, 47, 38, 31, 48, 54, 44, 53]
    Seed: UniBe004, Randomized Intervals: [59, 49, 60, 59, 52, 52, 40, 47, 58, 36, 50, 35, 45, 38, 30, 54, 33, 42, 36, 58, 44, 58, 50, 58, 45, 47, 46, 49, 49, 34]
    Seed: UniBe005, Randomized Intervals: [42, 39, 54, 41, 58, 40, 32, 49, 45, 32, 51, 51, 59, 44, 60, 35, 30, 48, 57, 55, 43, 56, 51, 37, 53, 60, 56, 53, 45, 60]
    Seed: UniBe006, Randomized Intervals: [40, 43, 34, 56, 55, 60, 45, 45, 30, 42, 49, 38, 50, 50, 51, 41, 36, 30, 34, 43, 32, 47, 49, 51, 41, 57, 32, 60, 55, 58]
    Seed: UniBe007, Randomized Intervals: [40, 40, 32, 40, 33, 42, 40, 40, 58, 37, 47, 48, 41, 48, 42, 37, 54, 42, 30, 59, 54, 45, 52, 45, 33, 38, 54, 54, 33, 42]
    Seed: UniBe008, Randomized Intervals: [60, 39, 43, 36, 32, 40, 33, 34, 48, 53, 37, 40, 54, 33, 59, 50, 40, 50, 51, 60, 52, 32, 47, 36, 58, 47, 36, 33, 60, 50]
    Seed: UniBe009, Randomized Intervals: [51, 30, 43, 42, 47, 60, 35, 52, 53, 39, 31, 60, 34, 54, 58, 53, 36, 57, 41, 52, 58, 33, 56, 43, 36, 37, 38, 48, 53, 42]
    Seed: UniBe010, Randomized Intervals: [37, 46, 58, 32, 49, 45, 41, 57, 46, 54, 58, 34, 47, 48, 43, 46, 36, 47, 40, 52, 49, 48, 32, 46, 56, 34, 60, 53, 48, 48]
    Seed: UniBe011, Randomized Intervals: [35, 34, 38, 48, 48, 59, 57, 57, 34, 33, 51, 55, 53, 59, 52, 56, 37, 34, 36, 42, 35, 42, 35, 59, 38, 42, 31, 56, 35, 32]
    Seed: UniBe012, Randomized Intervals: [46, 32, 40, 60, 42, 38, 31, 60, 51, 58, 30, 39, 45, 55, 58, 50, 31, 36, 54, 52, 31, 44, 37, 36, 41, 46, 56, 34, 31, 52]
    Seed: UniBe013, Randomized Intervals: [56, 48, 58, 43, 40, 32, 40, 60, 39, 58, 30, 45, 55, 51, 40, 47, 58, 38, 37, 59, 53, 55, 54, 36, 48, 34, 52, 37, 45, 31]
    


```python
import random

seeds = ['UniBe{:03d}'.format(i) for i in range(1, 14)]

for seed in seeds:
    random.seed(seed)
    row = [random.randint(30, 60) for _ in range(29)]
    cumulative_time = [30] + row
    cumulative_seconds = [sum(cumulative_time[:i+1]) for i in range(len(cumulative_time))]
    time_in_minutes = [divmod(seconds, 60) for seconds in cumulative_seconds]
    time_formatted = [f"{minutes:02d}:{seconds:02d}" for minutes, seconds in time_in_minutes]
    print(f"Seed: {seed}, Randomized Intervals: {time_formatted}")

```

    Seed: UniBe001, Randomized Intervals: ['00:30', '01:07', '01:54', '02:32', '03:05', '03:51', '04:37', '05:37', '06:11', '07:08', '07:49', '08:42', '09:22', '10:16', '10:57', '11:38', '12:38', '13:22', '13:53', '14:40', '15:24', '16:11', '16:49', '17:32', '18:24', '19:09', '20:09', '21:07', '21:53', '22:28']
    Seed: UniBe002, Randomized Intervals: ['00:30', '01:12', '01:57', '02:41', '03:27', '04:14', '05:02', '05:56', '06:39', '07:25', '08:17', '08:47', '09:39', '10:17', '10:49', '11:30', '12:16', '12:56', '13:38', '14:16', '15:05', '15:50', '16:45', '17:38', '18:11', '18:46', '19:31', '20:28', '21:13', '22:12']
    Seed: UniBe003, Randomized Intervals: ['00:30', '01:06', '02:02', '02:35', '03:27', '04:26', '05:07', '05:39', '06:34', '07:34', '08:28', '09:00', '10:00', '10:44', '11:28', '12:27', '13:22', '13:53', '14:41', '15:18', '16:01', '17:00', '17:43', '18:20', '19:07', '19:45', '20:16', '21:04', '21:58', '22:42']
    Seed: UniBe004, Randomized Intervals: ['00:30', '01:29', '02:18', '03:18', '04:17', '05:09', '06:01', '06:41', '07:28', '08:26', '09:02', '09:52', '10:27', '11:12', '11:50', '12:20', '13:14', '13:47', '14:29', '15:05', '16:03', '16:47', '17:45', '18:35', '19:33', '20:18', '21:05', '21:51', '22:40', '23:29']
    Seed: UniBe005, Randomized Intervals: ['00:30', '01:12', '01:51', '02:45', '03:26', '04:24', '05:04', '05:36', '06:25', '07:10', '07:42', '08:33', '09:24', '10:23', '11:07', '12:07', '12:42', '13:12', '14:00', '14:57', '15:52', '16:35', '17:31', '18:22', '18:59', '19:52', '20:52', '21:48', '22:41', '23:26']
    Seed: UniBe006, Randomized Intervals: ['00:30', '01:10', '01:53', '02:27', '03:23', '04:18', '05:18', '06:03', '06:48', '07:18', '08:00', '08:49', '09:27', '10:17', '11:07', '11:58', '12:39', '13:15', '13:45', '14:19', '15:02', '15:34', '16:21', '17:10', '18:01', '18:42', '19:39', '20:11', '21:11', '22:06']
    Seed: UniBe007, Randomized Intervals: ['00:30', '01:10', '01:50', '02:22', '03:02', '03:35', '04:17', '04:57', '05:37', '06:35', '07:12', '07:59', '08:47', '09:28', '10:16', '10:58', '11:35', '12:29', '13:11', '13:41', '14:40', '15:34', '16:19', '17:11', '17:56', '18:29', '19:07', '20:01', '20:55', '21:28']
    Seed: UniBe008, Randomized Intervals: ['00:30', '01:30', '02:09', '02:52', '03:28', '04:00', '04:40', '05:13', '05:47', '06:35', '07:28', '08:05', '08:45', '09:39', '10:12', '11:11', '12:01', '12:41', '13:31', '14:22', '15:22', '16:14', '16:46', '17:33', '18:09', '19:07', '19:54', '20:30', '21:03', '22:03']
    Seed: UniBe009, Randomized Intervals: ['00:30', '01:21', '01:51', '02:34', '03:16', '04:03', '05:03', '05:38', '06:30', '07:23', '08:02', '08:33', '09:33', '10:07', '11:01', '11:59', '12:52', '13:28', '14:25', '15:06', '15:58', '16:56', '17:29', '18:25', '19:08', '19:44', '20:21', '20:59', '21:47', '22:40']
    Seed: UniBe010, Randomized Intervals: ['00:30', '01:07', '01:53', '02:51', '03:23', '04:12', '04:57', '05:38', '06:35', '07:21', '08:15', '09:13', '09:47', '10:34', '11:22', '12:05', '12:51', '13:27', '14:14', '14:54', '15:46', '16:35', '17:23', '17:55', '18:41', '19:37', '20:11', '21:11', '22:04', '22:52']
    Seed: UniBe011, Randomized Intervals: ['00:30', '01:05', '01:39', '02:17', '03:05', '03:53', '04:52', '05:49', '06:46', '07:20', '07:53', '08:44', '09:39', '10:32', '11:31', '12:23', '13:19', '13:56', '14:30', '15:06', '15:48', '16:23', '17:05', '17:40', '18:39', '19:17', '19:59', '20:30', '21:26', '22:01']
    Seed: UniBe012, Randomized Intervals: ['00:30', '01:16', '01:48', '02:28', '03:28', '04:10', '04:48', '05:19', '06:19', '07:10', '08:08', '08:38', '09:17', '10:02', '10:57', '11:55', '12:45', '13:16', '13:52', '14:46', '15:38', '16:09', '16:53', '17:30', '18:06', '18:47', '19:33', '20:29', '21:03', '21:34']
    Seed: UniBe013, Randomized Intervals: ['00:30', '01:26', '02:14', '03:12', '03:55', '04:35', '05:07', '05:47', '06:47', '07:26', '08:24', '08:54', '09:39', '10:34', '11:25', '12:05', '12:52', '13:50', '14:28', '15:05', '16:04', '16:57', '17:52', '18:46', '19:22', '20:10', '20:44', '21:36', '22:13', '22:58']
    


```python
import random

seeds = ['UniBe{:03d}'.format(i) for i in range(1, 14)]
numbers = [0] * 15 + [1] * 15

for seed in seeds:
    random.seed(seed)
    random.shuffle(numbers)

    random_intervals = [random.randint(30, 60) for _ in range(29)]
    cumulative_time = [30] + random_intervals
    cumulative_seconds = [sum(cumulative_time[:i+1]) for i in range(len(cumulative_time))]
    time_in_minutes = [divmod(seconds, 60) for seconds in cumulative_seconds]
    time_formatted = [f"{minutes:02d}:{seconds:02d}" for minutes, seconds in time_in_minutes]
    
    print(f"Seed: {seed}, Randomized Stim: {numbers}")
    print(f"Seed: {seed}, Randomized Intervals: {time_formatted}")
    print()

```

    Seed: UniBe001, Randomized Stim: [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0]
    Seed: UniBe001, Randomized Intervals: ['00:30', '01:28', '01:59', '02:29', '03:23', '03:57', '04:36', '05:24', '06:24', '07:23', '08:10', '08:56', '09:39', '10:13', '10:54', '11:33', '12:15', '13:00', '13:34', '14:11', '15:03', '15:35', '16:09', '16:42', '17:38', '18:09', '18:51', '19:22', '20:00', '20:59']
    
    Seed: UniBe002, Randomized Stim: [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1]
    Seed: UniBe002, Randomized Intervals: ['00:30', '01:05', '01:53', '02:25', '03:25', '04:16', '05:10', '05:59', '06:35', '07:19', '08:17', '08:54', '09:50', '10:36', '11:30', '12:13', '12:48', '13:31', '14:16', '15:15', '16:08', '17:03', '17:44', '18:27', '19:24', '20:21', '20:53', '21:27', '22:09', '23:07']
    
    Seed: UniBe003, Randomized Stim: [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0]
    Seed: UniBe003, Randomized Intervals: ['00:30', '01:17', '01:47', '02:28', '03:11', '03:43', '04:19', '04:59', '05:32', '06:29', '07:28', '08:11', '08:42', '09:23', '10:18', '11:13', '12:04', '13:00', '13:36', '14:22', '15:13', '16:11', '16:52', '17:40', '18:14', '18:47', '19:36', '20:32', '21:22', '22:13']
    
    Seed: UniBe004, Randomized Stim: [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0]
    Seed: UniBe004, Randomized Intervals: ['00:30', '01:29', '02:07', '02:48', '03:39', '04:19', '04:59', '05:46', '06:20', '06:50', '07:49', '08:38', '09:37', '10:19', '11:16', '12:03', '12:42', '13:34', '14:08', '14:53', '15:25', '16:12', '16:56', '17:41', '18:11', '19:06', '19:43', '20:27', '21:02', '22:02']
    
    Seed: UniBe005, Randomized Stim: [0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1]
    Seed: UniBe005, Randomized Intervals: ['00:30', '01:15', '02:06', '02:55', '03:35', '04:12', '04:47', '05:29', '06:28', '07:11', '07:54', '08:31', '09:07', '09:54', '10:43', '11:15', '11:54', '12:48', '13:19', '14:08', '14:51', '15:47', '16:24', '17:20', '18:12', '19:08', '19:53', '20:48', '21:26', '22:09']
    
    Seed: UniBe006, Randomized Stim: [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1]
    Seed: UniBe006, Randomized Intervals: ['00:30', '01:02', '01:56', '02:36', '03:17', '03:54', '04:32', '05:05', '05:42', '06:30', '07:15', '07:54', '08:46', '09:16', '09:46', '10:23', '11:13', '11:49', '12:44', '13:39', '14:35', '15:26', '16:02', '16:34', '17:16', '18:15', '18:48', '19:46', '20:21', '21:00']
    
    Seed: UniBe007, Randomized Stim: [1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1]
    Seed: UniBe007, Randomized Intervals: ['00:30', '01:18', '02:06', '03:02', '03:39', '04:14', '05:13', '06:05', '06:47', '07:44', '08:42', '09:15', '10:06', '10:56', '11:56', '12:53', '13:23', '14:11', '14:51', '15:41', '16:34', '17:24', '18:07', '18:44', '19:43', '20:42', '21:42', '22:19', '22:53', '23:28']
    
    Seed: UniBe008, Randomized Stim: [1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
    Seed: UniBe008, Randomized Intervals: ['00:30', '01:24', '02:11', '02:47', '03:25', '03:56', '04:27', '05:06', '05:37', '06:32', '07:24', '08:00', '09:00', '09:30', '10:26', '11:08', '12:08', '12:50', '13:45', '14:38', '15:37', '16:30', '17:11', '18:03', '18:55', '19:41', '20:31', '21:16', '22:10', '22:59']
    
    Seed: UniBe009, Randomized Stim: [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0]
    Seed: UniBe009, Randomized Intervals: ['00:30', '01:25', '02:10', '02:43', '03:42', '04:15', '04:55', '05:40', '06:23', '06:58', '07:48', '08:36', '09:29', '10:09', '11:05', '11:49', '12:33', '13:18', '13:59', '14:56', '15:55', '16:50', '17:50', '18:46', '19:31', '20:30', '21:05', '22:05', '23:04', '23:57']
    
    Seed: UniBe010, Randomized Stim: [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1]
    Seed: UniBe010, Randomized Intervals: ['00:30', '01:14', '02:09', '03:07', '03:57', '04:28', '05:25', '06:21', '06:56', '07:30', '08:22', '09:02', '09:38', '10:26', '11:05', '11:40', '12:21', '13:14', '14:06', '14:37', '15:13', '16:04', '16:44', '17:23', '18:20', '19:02', '19:40', '20:28', '21:18', '22:07']
    
    Seed: UniBe011, Randomized Stim: [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1]
    Seed: UniBe011, Randomized Intervals: ['00:30', '01:10', '01:53', '02:29', '03:24', '04:00', '04:42', '05:33', '06:22', '07:20', '08:04', '08:52', '09:38', '10:35', '11:11', '12:01', '12:31', '13:08', '14:02', '14:39', '15:13', '15:54', '16:35', '17:25', '17:57', '18:43', '19:37', '20:29', '21:20', '22:08']
    
    Seed: UniBe012, Randomized Stim: [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1]
    Seed: UniBe012, Randomized Intervals: ['00:30', '01:06', '01:57', '02:44', '03:22', '04:19', '05:06', '05:45', '06:31', '07:14', '08:06', '08:49', '09:36', '10:06', '10:50', '11:36', '12:24', '13:13', '14:08', '14:48', '15:26', '16:14', '17:07', '18:03', '18:49', '19:21', '20:18', '21:07', '21:54', '22:32']
    
    Seed: UniBe013, Randomized Stim: [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
    Seed: UniBe013, Randomized Intervals: ['00:30', '01:26', '02:01', '02:47', '03:39', '04:36', '05:20', '06:13', '07:05', '07:38', '08:23', '09:10', '10:09', '10:48', '11:38', '12:16', '12:46', '13:44', '14:15', '15:13', '15:51', '16:48', '17:33', '18:08', '18:57', '19:35', '20:33', '21:30', '22:13', '23:07']
    
    


```python
import random
import pandas as pd

seeds = ['UniBe{:03d}'.format(i) for i in range(1, 14)]
numbers = [0] * 15 + [1] * 15

for seed in seeds:
    random.seed(seed)
    random.shuffle(numbers)

    random_intervals = [random.randint(30, 60) for _ in range(29)]
    cumulative_time = [0] + random_intervals
    cumulative_seconds = [sum(cumulative_time[:i+1]) for i in range(len(cumulative_time))]
    time_in_minutes = [divmod(seconds, 60) for seconds in cumulative_seconds]
    time_formatted = [f"{minutes:02d}:{seconds:02d}" for minutes, seconds in time_in_minutes]

    # Create a DataFrame for each seed's data
    data = pd.DataFrame({'Stim': numbers, 'Time': time_formatted})

    # Save DataFrame to an Excel file
    filename = f"seed_{seed}.xlsx"
    data.to_excel(filename, index=False)

```


```python
import random
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font

seeds = ['UniBe{:03d}'.format(i) for i in range(1, 14)]
numbers = [0] * 15 + [1] * 15

for seed in seeds:
    random.seed(seed)
    random.shuffle(numbers)

    random_intervals = [random.randint(30, 60) for _ in range(29)]
    cumulative_time = [0] + random_intervals
    cumulative_seconds = [sum(cumulative_time[:i+1]) for i in range(len(cumulative_time))]
    time_in_minutes = [divmod(seconds, 60) for seconds in cumulative_seconds]
    time_formatted = [f"{minutes:02d}:{seconds:02d}" for minutes, seconds in time_in_minutes]

    # Create a DataFrame for each seed's data
    data = pd.DataFrame({'Randomized Stim': numbers, 'Randomized Intervals': time_formatted})

    # Create a workbook and sheet
    workbook = Workbook()
    sheet = workbook.active

    # Convert DataFrame to a list of lists
    data_list = data.values.tolist()

    # Append the rows to the sheet
    for row in data_list:
        sheet.append(row)

    # Apply font formatting
    font = Font(size=14)  # Set the desired font size
    for col in sheet.columns:
        for cell in col:
            cell.font = font

    # Save the Excel file
    filename = f"seed_{seed}.xlsx"
    workbook.save(filename)

```


```python
import tkinter as tk
from datetime import datetime, timedelta

# Define the data
data = {
        'UniBe001': 
            {'Stim': [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0], 
             'Time': ['00:30', '01:28', '01:59', '02:29', '03:23', '03:57', '04:36', '05:24', '06:24', '07:23', 
                      '08:10', '08:56', '09:39', '10:13', '10:54', '11:33', '12:15', '13:00', '13:34', '14:11', 
                      '15:03', '15:35', '16:09', '16:42', '17:38', '18:09', '18:51', '19:22', '20:00', '20:59']}, 
        'UniBe002': 
            {'Stim': [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1], 
             'Time': ['00:30', '01:05', '01:53', '02:25', '03:25', '04:16', '05:10', '05:59', '06:35', '07:19', 
                      '08:17', '08:54', '09:50', '10:36', '11:30', '12:13', '12:48', '13:31', '14:16', '15:15', 
                      '16:08', '17:03', '17:44', '18:27', '19:24', '20:21', '20:53', '21:27', '22:09', '23:07']}, 
        'UniBe003': 
            {'Stim': [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0], 
             'Time': ['00:30', '01:17', '01:47', '02:28', '03:11', '03:43', '04:19', '04:59', '05:32', '06:29', 
                      '07:28', '08:11', '08:42', '09:23', '10:18', '11:13', '12:04', '13:00', '13:36', '14:22', 
                      '15:13', '16:11', '16:52', '17:40', '18:14', '18:47', '19:36', '20:32', '21:22', '22:13']}, 
        'UniBe004': 
            {'Stim': [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0], 
             'Time': ['00:30', '01:29', '02:07', '02:48', '03:39', '04:19', '04:59', '05:46', '06:20', '06:50', 
                      '07:49', '08:38', '09:37', '10:19', '11:16', '12:03', '12:42', '13:34', '14:08', '14:53', 
                      '15:25', '16:12', '16:56', '17:41', '18:11', '19:06', '19:43', '20:27', '21:02', '22:02']}, 
        'UniBe005': 
            {'Stim': [0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1], 
             'Time': ['00:30', '01:15', '02:06', '02:55', '03:35', '04:12', '04:47', '05:29', '06:28', '07:11', 
                      '07:54', '08:31', '09:07', '09:54', '10:43', '11:15', '11:54', '12:48', '13:19', '14:08', 
                      '14:51', '15:47', '16:24', '17:20', '18:12', '19:08', '19:53', '20:48', '21:26', '22:09']}, 
        'UniBe006': 
            {'Stim':[0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1], 
             'Time': ['00:30', '01:02', '01:56', '02:36', '03:17', '03:54', '04:32', '05:05', '05:42', '06:30', 
                      '07:15', '07:54', '08:46', '09:16', '09:46', '10:23', '11:13', '11:49', '12:44', '13:39', 
                      '14:35', '15:26', '16:02', '16:34', '17:16', '18:15', '18:48', '19:46', '20:21', '21:00']}, 
        'UniBe007': 
            {'Stim': [1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1], 
             'Time': ['00:30', '01:18', '02:06', '03:02', '03:39', '04:14', '05:13', '06:05', '06:47', '07:44', 
                      '08:42', '09:15', '10:06', '10:56', '11:56', '12:53', '13:23', '14:11', '14:51', '15:41', 
                      '16:34', '17:24', '18:07', '18:44', '19:43', '20:42', '21:42', '22:19', '22:53', '23:28']}, 
        'UniBe008': 
            {'Stim': [1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1], 
             'Time': ['00:30', '01:24', '02:11', '02:47', '03:25', '03:56', '04:27', '05:06', '05:37', '06:32', 
                      '07:24', '08:00', '09:00', '09:30', '10:26', '11:08', '12:08', '12:50', '13:45', '14:38', 
                      '15:37', '16:30', '17:11', '18:03', '18:55', '19:41', '20:31', '21:16', '22:10', '22:59']}, 
        'UniBe009': 
            {'Stim': [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0], 
             'Time': ['00:30', '01:25', '02:10', '02:43', '03:42', '04:15', '04:55', '05:40', '06:23', '06:58', 
                      '07:48', '08:36', '09:29', '10:09', '11:05', '11:49', '12:33', '13:18', '13:59', '14:56', 
                      '15:55', '16:50', '17:50', '18:46', '19:31', '20:30', '21:05', '22:05', '23:04', '23:57']}, 
        'UniBe010': 
            {'Stim': [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1], 
             'Time': ['00:30', '01:14', '02:09', '03:07', '03:57', '04:28', '05:25', '06:21', '06:56', '07:30', 
                      '08:22', '09:02', '09:38', '10:26', '11:05', '11:40', '12:21', '13:14', '14:06', '14:37', 
                      '15:13', '16:04', '16:44', '17:23', '18:20', '19:02', '19:40', '20:28', '21:18', '22:07']}, 
        'UniBe011': 
            {'Stim': [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1], 
             'Time': ['00:30', '01:10', '01:53', '02:29', '03:24', '04:00', '04:42', '05:33', '06:22', '07:20', 
                      '08:04', '08:52', '09:38', '10:35', '11:11', '12:01', '12:31', '13:08', '14:02', '14:39', 
                      '15:13', '15:54', '16:35', '17:25', '17:57', '18:43', '19:37', '20:29', '21:20', '22:08']}, 
        'UniBe012': 
            {'Stim': [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1], 
             'Time': ['00:30', '01:06', '01:57', '02:44', '03:22', '04:19', '05:06', '05:45', '06:31', '07:14', 
                      '08:06', '08:49', '09:36', '10:06', '10:50', '11:36', '12:24', '13:13', '14:08', '14:48', 
                      '15:26', '16:14', '17:07', '18:03', '18:49', '19:21', '20:18', '21:07', '21:54', '22:32']}, 
        'UniBe013': 
            {'Stim': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1], 
             'Time': ['00:30', '01:26', '02:01', '02:47', '03:39', '04:36', '05:20', '06:13', '07:05', '07:38', 
                      '08:23', '09:10', '10:09', '10:48', '11:38', '12:16', '12:46', '13:44', '14:15', '15:13', 
                      '15:51', '16:48', '17:33', '18:08', '18:57', '19:35', '20:33', '21:30', '22:13', '23:07']}}

class TimerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer GUI")
        self.current_set = None
        self.timer_running = False
        self.remaining_time = timedelta()
        self.upcoming_events = []

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        # Set Selection
        self.label_set = tk.Label(self.frame, text="Select Set:")
        self.label_set.grid(row=0, column=0, sticky="W")

        self.set_var = tk.StringVar()
        self.set_var.set("Select a set")
        self.set_dropdown = tk.OptionMenu(self.frame, self.set_var, *data.keys(), command=self.on_set_select)
        self.set_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="W")

        # Timer
        self.timer_label = tk.Label(self.frame, text="00:00", font=("Arial", 200), width=10)
        self.timer_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Upcoming Event
        self.event_label = tk.Label(self.frame, text="", font=("Arial", 100), fg="red")
        self.event_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Next Event Type
        self.event_type_label = tk.Label(self.frame, text="", font=("Arial", 100))
        self.event_type_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Begin Button
        self.begin_button = tk.Button(self.frame, text="Begin", command=self.start_timer, state=tk.DISABLED)
        self.begin_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def on_set_select(self, selected_set):
        self.current_set = selected_set
        self.begin_button["state"] = tk.NORMAL
        first_event_type = "TMT" if data[self.current_set]["Stim"][0] == 1 else "Saline"
        self.event_type_label["text"] = f"First Event Type: {first_event_type}"

    def start_timer(self):
        if self.current_set:
            self.timer_running =True
            self.begin_button["state"] = tk.DISABLED
            self.remaining_time = timedelta(seconds=0)
            self.upcoming_events = [datetime.strptime(t, "%M:%S") for t in data[self.current_set]["Time"]]
            self.countup()

    def countup(self):
        if self.timer_running:
            self.remaining_time += timedelta(seconds=1)
            self.timer_label["text"] = str(self.remaining_time)[2:]

            if self.upcoming_events:
                upcoming_event = self.upcoming_events[0]
                time_diff = upcoming_event - datetime.strptime(str(self.remaining_time)[2:], "%M:%S")

                if time_diff <= timedelta(seconds=30):
                    self.event_label["text"] = f"Upcoming Event: {upcoming_event.strftime('%M:%S')} ({time_diff.seconds}s)"
                    event_index = len(data[self.current_set]["Time"]) - len(self.upcoming_events)
                    if data[self.current_set]["Stim"][event_index] == 1:
                        self.event_type_label["text"] = "Next Event Type: TMT"
                    else:
                        self.event_type_label["text"] = "Next Event Type: Saline"
                else:
                    self.event_label["text"] = ""
                    self.event_type_label["text"] = ""

                if time_diff <= timedelta(seconds=0):
                    self.upcoming_events.pop(0)
            if self.timer_running:
                self.root.after(991, self.countup)

    def stop_timer(self):
        self.timer_running = False

root = tk.Tk()
root.attributes("-fullscreen", True)  # Make the GUI full screen
app = TimerGUI(root)
root.mainloop()


```


```python

```


```python

```


```python
import tkinter as tk
from datetime import datetime, timedelta, date

# Define the data
data = {
        'UniBe001': 
            {'Stim': [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0], 
             'Time': ['00:30', '01:28', '01:59', '02:29', '03:23', '03:57', '04:36', '05:24', '06:24', '07:23', 
                      '08:10', '08:56', '09:39', '10:13', '10:54', '11:33', '12:15', '13:00', '13:34', '14:11', 
                      '15:03', '15:35', '16:09', '16:42', '17:38', '18:09', '18:51', '19:22', '20:00', '20:59']}, 
        'UniBe002': 
            {'Stim': [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1], 
             'Time': ['00:30', '01:05', '01:53', '02:25', '03:25', '04:16', '05:10', '05:59', '06:35', '07:19', 
                      '08:17', '08:54', '09:50', '10:36', '11:30', '12:13', '12:48', '13:31', '14:16', '15:15', 
                      '16:08', '17:03', '17:44', '18:27', '19:24', '20:21', '20:53', '21:27', '22:09', '23:07']}, 
        'UniBe003': 
            {'Stim': [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0], 
             'Time': ['00:30', '01:17', '01:47', '02:28', '03:11', '03:43', '04:19', '04:59', '05:32', '06:29', 
                      '07:28', '08:11', '08:42', '09:23', '10:18', '11:13', '12:04', '13:00', '13:36', '14:22', 
                      '15:13', '16:11', '16:52', '17:40', '18:14', '18:47', '19:36', '20:32', '21:22', '22:13']}, 
        'UniBe004': 
            {'Stim': [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0], 
             'Time': ['00:30', '01:29', '02:07', '02:48', '03:39', '04:19', '04:59', '05:46', '06:20', '06:50', 
                      '07:49', '08:38', '09:37', '10:19', '11:16', '12:03', '12:42', '13:34', '14:08', '14:53', 
                      '15:25', '16:12', '16:56', '17:41', '18:11', '19:06', '19:43', '20:27', '21:02', '22:02']}, 
        'UniBe005': 
            {'Stim': [0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1], 
             'Time': ['00:30', '01:15', '02:06', '02:55', '03:35', '04:12', '04:47', '05:29', '06:28', '07:11', 
                      '07:54', '08:31', '09:07', '09:54', '10:43', '11:15', '11:54', '12:48', '13:19', '14:08', 
                      '14:51', '15:47', '16:24', '17:20', '18:12', '19:08', '19:53', '20:48', '21:26', '22:09']}, 
        'UniBe006': 
            {'Stim':[0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1], 
             'Time': ['00:30', '01:02', '01:56', '02:36', '03:17', '03:54', '04:32', '05:05', '05:42', '06:30', 
                      '07:15', '07:54', '08:46', '09:16', '09:46', '10:23', '11:13', '11:49', '12:44', '13:39', 
                      '14:35', '15:26', '16:02', '16:34', '17:16', '18:15', '18:48', '19:46', '20:21', '21:00']}, 
        'UniBe007': 
            {'Stim': [1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1], 
             'Time': ['00:30', '01:18', '02:06', '03:02', '03:39', '04:14', '05:13', '06:05', '06:47', '07:44', 
                      '08:42', '09:15', '10:06', '10:56', '11:56', '12:53', '13:23', '14:11', '14:51', '15:41', 
                      '16:34', '17:24', '18:07', '18:44', '19:43', '20:42', '21:42', '22:19', '22:53', '23:28']}, 
        'UniBe008': 
            {'Stim': [1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1], 
             'Time': ['00:30', '01:24', '02:11', '02:47', '03:25', '03:56', '04:27', '05:06', '05:37', '06:32', 
                      '07:24', '08:00', '09:00', '09:30', '10:26', '11:08', '12:08', '12:50', '13:45', '14:38', 
                      '15:37', '16:30', '17:11', '18:03', '18:55', '19:41', '20:31', '21:16', '22:10', '22:59']}, 
        'UniBe009': 
            {'Stim': [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0], 
             'Time': ['00:30', '01:25', '02:10', '02:43', '03:42', '04:15', '04:55', '05:40', '06:23', '06:58', 
                      '07:48', '08:36', '09:29', '10:09', '11:05', '11:49', '12:33', '13:18', '13:59', '14:56', 
                      '15:55', '16:50', '17:50', '18:46', '19:31', '20:30', '21:05', '22:05', '23:04', '23:57']}, 
        'UniBe010': 
            {'Stim': [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1], 
             'Time': ['00:30', '01:14', '02:09', '03:07', '03:57', '04:28', '05:25', '06:21', '06:56', '07:30', 
                      '08:22', '09:02', '09:38', '10:26', '11:05', '11:40', '12:21', '13:14', '14:06', '14:37', 
                      '15:13', '16:04', '16:44', '17:23', '18:20', '19:02', '19:40', '20:28', '21:18', '22:07']}, 
        'UniBe011': 
            {'Stim': [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1], 
             'Time': ['00:30', '01:10', '01:53', '02:29', '03:24', '04:00', '04:42', '05:33', '06:22', '07:20', 
                      '08:04', '08:52', '09:38', '10:35', '11:11', '12:01', '12:31', '13:08', '14:02', '14:39', 
                      '15:13', '15:54', '16:35', '17:25', '17:57', '18:43', '19:37', '20:29', '21:20', '22:08']}, 
        'UniBe012': 
            {'Stim': [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1], 
             'Time': ['00:30', '01:06', '01:57', '02:44', '03:22', '04:19', '05:06', '05:45', '06:31', '07:14', 
                      '08:06', '08:49', '09:36', '10:06', '10:50', '11:36', '12:24', '13:13', '14:08', '14:48', 
                      '15:26', '16:14', '17:07', '18:03', '18:49', '19:21', '20:18', '21:07', '21:54', '22:32']}, 
        'UniBe013': 
            {'Stim': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1], 
             'Time': ['00:30', '01:26', '02:01', '02:47', '03:39', '04:36', '05:20', '06:13', '07:05', '07:38', 
                      '08:23', '09:10', '10:09', '10:48', '11:38', '12:16', '12:46', '13:44', '14:15', '15:13', 
                      '15:51', '16:48', '17:33', '18:08', '18:57', '19:35', '20:33', '21:30', '22:13', '23:07']}}

class TimerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer GUI")
        self.current_set = None
        self.timer_running = False
        self.remaining_time = timedelta()
        self.upcoming_events = []

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        # Set Selection
        self.label_set = tk.Label(self.frame, text="Select Set:")
        self.label_set.grid(row=0, column=0, sticky="W")

        self.set_var = tk.StringVar()
        self.set_var.set("Select a set")
        self.set_dropdown = tk.OptionMenu(self.frame, self.set_var, *data.keys(), command=self.on_set_select)
        self.set_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="W")

        # Timer
        self.timer_label = tk.Label(self.frame, text="00:00", font=("Arial", 200), width=10)
        self.timer_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Upcoming Event
        self.event_label = tk.Label(self.frame, text="", font=("Arial", 100), fg="red")
        self.event_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Next Event Type
        self.event_type_label = tk.Label(self.frame, text="", font=("Arial", 100))
        self.event_type_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Begin Button
        self.begin_button = tk.Button(self.frame, text="Begin", command=self.start_timer, state=tk.DISABLED)
        self.begin_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def on_set_select(self, selected_set):
        self.current_set = selected_set
        self.begin_button["state"] = tk.NORMAL
        first_event_type = "TMT" if data[self.current_set]["Stim"][0] == 1 else "Saline"
        self.event_type_label["text"] = f"First Event Type: {first_event_type}"

    def start_timer(self):
        if self.current_set:
            self.timer_running =True
            self.begin_button["state"] = tk.DISABLED
            self.start_time = datetime.now()  # save the start time
            self.upcoming_events = [datetime.combine(date.today(), datetime.strptime(t, "%H:%M").time()) for t in data[self.current_set]["Time"]]
            self.countup()

    def countup(self):
        if self.timer_running:
            elapsed_time = datetime.now() - self.start_time  # calculate elapsed time
            mins, secs = divmod(int(elapsed_time.total_seconds()), 60)  # Convert elapsed time to mins:secs
            self.timer_label["text"] = f"{mins:02d}:{secs:02d}"

            if self.upcoming_events:
                upcoming_event = self.upcoming_events[0]
                elapsed_time_event = upcoming_event - datetime.now()

                if elapsed_time_event <= timedelta(seconds=30):
                    self.event_label["text"] = f"Upcoming Event: {upcoming_event.strftime('%M:%S')} ({elapsed_time_event.seconds}s)"
                    event_index = len(data[self.current_set]["Time"]) - len(self.upcoming_events)
                    if data[self.current_set]["Stim"][event_index] == 1:
                        self.event_type_label["text"] = "Next Event Type: TMT"
                    else:
                        self.event_type_label["text"] = "Next Event Type: Saline"
                else:
                    self.event_label["text"] = ""
                    self.event_type_label["text"] = ""

                if elapsed_time_event <= timedelta(seconds=0):
                    self.upcoming_events.pop(0)
            if self.timer_running:
                self.root.after(500, self.countup)  # check more often, e.g. every 500 ms
    

    def stop_timer(self):
        self.timer_running = False

root = tk.Tk()
root.attributes("-fullscreen", True)  # Make the GUI full screen
app = TimerGUI(root)
root.mainloop()


```


```python

```
