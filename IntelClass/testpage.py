import pyshark

capture = pyshark.FileCapture("./icmp.pcapng")

cur_frame = capture[16]

plen = f"РАЗМЕР ДАННЫХ: {cur_frame.ipv6.plen}"
nxt = f"СЛЕДУЮЩИЙ ЗАГОЛОВОК: IPV6 ({cur_frame.ipv6.nxt})"
hlim = f"ЛИМИТ ПЕРЕХОДОВ: {cur_frame.ipv6.hlim}"
src = f"IPV6-АДРЕС ИСТОЧНИКА: {cur_frame.ipv6.src}"
dst = f"IPV6-АДРЕС НАЗНАЧЕНИЯ: {cur_frame.ipv6.dst}"
        #src_slaac_mac = f"SLAAC MAC ИСТОЧНИКА: {cur_frame.ipv6.src_slaac_mac}"

print(f"{plen}\n{nxt}\n{hlim}\n{src}\n{dst}\n")
