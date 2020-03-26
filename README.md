# Template Based Information Extraction Rule (TIER) - Parser
<p align="center">
 <a href="https://media-exp1.licdn.com/dms/image/C560BAQFZ1nG-bnju2w/company-logo_200_200/0?e=2159024400&v=beta&t=WuKfeEccF7JVm71qILciqH20hxwAJSMGgalhq6W5e4I">
<img src="https://media-exp1.licdn.com/dms/image/C560BAQFZ1nG-bnju2w/company-logo_200_200/0?e=2159024400&v=beta&t=WuKfeEccF7JVm71qILciqH20hxwAJSMGgalhq6W5e4I" alt="Project Image">
</a>
 </p>

<p align="center">
<a href="https://github.com/RocktimRajkumar/ATS/issues">
<img src="https://img.shields.io/github/issues/RocktimRajkumar/ATS" alt="issue">
</a>

<a href="https://github.com/RocktimRajkumar/ATS/blob/master/LICENSE.md">
 <img src="https://img.shields.io/badge/License-MIT-informational.svg" alt="ATS is released under the MIT license." />
</a>

<a href="https://github.com/RocktimRajkumar/ATS/network">
<img src="https://img.shields.io/github/forks/RocktimRajkumar/ATS?color=blueviolet" alt="forks">
</a>


<a href="https://github.com/RocktimRajkumar/ATS/stargazers">
<img src="https://img.shields.io/github/stars/RocktimRajkumar/ATS?color=yellow" alt="stars">
</a>

<a href="#">
<img src="https://img.shields.io/github/repo-size/RocktimRajkumar/ATS?color=green" alt="Repository Size">
</a>

<a href="#">
<img src="https://img.shields.io/github/contributors/RocktimRajkumar/ATS" alt="Contributors">
</a>

</p>

>Power by Machine Learning, TIER-parser recognition processes is highly-variant invoices and documents in capabilities far beyond any Optical Character Recognition application Program.</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;It easily extracts complex data from highly varied, multifaceted business invoices.</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Our cloud-based technology ensures best-in-class security and scalability, as well as full 24/7 access on any device.

**Features**
* Build Reusable extraction templates based on text mining patterns and extract desired data from unstructured documents.
* Automates the entires business process around the ingestion of unstructured data.

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
For a long time, we have relied on paper invoices to process payments and maintain accounts. Reconciling invoices typically involves someone manually spending hours browsing through several invoices and jotting things down in a ledger.

>**But can this process be done better, more efficiently, with less wastage of paper, human labor and time?**

So, we present you Template Based Information Extraction Rule(TIER)-Parser.
<p>It's an Intelligent Template-based Data Extraction of significant fields and uses them as a piece of meaningful information from all incoming documents with similar layouts.</p>

The system depends on the knowledge base. The knowledgebase contains facts and rules. The facts are derived from the Standard model like **AWS comprehend**. The rules represent
the designed templates. The templates are helpful for detecting the meaning of the text. 

### **How does TIER-Parser work?**
TIER-Parser is a three-step procedure:-
* AWS textract analyzes the document thoroughly, extracts the essential data and format it as required.
* Grouping the line of text based on the template.
* Classifying the text such as (invoice date, address, name, etc). 

### **Technologies**

- AWS services (S3, Textract, Comprehend)
- Python
---

## How To Use

### **Installation**
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

**Requirements Files**<br>
"Requirement Files" are files containing a list of items to be installed using pip install.  
```
    $ python -m pip install -r requirements.txt
```

    
### **Configuration**
Configure AWS-CLI helps you to interact with AWS services. These include your security credentials, the default output format, and the default AWS Region.
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

**How To create access keys**

[Steps](Create-Access-Key.md)


### **Usage** 
This section will instruct other people on how to use our project after they’ve installed it.
1. **Designed Template**<br>
The templates are designed according to the morphological,
syntactical and vocabulary components of text sentences.<br>
The designed templates are created for helping to get the meaningful extraction of text from the unstructured documents.<br>
The template represents, resolution of the image and list of groups. Each group has its x0,y0, and x1,y1 co-ordinates, group id, name of the group and description.<br>
i.e.
![template](template/template.png)<br>
In the above image red boxes are the groups and the green dots are the co-ordinates i.e x0,y0 and x1,y1.<br>
*Syntax of Template*:-
    ```
    {
        "resolution": {
            "width": 1654,
            "height": 2339
                },
        "group": [
                {
                    "gid": "0",
                    "gname": "Group0",
                    "desc": "Group0 Description",
                    "x0": 70,
                    "y0": 60,
                    "x1": 639,
                    "y1": 404
                },
                {
                    "gid": "1",
                    "gname": "Group1",
                    "desc": "Group1 Description",
                    "x0": 1046,
                    "y0": 70,
                    "x1": 1625,
                    "y1": 375
                }
        ]
    }

    ```
Create your template and save it inside the template directory as .json file.<br>

2. **Run Program**
    ```
       $ python main.py "bucketName" "fileName" "templateName"
    ```

    > "bucketName" :- Name of the s3 bucket<br>
"fileName" :- Name of the file in s3 bucket<br>
"templateName" :- Name of the template created inside the template directory

    e.g
    ```
    $ python main.py poc-cloud-bucket invoice.pdf template.json
    ```
You will see output similar to the following:
![output](template/output.png)

The program creates 3 JSON files.
* <p>First file contain all the Line of text detected in a document, it also returns the location and geometry of items found on a document page</p>

* <p>Second file group the Line of text detected based on template</p>

* <p>Third file read the group of the line of text and extract information like (invoice date, invoice number, date, name, address, etc).</p>



## Contributing 

To contribute to TIER-Parser, follow these steps:

1. Fork this repository.
2. Create a branch: git checkout -b <branch_name>.
3. Make your changes and commit them: git commit -m '<commit_message>'
4. Push to the original branch: git push origin <project_name>/<location>
5. Create the pull request.

Alternatively, see the GitHub documentation on creating a pull request.

---

## Credits
Thanks to the following people who have contributed to this project.

* [@Naveen Gainedi](https://in.linkedin.com/in/naveengainedi)
* [@Koushtav Chakraborty](https://in.linkedin.com/in/koushtavc)
---

## License

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the [MIT](LICENSE.md) license.


---

## Author Info

- LinkedIn - [@RocktimRajkumar](https://www.linkedin.com/in/rocktim-rajkumar/)
- Github - [@RocktimRajkumar](https://github.com/RocktimRajkumar)

