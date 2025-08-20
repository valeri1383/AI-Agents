
import shutil
from datetime import datetime

def backup_database():
    src = 'path_to_database'
    dest = f'backups/backup_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.db'
    shutil.copy(src, dest)
    print('Backup completed!')

if __name__ == '__main__':
    backup_database()
