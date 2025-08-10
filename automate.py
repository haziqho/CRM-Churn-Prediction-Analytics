
# Simple orchestration script: ETL -> Features -> Train
import subprocess

def run(cmd):
    print('>>>', ' '.join(cmd))
    subprocess.check_call(cmd)

if __name__ == '__main__':
    run(['python','src/etl.py'])
    run(['python','src/build_features.py'])
    run(['python','src/train_model.py'])
