def process_blocks(fname_in,fname_out):
    with open(fname_in, 'r',encoding="UTF-8") as file:
        text = file.read()
    
    # Split the text into blocks separated by double newlines
    blocks = text.strip().split('\n\n')
    
    # Open the output file for writing
    with open(fname_out, 'w',encoding="UTF-8") as outfile:
        # Process each block
        for block in blocks:
            # Replace newlines within each block with spaces
            single_line = ' '.join(block.split('\n'))
            outfile.write(single_line + '\n')

if __name__ == "__main__":
    process_blocks("tmp.txt","tmp_out.txt")