import os
import datetime
import argparse

argparser = argparse.ArgumentParser()
# 参数tt
argparser.add_argument('--tt', type=float, required=True,help='super parameter tt')
argparser.add_argument('--cuda',type=int, required=True,help="cardid")

if_log = False

# 读取一个文件夹下的所有文件
base_dir = './data'
dataset = 'taught'
floder = base_dir + '/' + dataset + '/'
files = os.listdir(floder)
# 过滤后缀不是ply的文件
files = [file for file in files if file.endswith('.ply')]

for i in range(len(files)):
    f = files[i]
    # 设置输出路径
    output_local_dir = './local_net/'+dataset+'/'+f.split('.')[0]+'/'
    output_global_dir = './glocal_net/'+dataset + '/'+f.split('.')[0]+'/'
    
    cardid = argparser.parse_args().cuda
    base_cmd = 'nohup python pcp2.py ' + '--CUDA ' + str(cardid) + ' --save_idx -1' + ' --data_dir ' + floder + ' --OUTPUT_DIR_LOCAL ' + output_local_dir + ' --OUTPUT_DIR_GLOBAL ' + output_global_dir + ' --input_ply_file ' + f    

    train_local_cmd = base_cmd  + ' --train   '
    train_pred_cmd  = base_cmd  + ' --finetune'
    test_cmd        = base_cmd  + ' --test    '
    
    cmds = [train_local_cmd, train_pred_cmd, test_cmd]
    for cmd in cmds:
        tt = argparser.parse_args().tt
        cmd = cmd + ' --tt ' + str(tt)
        print(cmd)
        # os.system(cmd)
      
    



