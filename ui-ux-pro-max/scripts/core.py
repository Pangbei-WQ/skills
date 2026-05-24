import os
import csv

class DesignIntelligence:
    def __init__(self, base_path):
        self.base_path = base_path
        self.data_path = os.path.join(base_path, 'data')
        
    def get_reasoning(self, domain):
        """Retrieves design DNA for a specific domain."""
        with open(os.path.join(self.data_path, 'ui-reasoning.csv'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['domain'].lower() == domain.lower():
                    return row
        return None

    def get_style_tokens(self, style_name):
        """Retrieves detailed style tokens for a specific style."""
        with open(os.path.join(self.data_path, 'styles.csv'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['style_name'].lower() == style_name.lower():
                    return row
        return None
