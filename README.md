# Buckets full of secret plans

This is the companion repository to the 2023 Mercari Security team blog on Terraform data exfiltration.
The repository is contains three directories:

- `setup/`: The Terraform configuration for setting up the environment necessary for the levels.
- `secrets_receiver/`: The code for the secrets receiver sever used in levels 1 and 2 as well as the decoder used in level 3.
- `levels/`: The solutions for all the levels presented in the blog post.

*General note*: For all directories containing Terraform configuration you will have to configure the Terraform variables to match your environment. Todo this run `cp terraform.tfvars.example terraform.tfvars` and then modify the variables in the file.

## Setup

### Levels 1, 2a and 3

The levels 1, 2a and 3 all use the Google Cloud Platform (GCP) as the victim environment and thus require that you have access to a GCP project. To setup the environment for these level you will have to `apply` the Terraform configuration in `setup/gcp` after configuring the correct Terraform variables.

```bash
cd setup/gcp
terraform apply -var-file="terraform.tfvars"
```

For level 3 you will also have to setup the attacker environment. Note that you can use the same GCP project for the victim environment and the attacker, if you don't want to setup a separate GCP project for it.

```bash
cd setup/level_3_attacker
terraform apply -var-file="terraform.tfvars"
```

### Level 2b

This level use AWS for the victim environment so you will need access to an AWS account. To setup the resources necessary for the you will have to `apply` the Terraform configuration the `setup/aws` directory after configuring the Terraform variables.

```bash
cd setup/aws
terraform apply -var-file="terraform.tfvars"
```

## Secrets Receiver

Levels 1, 2a, 2b require that the secrets receiver is run. First you will have to install the required packages for the server. We recommend installing them in a virtual environment:

```bash
cd secrets_receiver
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

After you have installed all the necessary packages you can run the secrets receiver in your virtual environment by executing:

```bash
python3 server.py
```

By the default the secrets receiver will bind onto host `127.0.0.1` on port `80`. Depending on your system this might require privileged execution. You can change the host and port the receiver binds to by setting the environment variables:

- `SECRETS_RECEIVER_HOST`
- `SECRETS_RECEIVER_PORT`

For the levels presented in the blog it is enough to run the secrets receiver listening only on localhost. Since the receiver is using the Flask development server we do not recommend binding it to a publicly accessible port.

## The Levels


Before you use the terraform configurations in the sub directories you will have to create your own `terraform.tfvars` file for your environment. Each directory provides a `terraform.tfvars.example` file you can use as a reference. Note that for level 3 there are additional instructions in the [03_access_logs/README.md](./levels/03_access_logs/README.md) file.

Each level can be executed after following the setup instructions and configuring the Terraform variables by running:

```
cd levels/<level>
terraform plan -var-file="terraform.tfvars
```

## Contribution

Please read the CLA below carefully before submitting your contribution.

https://www.mercari.com/cla/

## License

Copyright 2023 Mercari,

Licensed under the MIT License.
