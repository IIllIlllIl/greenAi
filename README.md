# greenAi
This is the mutation test framework to estimate how Deep Learning (DL) hyperparameters affect energy consumption. It can mutate the hyperparameters and collect the energy metrics of the package, RAM, and GPU. Besides, it can analyze the correlation and trade-off between the metrics and hyperparameters. We are very grateful to thank Georgiou et al. [^1] for their contibution on ICSE22. This framework is designed based on their [ICSE_2022_artifact](https://github.com/stefanos1316/ICSE_2022_artifact). <br>

[^1]: S. Georgiou, M. Kechagia, T. Sharma, F. Sarro, Y. Zou, Green ai: Do
deep learning frameworks have different costs?, in: Proceedings of the 44th
International Conference on Software Engineering, ICSE ’22, Association
for Computing Machinery, New York, NY, USA, 2022, p. 1082–1094. doi:
10.1145/3510003.3510221. URL https://doi.org/10.1145/3510003.3510221

This repository contains:
- `mutation`: codes to conduct mutation tests on DL models. We did our mutation test on five open-source DL programs, including [mnist](https://github.com/pytorch/examples/tree/main/mnist), [mnist_forward_forward](https://github.com/pytorch/examples/tree/main/mnist_forward_forward), [siamese_network](https://github.com/pytorch/examples/tree/main/siamese_network), [pytorch_resnet_cifar10](https://github.com/akamaster/pytorch_resnet_cifar10), and [Person_reID_baseline_pytorch](https://github.com/layumi/Person_reID_baseline_pytorch). The codes are organized by the names of five models. Each directory includes `governor.sh`, `run.sh`, `shell.py`, and`result`. <br>
- `mutation/*/governor.sh `: a shell code to switch the CPU setting. <br>
- `mutation/*/run.sh `: This is a script to start the training and collect the energy metrics. Therefore, it is written based on the command line instructions to train the model. <br>
- `mutation/*/shell.py `: a Python script to mutate the hyperparameters and call `run.sh` to train the mutation. It repeats the mutation test automatically and writes the result into `result`. <br>
- `mutation/*/result `: the directory consists of `collect.py` and `data`. `collect.py` is a Python script to collect the output of `shell.py` in`data` and process the original output and organize them. <br>
- `analysis`: data and codes to conduct the analysis. The data we collected are organized in `analysis/comp/*.txt` and `analysis/*.txt`, which are collected from `mutation`. The three Python scripts can conduct three types of analysis, including correlation analysis, trade-off analysis, and parallel analysis. <br>

# Prerequisite
- Linux version 5.19.0-45-generic
- perf
- nvidia-smi
- Python 3.7.0

# Installation
1. Download this repository by:

		git clone https://github.com/IIllIlllIl/greenAi.git

2. Install the tools (`perf` and `nvidia-smi`). The vision of tools depends on your operating system. Be cautious that the function we used of `perf` may not work on some devices.
3. Install the models and their datasets. They can be installed from their repositories.
	- [mnist](https://github.com/pytorch/examples/tree/main/mnist)
	- [mnist_forward_forward](https://github.com/pytorch/examples/tree/main/mnist_forward_forward)
	- [siamese_network](https://github.com/pytorch/examples/tree/main/siamese_network)
	- [pytorch_resnet_cifar10](https://github.com/akamaster/pytorch_resnet_cifar10)
	- [Person_reID_baseline_pytorch](https://github.com/layumi/Person_reID_baseline_pytorch)
4. Install the relative Python codebase by:

		pip install -r requirements.txt

# Mutation
1. To run our mutation test on the five models, we need to copy our files to their repository downloaded from GitHub. For a chosen model, the needed files include `governor.sh`, `run.sh`, `shell.py`, and`result` under the directory with the name of the model in 'mutation'. The files above should be copied to the same directory with the training code, such as `main.py` or `train.py`.
2. Then we can use 'shell.py' to run our experiment, like

		python shell.py -k all

	This command will mutate all hyperparameters and collect the metrics. `-k` defines the type of mutation. if you wish to mutate a single hyperparameter, like change `epochs` to value 0.1, you can use the option, like

		python shell.py -k epochs -e 0.1

	The options we provide can be listed by:

		python shell.py -h

3. The results of the `shell.py` will be written to the 'result' directory. We can check them there. The files of the result will be named `pe190-0`. `e` means this mutation has a different `epochs` value, 190. `-0` means this is the first repeat of this mutation.

# Analysis
1. To analyze the metrics, we need to reorganize the output of the mutation first. Or you can use the data we prepared in `analysis`. We can use `collect.py` to do all this work under the `result` directory. First, we reorganize the output and write them into the `data` directory. For example, if we want to collect the data `pe190`, which includes `pe190-0`, `pe190-1`, `pe190-2`, `pe190-3`, and `pe190-4`, we can use the command:

		python collect.py -c pe190

	Be cautious that the output of the original model is also named `pe200` (here we assume the original value of `epochs` is 200). To collect these data, we should rename them before running `collect.py` by

		cp pe200-0 p-0

2. After reorganization, execute `collect.py ` again to compile the results:

		python collect.py -n pe190

	The output of this command should be copied into a text file like `analysis/*.txt` we provided. Then move these text files to the `analysis` directory.

3. With these text files, we can run the analysis codes, make sure that you replace the text file we provide with the same file name. Run the corresponding Python code to run the analysis. For instance, to run the correlation analysis, 

		python rq1-correlation.py

	`rq1-correlation.py` conducts the correlation analysis between hyperparameters and metrics. `rq2-trade-off.py` conducts the trade-off analysis in common environments and parallel environments. `rq3-parallel.py` conducts the correlation analysis in parallel environments.

# Run on your models
To run the code on your models, three scripts in `mutation` should be modified, including `run.sh`, `shell.py`, and`collect.py`. 
- `run.sh`: the bash commands to start training in this script should be changed. For example, in `mutation/mnist/run.sh`, these codes are written as:

		collect_energy_measurements "python3 main.py --gamma="$g" --lr="$lr" --epochs="$epoch"" "$repetitions"

	`python3 main.py` execute the training, `--gamma="$g" --lr="$lr" --epochs="$epoch"` pass the mutated value.<br>
	If you plan to mutate new hyperparameters, two parts should be changed. First, the default value of your new hyperparameters should be added here:

		# Set default values
		repetitions=1
		epoch=14
		lr=1.0
		g=0.7

	second, the codes getting arguments:

		# Get command-line arguments
		OPTIONS=$(getopt -o r:e:l:w: --long repetitions:test -n 'run_experiments' -- "$@")
		eval set -- "$OPTIONS"
		while true; do
		  case "$1" in
		    -r|--repetitions) repetitions="$2"; shift 2;;
		    -e|--epoch) epoch="$2"; shift 2;;
		    -l|--lr)lr="$2";shift 2;;
		    -g|--gamma)g="$2";shift 2;;
		    -h|--help) help_info; shift;;
		    --) shift; break;;
		    *) >&2 log "${redlabel}[ERROR]${default} Wrong command line argument, please try again."; exit 1;;
		  esac
		done

