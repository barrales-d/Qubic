import csv


def time_file(csv_file_name: str) -> None:
    with open(csv_file_name + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['depth', 'Minimax time taken(seconds)', 'Alpha Beta time taken(seconds)', ])

def mark_times(csv_file_name, depth: int, minimax_times: list[float], alphabeta_times: list[float]) -> None:
    def format_time(time):
        return "{:.3f}".format(time)
    
    with open(csv_file_name + '.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        max_len =  min(len(minimax_times), len(alphabeta_times))

        for idx in range(max_len):
            writer.writerow([str(depth)] + [format_time(minimax_times[idx])] + [format_time(alphabeta_times[idx])])


def game_won_file(csv_file_name: str, mm_win_count, ab_win_count, draw_count) -> None:
    with open(csv_file_name + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Minimax won', 'Alpha Beta won', 'Draws'])
        writer.writerow([mm_win_count, ab_win_count, draw_count])


def mark_winner(csv_file_name: str, h_won, mm_won, ab_won, draw) -> None:
    with open(csv_file_name + '.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([h_won, mm_won, ab_won, draw])
