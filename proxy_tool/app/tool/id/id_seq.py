from enum import IntEnum


# 给id generator分配 work id
# 取值范围：51 - 63
class IdSeq(IntEnum):
    metasploit = 51
    exploit_db = 52
    packetstormsecurity = 53
    coresecurity = 54
    cxsecurity = 55
    security_database_snort =56
    fortiguard = 57
    acunetix = 58
    standard_vul = 60