- `shell.py`: to mutate your new hyperparameters, the mutation operator functions and its callee should be changed. For the mutation operator functions, in `mutation/mnist/shell.py`:

		def modify_epoch(current_epoch, target=None):
	    if target is None:
        	flag = random.sample([-1, 1], 1)[0]
	        if flag == 1:
        	    new_epoch = current_epoch - int(current_epoch * random.random() * 0.25)
	        else:
        	    new_epoch = current_epoch + int(current_epoch * random.random() * 0.25)
	        # make sure new_epoch != cur_epoch, except cur_epoch is minimized (1)
        	if new_epoch == current_epoch:
	            new_epoch = max(1, min(10, new_epoch) - 1)
	    else:
        	new_epoch = target
	    return new_epoch

	You can write a mutation operator function for your new hyperparameters. <br> For its callee:

		if mutate_key == "all":
		    shell("e", args.epochs)
		    mutate("lr", args.learning_rate)
		    mutate("g", args.gamma)
		    mutate("epochs", args.epochs)
		elif mutate_key == "epochs":
		    print(args.epochs)
		    mutate(mutate_key, args.epochs)
		elif mutate_key == "lr":
		    print(args.learning_rate)
		    mutate(mutate_key, args.learning_rate)
		elif mutate_key == "g":
		    print(args.gamma)
		    mutate(mutate_key, args.gamma)
		elif mutate_key == "measure":
		    test = [14]
		    mutate_reputation = 5
		    for i in range(len(test)):
		        shell("e", test[i])

	You need to add the option `mutation_key` for your new hyperparameters and write its workflow. Also, if you wish to run `-k all`, you also need to rewrite the code below  `if mutate_key == "all":`.

- `collect.py`: In this script, the function of reading accuracy should be modified. For example, in `mutation/mnist/collect.py` it is written as:

		pre_data = open(path + "/out.log", 'r')
    	try:
        pre = "0"
        while True:
            line = pre_data.readline()
            if line:
                if 'Accuracy: ' in line:
                    pre = line.split(" ")
                    for piece in pre:
                        if '/' in piece:
                            pre = float(piece.split("/")[0]) / 10000
            else:
                break
        data.append(pre)
    	finally:
        pre_data.close()
	
	To use `collect.py` on your text file, you need to change the codes above which read the accuracy metrics.

Also, the codes in `analysis` need to be modified. To analyze your data, the paths of the text file should be rewritten. The paths are saved in the list named `paths`. For example, in the `rq1-correlation.py`, they are written as follows:

	paths = ["mnist_new", "mff", "sia", "resnet", "hr18"]

After rewritting these paths, the analysis code can be executed on the text file of your models.