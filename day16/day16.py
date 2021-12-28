version_sum = 0
bit_pile = []

def read_num_of_packets(number):
    global version_sum, bit_pile
    pccs = []
    read_bits = 0 
    for i in range(number):
        print("Read num loop ")
        print(bit_pile)
        try:
            packet_version = int(bit_pile[:3], base=2)
            bit_pile = bit_pile[3:]
            read_bits += 3
            type_id = int(bit_pile[:3], base=2)
            bit_pile = bit_pile[3:]
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
                bits_of_literal = bit_pile[:5]
                bit_pile = bit_pile[5:]
                read_bits += 5
                if bits_of_literal[0] == "0":
                    read_next = False
                translated_list.extend(bits_of_literal[1:])
            pccs.append(int("".join(translated_list),base=2))
        else:
            # Operator packet
            length_type_id = bit_pile[:1]
            bit_pile = bit_pile[1:]
            read_bits += 1
            if length_type_id == "0":
                length_in_bits = bit_pile[:15]
                bit_pile = bit_pile[15:]
                read_bits += 15
                pack = read_packets(int(length_in_bits, base=2))
                bit_pile = bit_pile[int(length_in_bits, base=2):]
                read_bits += int(length_in_bits, base=2)
                pccs.append(pack)
            else:
                num_of_subpacks = bit_pile[:11]
                bit_pile = bit_pile[11:]
                read_bits += 11
                pack, read_bits_2 = read_num_of_packets(int(num_of_subpacks, base=2))
                read_bits += read_bits_2
                pccs.append(pack)
    return pccs, read_bits


def read_packets(leng=None):
    global version_sum, bit_pile
    packs = []
    bitts = 0
    if leng is None:
        leng = len(bit_pile)
    while len(bit_pile) > 6 and int(bit_pile,base=2) != 0 and bitts < leng:
        print("Read packets loop ")
        print(bit_pile)
        try:
            packet_version = int(bit_pile[:3], base=2)
            bit_pile = bit_pile[3:]
            bitts += 3
            type_id = int(bit_pile[:3], base=2)
            bit_pile = bit_pile[3:]
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
                bits_of_literal = bit_pile[:5]
                bit_pile = bit_pile[5:]
                bitts += 5
                if bits_of_literal[0] == "0":
                    read_next = False
                translated_list.extend(bits_of_literal[1:])
            packs.append(int("".join(translated_list),base=2))
        else:
            # Operator packet
            length_type_id = bit_pile[:1]
            bit_pile = bit_pile[1:]
            bitts += 1
            if int(length_type_id,base=2) == 0:
                length_in_bits = bit_pile[:15]
                bit_pile = bit_pile[15:]
                bitts += 15
                pack = read_packets(int(length_in_bits, base=2))
                packs.append(pack)
            else:
                num_of_subpacks = bit_pile[:11]
                bit_pile = bit_pile[11:]
                pack, read_bits = read_num_of_packets(int(num_of_subpacks, base=2))
                bitts += read_bits
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
    bit_pile = binary_str
    print(read_packets())
    print("Part 1: ", version_sum)