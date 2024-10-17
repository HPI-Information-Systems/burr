import subprocess
import wandb

class PostgresClient:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        
    def update_database(self, script_path):
        wandb.save(script_path)
        command = ['psql', '-f', script_path, '-U', self.user, '-d', self.database]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print("Databaseupload execution failed with return code:", result.returncode)
            print("Error output:")
            print(result.stderr)