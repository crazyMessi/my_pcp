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
print(files)

for i in range(len(files)):
    # 记录时间
    starti = str(datetime.datetime.now())
    f = files[i]
    # 设置输出路径
    output_local_dir = './local_net/'+dataset+'/'+f.split('.')[0]+'/'
    output_global_dir = './glocal_net/'+dataset + '/'+f.split('.')[0]+'/'
    
    # 打印进度和当前文件名
    print('processing: ' + f + ' ' + str(i) + '/' + str(len(files)))
    cardid = argparser.parse_args().cuda
    base_cmd = 'nohup python pcp2.py ' + '--CUDA ' + str(cardid) + ' --save_idx -1' + ' --data_dir ' + floder + ' --OUTPUT_DIR_LOCAL ' + output_local_dir + ' --OUTPUT_DIR_GLOBAL ' + output_global_dir + ' --input_ply_file ' + f    
    # 设置log文件路径
    log_file = './log/' + dataset + '/' + f.split('.')[0] + '.log'
    # 创建log文件夹
    if not os.path.exists('./log/'):
        os.mkdir('./log/')
    if not os.path.exists('./log/' + dataset):
        os.mkdir('./log/' + dataset)    

    train_local_cmd = base_cmd  + ' --train   '
    train_pred_cmd  = base_cmd  + ' --finetune'
    test_cmd        = base_cmd  + ' --test    '
    
    cmds = [train_local_cmd, train_pred_cmd, test_cmd]
    # 设置命令
    print('-----------------------------------')
    for cmd in cmds:
        tt = argparser.parse_args().tt
        cmd = cmd + ' --tt ' + str(tt)
        cmd = cmd + ' > ' + log_file + ' 2>&1'
        print(cmd)
        startcmdi = datetime.datetime.now()
        with open(log_file, 'a') as f:
            f.write('-----------------------------------\n')
            f.write(cmd + '\n')
            f.write("start: " + str(startcmdi) + '\n')
        os.system(cmd)
        with open(log_file, 'a') as f:
            f.write("end:   " + str(datetime.datetime.now()) + '\n\n')
            f.write('cost:  ' + str(datetime.datetime.now() - startcmdi) + '\n')
    
    # 记录时间
    endi = str(datetime.datetime.now())
    # 写入时间
    with open(log_file, 'a') as f:
        f.write('start: ' + starti + '\n')
        f.write('end:   ' + endi + '\n')
        f.write('-----------------------------------\n')
    print('-----------------------------------\n')


