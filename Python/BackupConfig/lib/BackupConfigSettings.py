
# XLSX_Path = "..\\data\\Data-Origin.xlsx"
XLSX_Path = "..\\data\\Data.xlsx"
DataDict = {}
Global_ErrorMess = {}
FtpServerIP = "11.148.164.224"
FtpServerUsername = "liuyubo"
FtpServerPassword = "11223344"
FtpServerRoot = "D:\\FTP"

H3C = '''
save
y


y
ftp {0} source ip {5}
{1}
{2}
ascii
put startup.cfg {4}/H3C/{3}
quit
quit
'''
H3C_Cv7 = "save force \n\n copy startup.cfg ftp://{0}:{1}@{2}/{4}/H3C/{3} \n "
MaiPu = '''
enable
{6}
filesystem
copy running-config ftp {0} {1} {2} {4}/MaiPu/{3}
end
exit
exit
'''
Cisco = '''
'''

run_cmd_dict = {'H3C': H3C, 'MaiPu': MaiPu, 'Cisco': Cisco}
