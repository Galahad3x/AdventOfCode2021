input="""4057231006FF2D2E1AD8025275E4EB45A9ED518E5F1AB4363C60084953FB09E008725772E8ECAC312F0C18025400D34F732333DCC8FCEDF7CFE504802B4B00426E1A129B86846441840193007E3041483E4008541F8490D4C01A89B0DE17280472FE937C8E6ECD2F0D63B0379AC72FF8CBC9CC01F4CCBE49777098D4169DE4BF2869DE6DACC015F005C401989D0423F0002111723AC289DED3E64401004B084F074BBECE829803D3A0D3AD51BD001D586B2BEAFFE0F1CC80267F005E54D254C272950F00119264DA7E9A3E9FE6BB2C564F5376A49625534C01B0004222B41D8A80008446A8990880010A83518A12B01A48C0639A0178060059801C404F990128AE007801002803AB1801A0030A280184026AA8014C01C9B005CE0011AB00304800694BE2612E00A45C97CC3C7C4020A600433253F696A7E74B54DE46F395EC5E2009C9FF91689D6F3005AC0119AF4698E4E2713B2609C7E92F57D2CB1CE0600063925CFE736DE04625CC6A2B71050055793B4679F08CA725CDCA1F4792CCB566494D8F4C69808010494499E469C289BA7B9E2720152EC0130004320FC1D8420008647E8230726FDFED6E6A401564EBA6002FD3417350D7C28400C8C8600A5003EB22413BED673AB8EC95ED0CE5D480285C00372755E11CCFB164920070B40118DB1AE5901C0199DCD8D616CFA89009BF600880021304E0EC52100623A4648AB33EB51BCC017C0040E490A490A532F86016CA064E2B4939CEABC99F9009632FDE3AE00660200D4398CD120401F8C70DE2DB004A9296C662750663EC89C1006AF34B9A00BCFDBB4BBFCB5FBFF98980273B5BD37FCC4DF00354100762EC258C6000854158750A2072001F9338AC05A1E800535230DDE318597E61567D88C013A00C2A63D5843D80A958FBBBF5F46F2947F952D7003E5E1AC4A854400404A069802B25618E008667B7BAFEF24A9DD024F72DBAAFCB312002A9336C20CE84"""

#input_decimal = """D2FE28"""
#input_decimal = """EE00D40C823060""" #3 sub-pakets
input_decimal = """38006F45291200"""


from functools import reduce

def get_bin_val(input):
    temp = int(input, 16)
    res = bin(temp)[2:]
    while len(res) < 4:
        res = "0" + res
    return res

def parse_packet_value(decoded, index):
    if index >= len(decoded) or int(decoded[index:], 2) == 0:
        return (0, len(decoded))
    res = 0
    version = int(decoded[index:index + 3], 2)
    res += version
    type = int(decoded[index + 3:index + 6], 2)
    index_r = index + 6
    value = 0
    if type == 4:
        val = ''
        condition = True
        while condition:
            if decoded[index_r] == '0':
                val = val + decoded[index_r + 1:index_r + 5]
                index_r += 5
                condition = False
            else:
                val = val + decoded[index_r + 1:index_r + 5]
                index_r += 5
    else:
        if decoded[index_r] == '0':
            len_sub_p = 15
            index_r += 1
            length = int(decoded[index_r:index_r + len_sub_p], 2)
            index_r += len_sub_p
            # here no operations on first star
            index_u = index_r
            while(index_r < index_u + length):
                (resadd, add) = parse_packet_value(decoded, index_r)
                res+=resadd
                index_r = add
        else:
            len_sub_p = 11
            index_r += 1
            number_sub = int(decoded[index_r:index_r + len_sub_p], 2)
            index_r += len_sub_p
            # here no operations on first star
            for i in range(number_sub):
                (resadd, add) =  parse_packet_value(decoded, index_r)
                res+=resadd
                index_r = add
    return (res, index_r)


def parse_packet(decoded, index):
    if index >= len(decoded) or int(decoded[index:], 2) == 0:
        return (-1, len(decoded))
    res = 0
    version = int(decoded[index:index + 3], 2)
    res+= version
    type = int(decoded[index + 3:index + 6], 2)
    index_r = index + 6
    value = 0
    if type == 4:
        val = ''
        condition = True
        while condition:
            if decoded[index_r] == '0':
                val = val + decoded[index_r + 1:index_r + 5]
                index_r += 5
                condition = False
            else:
                val = val + decoded[index_r + 1:index_r + 5]
                index_r += 5
        value = int(val, 2)
    else:
        l=[]
        if decoded[index_r] == '0':
            len_sub_p = 15
            index_r += 1
            length = int(decoded[index_r:index_r + len_sub_p], 2)
            index_r += len_sub_p
            # here no operations on first star
            index_u = index_r
            while(index_r < index_u + length):
                (resadd, add) = parse_packet(decoded, index_r)
                if resadd >=0:
                    l.append(resadd)
                index_r = add
        else:
            len_sub_p = 11
            index_r += 1
            number_sub = int(decoded[index_r:index_r + len_sub_p], 2)
            index_r += len_sub_p
            # here no operations on first star
            for i in range(number_sub):
                (resadd, add) =  parse_packet(decoded, index_r)
                if resadd >= 0:
                    l.append(resadd)
                index_r = add

        if type == 0:
            value = sum(l)
        elif type == 1:
            value = reduce(lambda x,y: x*y, l)
        elif type == 2:
            value = min(l)
        elif type == 3:
            value = max(l)
        elif type == 5:
            value = 1 if l[0] > l[1] else 0
        elif type == 6:
            value = 1 if l[0] < l[1] else 0
        elif type == 7:
            value = 1 if l[0] == l[1] else 0
    return (value, index_r)

def first_star():
    decoded = ""
    for x in input:
        decoded = decoded + get_bin_val(x)
    print(f"First star: {parse_packet_value(decoded, 0)[0]}")

def second_star():
    decoded = ""
    for x in input:
        decoded = decoded + get_bin_val(x)
    print(f"Second star: {parse_packet(decoded, 0)[0]}")



if __name__ == '__main__':
   first_star()
   second_star()
