import os
import csv


directory = 'e:/Projects/slips/photos'
output_file = 'e:/Projects/slips/consolidated_data.csv'

data = []

for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        
        
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            
            
            for row in reader:
                if len(row) == 1:
                    item, cost = row[0].strip().rsplit(',', 1)
                    cost = cost.strip().replace('\n', '')  
                    data.append([item.strip(), cost])
                else:
                    data.append(row)


with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Item', 'Cost'])  
    writer.writerows(data)  

total_cost = sum(float(row[1]) for row in data)

print(f"Consolidated data saved to: {output_file}")
print(f"Total cost: {total_cost:.2f}")