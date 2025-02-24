# aap-terraform-template

This template is an opiniated starting point for deploying Ansible Automation Platform with Terraform.

## Features

**The features include:**

- Dev env managed w/ [mise](https://mise.jdx.dev/)
- Secrets ecnrypted w/ [sops](https://github.com/getsops/sops). No plain text secrets in your git repository
- Infrastrcture provisioned w/ [Terraform](https://github.com/hashicorp/terraform) on AWS
- Ansible Automation Platform installation using [Ansible](https://github.com/ansible/ansible)
- Comes with pre-configured settings for [Visual Studio Code](https://github.com/microsoft/vscode)

## 🚀 Let's Go!

There are **4 stages** outlined below for completing this project, make sure you follow the stages in order.

### Stage 1: Prepare external requirements

1. [Configure your AWS profile and credentials](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html) in ~/.aws/credentials. 

### Stage 2: Local Workstation

1. Create a new **public** repository by clicking the big green "Use this template" button at the top of this page.

2. Use `git clone` to download **the repo you just created** to your local workstation and `cd` into it.

3. **Install** and **activate** [mise](https://mise.jdx.dev/) following the instructions for your workstation [here](https://mise.jdx.dev/getting-started.html).

4. Use `mise` to install the **required** CLI tools:

   📍 _If `mise` is having trouble compiling Python, try running `mise settings python.compile=0` and try these commands again_

    ```sh
    mise trust
    mise install
    mise run deps
    ```

### Stage 3: Template Configuration

> [!IMPORTANT]
> The [config.sample.yaml](./config.sample.yaml) file contains config that are **vital** to the template process.

1. Generate the `config.yaml` from the [config.sample.yaml](./config.sample.yaml) configuration file:

   📍 _If the below command fails `mise` is either not install or configured incorrectly._

    ```sh
    task init
    ```

2. Fill out the `config.yaml` configuration file using the comments in that file as a guide.

3. Template out all the configuration files:

   📍 _`task --list` gives you a full list of tasks if you want to run some steps manually._

    ```sh
    task configure
    ```

4. Push your changes to git:

   📍 _**Verify** all the `.sops.*` files are **encrypted** with SOPS_

    ```sh
    git add -A
    git commit -m "chore: initial commit :rocket:"
    git push
    ```

### Stage 4: Bootstrap VMs and AAP

📍 _You can run `task deploy` instead of executing every step manually._

1. Proviosion infrastructure on AWS:

    ```sh
    task deploy:terraform-apply
    ```

2. Configure the VMs and install Ansible Application Platform

   📍 _Installation of Ansible Application Platform takes a lot of time. It's normal to wait for 30-40 minutes on the "Run Ansible Automation Installer" step with no progress._

    ```sh
    task deploy:ansible-apply
    ```

3. Get host information to add to /etc/hosts

    ```sh
    task deploy:output-results
    ```

## 💥 Reset

There might be a situation where you want to destroy your cluster. The following command will unregister your VMs and remove all provisioned cloud infrastructure.

```sh
task nuke
```

## 🤝 Thanks

This template has been heavily inspired by [onedr0p's cluster-template](https://github.com/onedr0p/cluster-template) and [mikhailknyazev](https://github.com/mikhailknyazev).
