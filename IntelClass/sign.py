import pyshark
capture = pyshark.FileCapture("./traffic_cap1.pcapng")

id = 203

print(capture[id].frame_info.protocols.split(':'))
print(str(capture[id].tcp.flags))