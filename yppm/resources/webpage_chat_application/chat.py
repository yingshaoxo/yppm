import os
from complete import load_data, get_next_text_block

resource_basic_folder_path = os.path.dirname(os.path.abspath(__file__))
offline_question_and_answer_bot_dataset_path = os.path.join(resource_basic_folder_path, "./yingshaoxo_txt_data")

Has_Data = True
if not os.path.exists(offline_question_and_answer_bot_dataset_path):
    print("Run following command before anything:")
    print("git clone https://gitlab.com/yingshaoxo/yingshaoxo_txt_data.git")
    Has_Data = False

def read_text_files(folder_path):
    new_text = ""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.txt', '.md')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        new_text += f.read() + "\n"
                except UnicodeDecodeError:
                    try:
                        with open(file_path, 'r', encoding='latin-1') as f:
                            new_text += f.read() + "\n"
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
    return new_text

new_text = read_text_files(offline_question_and_answer_bot_dataset_path)
the_text_list = [one.strip() for one in new_text.split("\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n") if one.strip() != ""]
new_text_list = []
for one in the_text_list:
    temp_list1 = one.split("\n#")
    temp_list2 = []
    for sub_one in temp_list1:
        if "第" in sub_one and "章" in sub_one:
            temp_list2 += sub_one.split("\n\n\n")
        else:
            temp_list2 += [sub_one]
    new_text_list += temp_list2
the_text_list = new_text_list
new_text = "\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n".join(the_text_list)

load_data("", text_data=new_text)

def my_unquote(encoded_str):
    if "%u" in encoded_str:
        parts = encoded_str.split('%u')[1:]
        decoded_str = ''.join(chr(int(code, 16)) for code in parts)
        return decoded_str
    else:
        return encoded_str

def get_response(input_text):
    if not input_text:
        return "Please say something!"

    if Has_Data == True:
        input_text = my_unquote(input_text)
        natural_next_text = get_next_text_block(input_text)
        return input_text + " " + natural_next_text
    else:
        return "You said: " + input_text
