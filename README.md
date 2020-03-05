# Getting Start
1. Configure aws cli using Access Key ID and Secret Access Key
2. Create a s3 bucket
3. Upload a document in s3 bucket and defined the co-ordinate in template/template.json file using the followinig format:
> {</br>
			&emsp;&emsp;"resolution":{</br>
						&emsp;&emsp;&emsp;&emsp;"width": 1654,</br>
						&emsp;&emsp;&emsp;&emsp;"height" 355</br>
			&emsp;&emsp;&emsp;},</br>
			&emsp;&emsp;"group":[</br>
			&emsp;&emsp;&emsp;&emsp;{</br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"gid": "0",</br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"gname": "group name",</br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"desc":"group description",</br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"x0":83,</br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"y0":23,</br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"x1":832,</br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"y1":344</br>
			&emsp;&emsp;&emsp;&emsp;},</br>
			&emsp;&emsp;&emsp;&emsp;{</br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"gid": "1",</br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"gname": "group name",</br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"desc":"group description",</br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"x0":83,</br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"y0":23,</br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"x1":832,</br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"y1":344</br>
			&emsp;&emsp;&emsp;&emsp;}</br>
			&emsp;&emsp;]</br>
			&emsp;}</br>

or use the template which is already defined in template.json and upload invoice.pdf file in s3 bucket</br>
4. Change the bucketName and fileName if required then Execute POC_input.py file, it will create the textract block object from the file in s3 bucket and format and store the response in json file.<br>
5. Change the bucketName and fileName if required then Execute template/template.py file, it will group the element on the basis of template defined and store the result in template/group_element/*.json file.<br>
6. Change the fileName if required then Execute template/detect_group_entities.py file, it will classify the element into people, places, locations, date etc and store the result in template/entity_group_element*.json file.