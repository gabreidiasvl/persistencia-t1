import csv
import os
import shutil
from typing import List, Dict, Optional

class MiniDB:
    def __init__(self, entity_name: str):
        self.entity_name = entity_name
        self.csv_file = f"{entity_name}.csv"
        self.seq_file = f"{entity_name}.seq"
        # O cabeçalho agora define a estrutura de uma avaliação completa
        self.header = ['id', 'nome_usuario', 'titulo_midia', 'tipo_midia', 'estrelas', 'comentario', 'deleted']
        self._initialize_db()

    def _initialize_db(self):
        if not os.path.exists(self.seq_file):
            with open(self.seq_file, 'w') as f:
                f.write('0')
        
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.header)

    def _get_next_id(self) -> int:
        with open(self.seq_file, 'r+') as f:
            current_id = int(f.read().strip())
            next_id = current_id + 1
            f.seek(0)
            f.write(str(next_id))
            f.truncate()
            return next_id

    def insert(self, record: Dict) -> Dict:
        new_id = self._get_next_id()
        record['id'] = new_id
        record['deleted'] = False
        
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.header)
            writer.writerow(record)
        return record

    def get_by_id(self, record_id: int) -> Optional[Dict]:
        with open(self.csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['id']) == record_id:
                    if row.get('deleted', 'false').lower() != 'true':
                        return row
                    return None 
        return None

    def get_all(self, page: int = 1, page_size: int = 10) -> List[Dict]:
        records = []
        skip_count = (page - 1) * page_size
        
        with open(self.csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            valid_records_count = 0
            for row in reader:
                if row.get('deleted', 'false').lower() != 'true':
                    if valid_records_count >= skip_count:
                        if len(records) < page_size:
                            records.append(row)
                        else:
                            break 
                    valid_records_count += 1
        return records
    
    # Adicionamos uma função de busca para filtrar por título
    def search_by_title(self, titulo: str) -> List[Dict]:
        records = []
        with open(self.csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Busca case-insensitive
                if titulo.lower() in row['titulo_midia'].lower() and row.get('deleted', 'false').lower() != 'true':
                    records.append(row)
        return records

    def update(self, record_id: int, data_update: Dict) -> Optional[Dict]:
        temp_file = f"{self.csv_file}.tmp"
        found = False
        updated_record = None

        with open(self.csv_file, 'r', newline='', encoding='utf-8') as infile, \
             open(temp_file, 'w', newline='', encoding='utf-8') as outfile:
            
            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, fieldnames=self.header)
            writer.writeheader()

            for row in reader:
                if int(row['id']) == record_id and row.get('deleted', 'false').lower() != 'true':
                    found = True
                    # Atualiza apenas os campos permitidos
                    row['estrelas'] = data_update.get('estrelas', row['estrelas'])
                    row['comentario'] = data_update.get('comentario', row['comentario'])
                    updated_record = row
                writer.writerow(row)
        
        if found:
            shutil.move(temp_file, self.csv_file)
            return updated_record
        else:
            os.remove(temp_file)
            return None

    def soft_delete(self, record_id: int) -> bool:
        temp_file = f"{self.csv_file}.tmp"
        found = False
        with open(self.csv_file, 'r', newline='', encoding='utf-8') as infile, \
             open(temp_file, 'w', newline='', encoding='utf-8') as outfile:
            
            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, fieldnames=self.header)
            writer.writeheader()

            for row in reader:
                if int(row['id']) == record_id:
                    row['deleted'] = 'True'
                    found = True
                writer.writerow(row)
        
        if found:
            shutil.move(temp_file, self.csv_file)
            return True
        else:
            os.remove(temp_file)
            return False

    def count(self) -> int:
        count = 0
        try:
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('deleted', 'false').lower() != 'true':
                        count += 1
        except FileNotFoundError:
            return 0
        return count