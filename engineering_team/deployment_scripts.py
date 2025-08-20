
import subprocess

def deploy():
    subprocess.run(['docker-compose', 'up', '-d'])
    print('Deployment completed!')

if __name__ == '__main__':
    deploy()
