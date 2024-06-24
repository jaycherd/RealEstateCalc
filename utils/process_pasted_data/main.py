import constants
import re


def process_blocks(fname_in,fname_out):
    with open(fname_in, 'r',encoding="UTF-8") as file:
        text = file.read()
    
    # Split the text into blocks separated by double newlines
    blocks = text.strip().split('\n\n')
    
    # Open the output file for writing
    with open(fname_out, 'w',encoding="UTF-8") as outfile:
        # Process each block
        max_price_change = 0
        for block in blocks:
            # Replace newlines within each block with spaces
            lines = block.split('\n')
            cleaned_lines = []
            for line in lines:
                if "Source" in line:
                    continue
                cleaned_line = re.sub(r'\s+', ' ', line).strip()
                cleaned_lines.append(cleaned_line)

            cleaned_lines.reverse()
            price_change_num = 1
            for i,line in enumerate(cleaned_lines):
                if "Price change" in line:
                    new_line = line + str(price_change_num)
                    price_change_num += 1
                    cleaned_lines[i] = new_line
            cleaned_lines.reverse()
            new_cleaned_lines = []
            for i,line in enumerate(cleaned_lines):
                cleaned_line = []
                for word in line.split(" "):
                    rmv_flag = False
                    for rmv_word in constants.RMV_WORDS:
                        if rmv_word in word:
                            rmv_flag = True
                            break
                    if rmv_flag:
                        continue
                    cleaned_line.append(word)
                if cleaned_line:
                    new_cleaned_lines.append(" ".join(cleaned_line))
            max_price_change = max(max_price_change,price_change_num)
                    

            single_line = ' '.join(new_cleaned_lines)
            outfile.write(single_line + '\n')
    print(f"max num of price changes was {max_price_change}")

if __name__ == "__main__":
    process_blocks("tmp.txt","tmp_out.txt")