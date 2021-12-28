class Scanner:
    def __init__(self, beacons) -> None:
        self.beacons = beacons
        self.x = 0
        self.y = 0
        self.z = 0
        self.orientation = 0

    def rotate_next(self):
        if 0 <= self.orientation <= 2:
            self.rotate_x()
        if self.orientation == 3:
            self.rotate_x()
            self.rotate_z()
        if 4 <= self.orientation <= 6:
            self.rotate_y()
        if self.orientation == 7:
            self.rotate_y()
            self.rotate_z()
        if 8 <= self.orientation <= 10:
            self.rotate_x()
        if self.orientation == 11:
            self.rotate_x()
            self.rotate_z()
        if 12 <= self.orientation <= 14:
            self.rotate_y()
        if self.orientation == 15:
            self.rotate_y()
            self.rotate_z()
            self.rotate_y()
        if 16 <= self.orientation <= 18:
            self.rotate_z()
        if self.orientation == 19:
            self.rotate_z()
            self.rotate_y()
            self.rotate_y()
        if 20 <= self.orientation <= 22:
            self.rotate_y()
        if self.orientation == 23:
            self.rotate_z()
            self.rotate_y()
        self.orientation = (self.orientation + 1) % 24


    def print(self):
        print("#" * len(self.beacons[0]))
        for b_l in self.beacons:
            print(b_l)
        print("#" * len(self.beacons[0]))

    def rotate_x(self):
        # X doesn't change
        # Transpose matrix on y and z then reverse rows
        new_beacons = []
        for b_l in self.beacons:
            new_beacons.append([b_l[0], b_l[2], -b_l[1]])
        self.beacons = new_beacons

    def rotate_y(self):
        # Y doesn't change
        # Transpose matrix on x and z then reverse rows
        new_beacons = []
        for b_l in self.beacons:
            new_beacons.append([b_l[2], b_l[1], -b_l[0]])
        self.beacons = new_beacons

    def rotate_z(self):
        # Z doesn't change
        # Transpose matrix on x and y then reverse rows
        new_beacons = []
        for b_l in self.beacons:
            new_beacons.append([b_l[1], -b_l[0], b_l[2]])
        self.beacons = new_beacons

    def copy(self):
        copied = []
        for b in self.beacons:
            copied.append(b[:])
        s = Scanner(copied)
        s.x = self.x
        s.y = self.y
        s.z = self.z
        return s 

def read_input():
    scanners = []
    with open("day19/input.txt", "r") as f:
        for line in [ln.rstrip('\n') for ln in f.readlines()]:
            if line == "":
                scanners.append(Scanner(beacons))
                continue
            if line.startswith("---"):
                beacons = []
            else:
                beacons.append([int(n) for n in line.split(",")])
    return scanners


if __name__ in "__main__":
    scanners = read_input()
    num_of_scanners = len(scanners)
    # Everything is related to the first scanner
    correct_scanners = [scanners[0]]
    correct_scanners[0].x = 0
    correct_scanners[0].y = 0
    correct_scanners[0].z = 0
    scanners = scanners[1:]
    next_corrects = [correct_scanners[0]]
    while len(correct_scanners) < num_of_scanners:
        removers = []
        last_corrects = next_corrects
        next_corrects = []
        print("Progress: ", len(correct_scanners))
        for si, scanner in enumerate(scanners):
            print(si)
            should_break = False
            for _ in range(24):
                for beacon in scanner.beacons:
                    for cscan in correct_scanners:
                        for cbeacon in cscan.beacons:
                            # Assume beacon and cbeacon are the same, check for overlap
                            temp_scanner = scanner.copy()
                            temp_scanner.x, temp_scanner.y, temp_scanner.z = [cb - v for (cb, v) in zip(cbeacon, beacon)]
                            # Temp scanner has xyz relative to 0
                            for i, beac in enumerate(temp_scanner.beacons):
                                temp_scanner.beacons[i] = [b + e for (b, e) in zip(beac, [temp_scanner.x, temp_scanner.y, temp_scanner.z])]
                            num_of_beacons = 0
                            for cbeacon2 in cscan.beacons:
                                for beac2 in temp_scanner.beacons:
                                    if cbeacon2 == beac2:
                                        num_of_beacons += 1
                            if num_of_beacons >= 12:
                                # We have overlap
                                print("Overlap")
                                removers.append(si)
                                correct_scanners.append(temp_scanner)
                                next_corrects.append(temp_scanner)
                                last_corrects.append(temp_scanner)
                                should_break = True
                                break
                        if should_break:
                            break
                    if should_break:
                        break
                if should_break:
                    break
                scanner.rotate_next()
        removers.sort(reverse=True)
        for index in removers:
            scanners.pop(index)
    print("DONE")
    beacons2 = []
    for scanner in correct_scanners:
        for beacon in scanner.beacons:
            if tuple(beacon) not in beacons2:
                beacons2.append(beacon)
    print("Part 1: ", len(beacons2))




