import sys
from IPython.utils.capture import capture_output
import subprocess
import os
import os.path
my_prompt = "#:\itay's shell> "
DEBUG = True
programs_path = 'programs files'


def ping(params):
    params_string = " ".join(params)
    ping_result = os.popen(f'cmd /c "ping {params_string}"').read()
    return ping_result


def dir(params):
    #dir_result = os.system('cmd /c "dir"')
    dir_result = os.popen('cmd /c "dir"').read()
    dir_result_splited = dir_result.split("\n")[7:][:-3]
    dir_result_cutted = "\n".join(dir_result_splited)
    return dir_result_cutted


def cd(params):
    #cd_result = os.popen(f'cd {params[0]}')
    params_string = " ".join(params)
    cd_result = os.chdir(params_string)
    if cd_result:
        return cd_result
    else:
        return f"[+] Changed Current Working Dir To:\n{pwd('')}"


def pwd(params):
    pwd_result = os.popen('cmd /c cd ').read()
    cwd = os.getcwd()
    return cwd


def help_cmnd(params):
    return "HELP: \n\n"


def set_cmnd(params):
    params_string = " ".join(params)
    set_result = os.popen(f'cmd /c "set {params_string}"').read()
    return set_result


def external_prog(file_name, params):
    global programs_path

    if ".py" not in file_name:
        file_name += ".py"
    if DEBUG:
        print("is: " + programs_path + "/" + file_name + " exists?: ")
        print(os.path.isfile(programs_path + "/" + file_name))
    if os.path.isfile(programs_path + "/" + file_name):
        return run_external_prog(file_name, params)
    else:
        if DEBUG:
            print("is: " + file_name + " exists?: ")
            print(os.path.isfile(file_name))
        if os.path.isfile(file_name):
            return run_downloaded_prog(file_name, params)


def run_downloaded_prog(file_name, params):
    params_string = " ".join(params)
    if ".py" not in file_name:
        file_name += ".py"

    if DEBUG:
        print(f"run_downloaded_prog: \n cmnd = {file_name}, params = {params}")
    if params_string:
        to_send = os.popen(f'python {file_name} {params_string}').read()
    else:
        to_send = os.popen(f'python {file_name}').read()
    return to_send


def run_external_prog(cmnd, params):
    global programs_path
    cd([programs_path])
    params_string = " ".join(params)
    if ".py" not in cmnd:
        cmnd += ".py"

    if DEBUG:
        print(f"run_external_prog: \n cmnd = {cmnd}, params = {params}")


    if params_string:
        to_send = os.popen(f'python {cmnd} {params_string}').read()
    else:
        try:
            to_send = os.popen(f'python {cmnd}').read()
        except Exception as err:
            print("err " + str(err))
    return to_send


def set_cmd(params):
    params_string = " ".join(params)
    to_send = os.popen(f'{params_string}').read()
    return to_send


def cmnd_manu(cmnd, params):
    if DEBUG:
        print("cmnd = " + cmnd + ">> changed: " + cmnd.lower())
        print("params = " + str(params))
    cmnd = cmnd.lower()
    if cmnd == "exit":
        to_print = "[-] Quitting"
        quit()
    elif cmnd == "help":
        to_print = help_cmnd(params)
    elif cmnd == "dir":
        to_print = dir(params)
    elif cmnd == "ping":
        to_print = ping(params)
    elif cmnd == "cd":
        to_print = cd(params)
    elif cmnd == "pwd":
        to_print = pwd(params)
    elif cmnd == "set":
        to_print = set_cmnd(params)
    elif cmnd == "cmd":
        to_print = set_cmd(params)
    else:
        to_print = external_prog(cmnd, params)
        #to_print = f"[-] Command '{cmnd}' Not found :("
    return to_print


def split_to_cmnd_n_params(line):
    cmnd_param = line.split(" ")
    cmnd = cmnd_param[0]
    cmnd_param = cmnd_param[1:]
    return cmnd, cmnd_param


def main():

    #subprocess.run(["prompt", "itay's shell\\"])
    os.chdir("C:/Users/itays/PycharmProjects/itayshell")
    shell_input = input(my_prompt)
    print("shell input", shell_input[-2:-1])
    if ">" in shell_input and ">" not in shell_input[-2:-1]:
        input_splited = shell_input.split(" > ")
        file_to_direct_output = input_splited[1]
        cmnd_param = input_splited[0]
        cmnd_param = cmnd_param.split(" ")
        cmnd = cmnd_param[0]
        with open(file_to_direct_output, "w") as file:
            file.write(cmnd_manu(cmnd, cmnd_param))
        return
    
    if "|" in shell_input and "|" not in shell_input[-2:-1]:
        input_splited = shell_input.split(" | ")
        pipe_right_side = input_splited[0]
        pipe_left_side = input_splited[1]
        left_cmnd, left_params = split_to_cmnd_n_params(pipe_left_side)
        with capture_output() as c:
            cmnd_manu(left_cmnd, left_params)
        right_cmnd, right_params = split_to_cmnd_n_params(pipe_right_side)
        right_params = right_params + c.stdout.split(" ")
        print(cmnd_manu(right_cmnd, right_params))
        return

    cmnd_param = shell_input.split(" ")
    cmnd = cmnd_param[0]
    params = []
    for i in range(1, len(cmnd_param)):
        params.append(cmnd_param[i])

    try:
        to_print = cmnd_manu(cmnd, params)
        print(to_print)
    except NameError as f:
        print(f"[-] {cmnd} Not found :(")
    except Exception as err:
        print("General Error:", err)
        print(sys.exc_info()[0].__name__, os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename),
              sys.exc_info()[2].tb_lineno)
    return


if __name__ == '__main__':
    try:
        print(my_prompt + "Hello")
        while True:
            main()
    except Exception as ff:
        "Bye Bye"

