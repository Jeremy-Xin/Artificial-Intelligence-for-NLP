from make_graph import process as process_graph
from build_distance import process as process_distance
from build_neighbour_station import process as process_station

def main():
    process_graph()
    process_distance()
    process_station()

if __name__ == '__main__':
    main()