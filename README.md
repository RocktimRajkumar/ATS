# Template Based Information Extraction Rule (TIER) - Parser
![Project Image](project-image-url)

<center>

[![GitHub issues](https://img.shields.io/github/issues/RocktimRajkumar/AWS_POC)](https://github.com/RocktimRajkumar/AWS_POC/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub forks](https://img.shields.io/github/forks/RocktimRajkumar/AWS_POC)](https://github.com/RocktimRajkumar/AWS_POC/network)
[![GitHub stars](https://img.shields.io/github/stars/RocktimRajkumar/AWS_POC)](https://github.com/RocktimRajkumar/AWS_POC/stargazers) 
![GitHub repo size](https://img.shields.io/github/repo-size/RocktimRajkumar/AWS_POC)
![GitHub contributors](https://img.shields.io/github/contributors/RocktimRajkumar/AWS_POC)

</center>

> Intelligent Template based Data Extraction of significant fields and use them as a meaningful information from all incoming documents with similar layouts.

---

## Prerequisites
Before you begin, ensure you have met the following requirements:


1. Python 3.8 or later.
2. AWS account.

---

### Table of Contents

- [Description](#description)
- [How To Use](#how-to-use)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)
- [Author Info](#author-info)

---

## Description



#### Technologies

- AWS services (Textract, Comprehend)
- Python
---

## How To Use

#### Installation
 The AWS Command Line Interface(CLI) is a unified tool to manage AWS services.
 
**Windows**<br>
[Download](https://awscli.amazonaws.com/AWSCLIV2.msi) 

**Linux**
```
$ curl "https://awscli.amazonaws.com/$ awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ unzip awscliv2.zip
$ sudo ./aws/install
```

**macOS**
```
$ curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
$ sudo installer -pkg AWSCLIV2.pkg -target /
```

    
#### Configuration
Configure AWS-CLI help you to interact with AWS services.These include your security credentials, the default output format, and the default AWS Region.
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AWS requires that all incoming requests are cryptographically signed. The AWS CLI does this for you.<p>

**Quickly Configuring the AWS CLI**
```
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json
```
When you enter this command, the AWS CLI prompts you for four pieces of information (access key, secret access key, AWS Region, and output format)

**To create access keys**

1. Sign in to the AWS Management Console and open the IAM console at https://console.aws.amazon.com/iam/.

2. In the navigation pane, choose Users.

3. Choose the name of the user whose access keys you want to create, and then choose the Security credentials tab.

4. In the Access keys section, choose Create access key.

5. To view the new access key pair, choose Show. You will not have access to the secret access key again after this dialog box closes. Your credentials will look something like this: 
    ``` 
        Access key ID: AKIAIOSFODNN7EXAMPLE

        Secret access key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    ```

6. To download the key pair, choose Download .csv file. Store the keys in a secure location. You will not have access to the secret access key again after this dialog box closes.

7. Keep the keys confidential in order to protect your AWS account and never email them. Do not share them outside your organization, even if an inquiry appears to come from AWS or Amazon.com. No one who legitimately represents Amazon will ever ask you for your secret key.

8. After you download the .csv file, choose Close. When you create an access key, the key pair is active by default, and you can use the pair right away.

#### API Reference

``` html
    <p>dummy code</p>
```

---

## Contributing 

To contribute to TIER-Parser, follow these steps:

1. Fork this repository.
2. Create a branch: git checkout -b <branch_name>.
3. Make your changes and commit them: git commit -m '<commit_message>'
4. Push to the original branch: git push origin <project_name>/<location>
5. Create the pull request.

Alternatively see the GitHub documentation on creating a pull request.

---

## Credits
Thanks to the following people who have contributed to this project.

* [@Naveen Gainedi](https://in.linkedin.com/in/naveengainedi)
* [@Koushtav Chakraborty](https://in.linkedin.com/in/koushtavc)
---

## License

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the [MIT](LICENSE) license.


---

## Author Info

- LinkedIn - [@RocktimRajkumar](https://www.linkedin.com/in/rocktim-rajkumar/)
- Github - [@RocktimRajkumar](https://github.com/RocktimRajkumar)

