# E-Net_framework
The framework of E-Net building.

## To run the code or train
* **Environment**:

Pytorch 1.2

Python 3.7

The following libs may be required:
boto3 six tqdm requests regex sentencepiece

* **Manuscript**:
````
python kagnet_5w1h.py  --language_model xlnet-base-cased   --do_train  --do_lower_case   --do_eval 
--data_dir ../datasets/csqa_new   --train_batch_size 8  --eval_batch_size 4  --learning_rate 1e-4  
--num_train_epochs 100.0  --max_seq_length 100  --output_dir ./saved_models/  --save_model_name bert_large_1e-4    
--gradient_accumulation_steps 4
````


### E-Net framework 1.0
* ATOMIC (sharing exactly the same form with E-Net) interface is provided
* XLNet tokenizer is added
![.architecture 1.0](https://github.com/gogowhy/ENet_framework/blob/master/images/enet1_0.jpg)
