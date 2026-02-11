import shutil
import os
from src.db_manager import DBManager
from src.logger import get_logger

class UndoManager:
    def __init__(self):
        self.db = DBManager()
        self.logger = get_logger()

    def perform_selective_undo(self, session_op_ids, target_undo_id):
        """
        session_op_ids: O anki gruptaki tüm dosyaların ID'leri.
        target_undo_id: Özellikle geri alınmak (A klasörüne dönmesi) istenen dosya.
        """
        # Burada bütün işlemler geri alınıyor 
        for op_id in session_op_ids:
            with self.db._get_connection() as conn:
                op = conn.execute("SELECT * FROM operations WHERE id = ?", (op_id,)).fetchone()
                if op and os.path.exists(op['new_path']):
                    try:
                        shutil.move(op['new_path'], op['old_path'])
                        conn.execute("UPDATE operations SET status = 'UNDONE' WHERE id = ?", (op_id,))
                        self.logger.info(f"Geçici Geri Alma: {op['new_path']}")
                    except Exception as e:
                        self.logger.error(f"Taşıma hatası: {e}")

        # Burada sadece hangi işlem özelliği istenmiyorsa o çıkarılıyor ve tekrardan işlemi yapıyoruz
        redo_ids = [id for id in session_op_ids if id != target_undo_id]
        
        if redo_ids:
            from src.organizer import Organizer
            re_organizer = Organizer()
            for op_id in redo_ids:
                with self.db._get_connection() as conn:
                    op = conn.execute("SELECT old_path FROM operations WHERE id = ?", (op_id,)).fetchone()
                    if op:
                        re_organizer.organize_file(op['old_path'])
                        self.logger.info(f"Tekrar Organize Edildi: {op['old_path']}")

        return True
    