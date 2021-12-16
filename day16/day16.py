version_sum = 0

def read_num_of_packets(bits, number):
    global version_sum
    pccs = []
    read_bits = 0 
    for i in range(number):
        print("Read num loop ")
        print(bits)
        try:
            packet_version = int(bits[:3], base=2)
            bits = bits[3:]
            read_bits += 3
            type_id = int(bits[:3], base=2)
            bits = bits[3:]
            read_bits += 3
        except ValueError:
            return pccs, read_bits
        version_sum += packet_version
        print("Versum ", packet_version, version_sum, "Pccs", pccs)
        # Literal value
        if type_id == 4:
            read_next = True
            translated_list = []
            while read_next:
                bits_of_literal = bits[:5]
                bits = bits[5:]
                read_bits += 5
                if bits_of_literal[0] == "0":
                    read_next = False
                translated_list.extend(bits_of_literal[1:])
            pccs.append(int("".join(translated_list),base=2))
        else:
            # Operator packet
            length_type_id = bits[:1]
            bits = bits[1:]
            read_bits += 1
            if length_type_id == "0":
                length_in_bits = bits[:15]
                bits = bits[15:]
                read_bits += 15
                pack = read_packets(bits[:int(length_in_bits, base=2)])
                bits = bits[int(length_in_bits, base=2):]
                read_bits += int(length_in_bits, base=2)
                pccs.append(pack)
            else:
                num_of_subpacks = bits[:11]
                bits = bits[11:]
                read_bits += 11
                pack, read_bits_2 = read_num_of_packets(bits[:], int(num_of_subpacks, base=2))
                read_bits += read_bits_2
                pccs.append(pack)
    print("Version ", packet_version, version_sum, "PCCS: ", pccs)
    return pccs, read_bits


def read_packets(bits):
    global version_sum
    packs = []
    bitts = 0
    while len(bits) > 6 and int(bits,base=2) != 0:
        print("Read packets loop ")
        print(bits)
        try:
            packet_version = int(bits[:3], base=2)
            bits = bits[3:]
            bitts += 3
            type_id = int(bits[:3], base=2)
            bits = bits[3:]
            bitts += 3
        except ValueError:
            return packs
        version_sum += packet_version
        print("Versum ", packet_version, version_sum, "Packs", packs)
        # Literal value
        if type_id == 4:
            read_next = True
            translated_list = []
            while read_next:
                bits_of_literal = bits[:5]
                bits = bits[5:]
                bitts += 5
                if bits_of_literal[0] == "0":
                    read_next = False
                translated_list.extend(bits_of_literal[1:])
            packs.append(int("".join(translated_list),base=2))
        else:
            # Operator packet
            length_type_id = bits[:1]
            bits = bits[1:]
            bitts += 1
            if int(length_type_id,base=2) == 0:
                length_in_bits = bits[:15]
                bits = bits[15:]
                bitts += 15
                pack = read_packets(bits[:int(length_in_bits, base=2)])
                bits = bits[int(length_in_bits, base=2):]
                bitts += int(length_in_bits,base=2)
                packs.append(pack)
            else:
                num_of_subpacks = bits[:11]
                bits = bits[11:]
                pack, read_bits = read_num_of_packets(bits, int(num_of_subpacks, base=2))
                bits = bits[read_bits:]
                bitts += read_bits
                print(read_bits)
                packs.append(pack)
    print("Version ", packet_version, version_sum, "Paccs: ", packs)
    return packs

if __name__ in "__main__":
    with open("day16/input.txt", "r") as f:
        binary_str = ""
        for ch in f.read():
            if ch in "0123456789ABCDEFabcdef":
                binary_rep = bin(int(ch,base=16))[2:]
                while len(binary_rep) < 4:
                    binary_rep = "0" + binary_rep
                binary_str += binary_rep
    print(read_packets(binary_str))
    print("Part 1: ", version_sum)